"""cut_clips.py — extract raw select clips from an approved edl.json for a
Premiere handoff (no baked fades, no reframe crop, no grade).

Stage 7 of the reworked video-use pipeline. See SKILL.md.
"""

import argparse
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

_UNSAFE = re.compile(r"[^A-Za-z0-9]+")


def _safe_token(s: str) -> str:
    """Filesystem-safe token; case preserved, non-alnum runs → single '-'."""
    return _UNSAFE.sub("-", s).strip("-")


def parse_ranges(spec: str | None, n: int) -> list[int]:
    """None → all indices [0, n). Else a comma list of in-range ints."""
    if spec is None:
        return list(range(n))
    out: list[int] = []
    for part in spec.split(","):
        i = int(part.strip())
        if i < 0 or i >= n:
            raise ValueError(f"range index {i} out of bounds [0, {n})")
        out.append(i)
    return out


def kebab(title: str) -> str:
    """Lowercase kebab slug for session folder names."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def sanitize_beat(beat: str | None) -> str:
    """Beat label as a filename token; case preserved. None/'' → ''."""
    if not beat:
        return ""
    return _safe_token(beat)


def clip_filename(
    index: int, beat: str | None, source: str, ext: str = "mov"
) -> str:
    """seg_<NN>_<BEAT>_<source>.<ext>; the _<BEAT> part is omitted if absent."""
    parts = ["seg", f"{index:02d}"]
    b = sanitize_beat(beat)
    if b:
        parts.append(b)
    parts.append(_safe_token(source))
    return "_".join(parts) + f".{ext}"


def clamp_window(
    start: float, end: float, handles: float, src_dur: float
) -> tuple[float, float]:
    """Pad [start, end] by `handles` on each side, clamped to [0, src_dur].

    Returns (in, out) rounded to millisecond precision.
    """
    if handles < 0:
        raise ValueError(f"handles must be >= 0, got {handles}")
    if src_dur <= 0:
        raise ValueError(f"source duration must be > 0, got {src_dur}")
    if start >= end:
        raise ValueError(f"start ({start}) must be < end ({end})")
    in_ = max(0.0, start - handles)
    out = min(src_dur, end + handles)
    return round(in_, 3), round(out, 3)


def clip_hash(src_path: str, in_: float, out: float, codec: str) -> str:
    """Stable identity for idempotent re-runs: same inputs → same hash."""
    canonical = f"{src_path}|{in_:.3f}|{out:.3f}|{codec}"
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


# Codec-specific encode args. ProRes 422 HQ (profile 3) + PCM is the
# edit-friendly, near-visually-lossless default for a Premiere handoff.
_CODEC_ARGS = {
    "prores": [
        "-c:v", "prores_ks", "-profile:v", "3",
        "-pix_fmt", "yuv422p10le", "-c:a", "pcm_s16le",
    ],
    "h264": [
        "-c:v", "libx264", "-preset", "slow", "-crf", "14",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
        "-movflags", "+faststart",
    ],
}


def ffmpeg_cmd(
    src: str, in_: float, out: float, codec: str, out_path: str
) -> list[str]:
    """argv for a raw select extract: frame-accurate, no fades, no reframe.

    Uses input-side seeking (`-ss` before `-i`) to seek instantly, and `-t`
    after `-i` to transcode exactly the duration needed. This is both fast
    and frame-accurate because we are transcoding.
    """
    if codec not in _CODEC_ARGS:
        raise ValueError(f"unknown codec {codec!r}; expected prores or h264")
    dur = out - in_
    return [
        "ffmpeg", "-y",
        "-ss", f"{in_:.3f}",
        "-i", src,
        "-t", f"{dur:.3f}",
        *_CODEC_ARGS[codec],
        "-map", "0:v:0", "-map", "0:a:0?", out_path,
    ]


def parse_probe_duration(probe: dict) -> float:
    """Seconds from `ffprobe -show_format -show_streams` JSON.

    Prefers container duration; falls back to the first video stream.
    """
    fmt_dur = probe.get("format", {}).get("duration")
    if fmt_dur is not None:
        return float(fmt_dur)
    for st in probe.get("streams", []):
        if st.get("codec_type") == "video" and st.get("duration") is not None:
            return float(st["duration"])
    raise ValueError("no duration in ffprobe output")


def should_skip(
    prev_entry: dict | None, cur_hash: str, file_exists: bool
) -> bool:
    """Idempotency: skip only if the output exists and matches a prior OK run."""
    return (
        file_exists
        and prev_entry is not None
        and prev_entry.get("hash") == cur_hash
        and prev_entry.get("status") == "ok"
    )


def build_clip_entry(
    index: int,
    rng: dict,
    src_path: str,
    src_dur: float,
    handles: float,
    codec: str,
) -> dict:
    """Manifest entry for one EDL range (pre-extract; status 'pending')."""
    in_, out = clamp_window(rng["start"], rng["end"], handles, src_dur)
    beat = rng.get("beat") or ""
    return {
        "index": index,
        "filename": clip_filename(index, beat, rng["source"]),
        "source": rng["source"],
        "src_path": src_path,
        "start": rng["start"],
        "end": rng["end"],
        "handle_in": in_,
        "handle_out": out,
        "beat": sanitize_beat(beat),
        "quote": rng.get("quote") or "",
        "hash": clip_hash(src_path, in_, out, codec),
        "duration_s": None,
        "bytes": None,
        "sha256": None,
        "status": "pending",
        "cc_asset_urn": None,
    }


def resolve_source(edl: dict, key: str) -> str:
    """Absolute source path for an EDL range's `source` key."""
    sources = edl.get("sources")
    if not sources:
        raise ValueError("edl has no 'sources' map")
    if key not in sources:
        raise ValueError(f"source {key!r} not in edl 'sources' map")
    return sources[key]


# ── I/O boundary (subprocess + filesystem); integration-tested via a real
#    run against footage/edit/edl.json, not unit mocks. ──


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def probe_duration(path: str) -> float:
    cp = _run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams",
         "-of", "json", path]
    )
    if cp.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {path}: {cp.stderr.strip()}")
    return parse_probe_duration(json.loads(cp.stdout))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_clip(
    src: str, in_: float, out: float, codec: str, out_path: Path
) -> None:
    """Run ffmpeg once; one retry on failure before giving up."""
    cmd = ffmpeg_cmd(src, in_, out, codec, str(out_path))
    for attempt in (1, 2):
        cp = _run(cmd)
        if cp.returncode == 0 and out_path.exists():
            return
        if attempt == 2:
            tail = "\n".join(cp.stderr.strip().splitlines()[-3:])
            raise RuntimeError(f"ffmpeg failed for {out_path.name}: {tail}")
        out_path.unlink(missing_ok=True)


def load_manifest(path: Path) -> dict:
    if path.exists():
        try:
            return json.loads(path.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def process(
    edl: dict,
    edit_dir: Path,
    handles: float,
    codec: str,
    indices: list[int],
) -> dict:
    """Extract the selected ranges; return the manifest dict."""
    clips_dir = edit_dir / "clips_premiere"
    clips_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = clips_dir / "manifest.json"

    prev = {e["index"]: e for e in load_manifest(manifest_path).get("clips", [])}
    ranges = edl.get("ranges", [])
    entries: list[dict] = []
    dur_cache: dict[str, float] = {}
    ok = skipped = failed = 0

    for i in indices:
        rng = ranges[i]
        try:
            src = resolve_source(edl, rng["source"])
            if src not in dur_cache:
                dur_cache[src] = probe_duration(src)
            entry = build_clip_entry(
                i, rng, src, dur_cache[src], handles, codec
            )
        except (ValueError, RuntimeError) as e:
            print(f"  ✗ range {i}: {e}")
            entries.append(
                {"index": i, "source": rng.get("source"),
                 "status": "failed", "error": str(e)}
            )
            failed += 1
            continue

        out_path = clips_dir / entry["filename"]
        if should_skip(prev.get(i), entry["hash"], out_path.exists()):
            e = dict(prev[i])
            entries.append(e)
            skipped += 1
            print(f"  • range {i}: skip (unchanged) {entry['filename']}")
            continue

        try:
            extract_clip(
                src, entry["handle_in"], entry["handle_out"], codec, out_path
            )
            entry["duration_s"] = round(probe_duration(str(out_path)), 3)
            entry["bytes"] = out_path.stat().st_size
            entry["sha256"] = sha256_file(out_path)
            entry["status"] = "ok"
            ok += 1
            print(
                f"  ✓ range {i}: {entry['filename']} "
                f"({entry['duration_s']:.2f}s, "
                f"{entry['bytes'] / 1e6:.1f} MB)"
            )
        except RuntimeError as e:
            print(f"  ✗ range {i}: {e}")
            entry["status"] = "failed"
            entry["error"] = str(e)
            failed += 1
        entries.append(entry)

    manifest = {
        "edl": str((edit_dir / "edl.json").resolve()),
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "handles_s": handles,
        "codec": codec,
        "cc": {
            "root": "VideoStudio",
            "project": None,
            "session_folder": None,
            "folder_urn": None,
        },
        "clips": entries,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(
        f"\n{ok} extracted, {skipped} skipped, {failed} failed → "
        f"{manifest_path}"
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract raw select clips from edl.json for a "
        "Premiere handoff (no fades, no reframe, no grade)."
    )
    ap.add_argument(
        "--edit-dir", required=True,
        help="Session edit dir containing edl.json; outputs go to "
        "<edit-dir>/clips_premiere/.",
    )
    ap.add_argument(
        "--handles", type=float, default=1.0,
        help="Seconds of pre-roll/post-roll on each side (default 1.0).",
    )
    ap.add_argument(
        "--codec", choices=("prores", "h264"), default="prores",
        help="prores = ProRes 422 HQ .mov (default); h264 = smaller files.",
    )
    ap.add_argument(
        "--ranges", default=None,
        help="Comma list of EDL range indices (default: all).",
    )
    args = ap.parse_args(argv)

    edit_dir = Path(args.edit_dir).expanduser().resolve()
    edl_path = edit_dir / "edl.json"
    if not edl_path.exists():
        print(f"error: no edl.json in {edit_dir}", file=sys.stderr)
        return 2
    edl = json.loads(edl_path.read_text())
    n = len(edl.get("ranges", []))
    if n == 0:
        print("error: edl.json has no ranges", file=sys.stderr)
        return 2

    try:
        indices = parse_ranges(args.ranges, n)
    except ValueError as e:
        print(f"error: --ranges: {e}", file=sys.stderr)
        return 2

    print(
        f"cut_clips: {len(indices)} of {n} ranges, codec={args.codec}, "
        f"handles=±{args.handles}s"
    )
    manifest = process(edl, edit_dir, args.handles, args.codec, indices)
    failed = sum(1 for c in manifest["clips"] if c.get("status") == "failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
