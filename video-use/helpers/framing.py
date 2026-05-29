"""Shared crop/reframe math — the single source of truth for vertical reframing.

Both `render.py` (final ffmpeg crop) and `edl_to_hyperframes.py` (Studio
preview CSS) import this. Because the geometry is computed here once, the
HyperFrames preview the user frames against and the rendered output are
identical by construction — they cannot drift.

Model: a horizontal source (SW×SH) is reframed into a target canvas (TW×TH,
e.g. 1080×1920 vertical) by taking a target-aspect crop rectangle out of the
source and scaling it up to fill the canvas.

Per-range `frame` (all normalized, source-space, sensible defaults):
  x      horizontal center of the crop in the source, 0..1   (default 0.5)
  y      vertical center of the crop in the source,   0..1   (default 0.5)
  scale  zoom: 1.0 = the largest target-aspect crop that fits the source
         (for 16:9→9:16 that's the full source height); >1 punches in tighter
         (default 1.0)

The speaker is often off-center in a podcast frame — `x` is the control the
user adjusts ("speaker's on the left in clip 3" → lower x).
"""

from __future__ import annotations

DEFAULT_FRAME = {"x": 0.5, "y": 0.5, "scale": 1.0}


def parse_target(target: str | None) -> tuple[int, int] | None:
    """"1080x1920" -> (1080, 1920). None/blank -> None (legacy passthrough)."""
    if not target:
        return None
    try:
        w, h = target.lower().split("x")
        return int(w), int(h)
    except (ValueError, AttributeError):
        return None


def normalize_frame(frame: dict | None) -> dict:
    """Fill missing keys with centered defaults; clamp to valid ranges."""
    f = dict(DEFAULT_FRAME)
    if frame:
        for k in ("x", "y", "scale"):
            if k in frame and frame[k] is not None:
                f[k] = float(frame[k])
    f["x"] = min(1.0, max(0.0, f["x"]))
    f["y"] = min(1.0, max(0.0, f["y"]))
    f["scale"] = max(1.0, f["scale"])
    return f


def compute_crop(
    sw: int, sh: int, tw: int, th: int, frame: dict | None
) -> tuple[int, int, int, int]:
    """Return the integer crop rectangle (cw, ch, cx, cy) taken from the
    source, which — scaled to (tw, th) — is the reframed output.

    The crop has the target aspect ratio. `scale` shrinks it (zoom in);
    `x`/`y` position its center, clamped so it stays inside the source.
    """
    f = normalize_frame(frame)
    ar_t = tw / th

    if sw / sh >= ar_t:
        # Source is wider than target (16:9 → 9:16): height-bound.
        ch = sh / f["scale"]
        cw = ch * ar_t
    else:
        # Source is taller/narrower than target: width-bound.
        cw = sw / f["scale"]
        ch = cw / ar_t

    cw = min(cw, float(sw))
    ch = min(ch, float(sh))

    cx = f["x"] * sw - cw / 2.0
    cy = f["y"] * sh - ch / 2.0
    cx = min(max(cx, 0.0), sw - cw)
    cy = min(max(cy, 0.0), sh - ch)

    # Even integers — ffmpeg crop + yuv420p scaling want mod-2 dimensions.
    cw_i = max(2, int(round(cw / 2)) * 2)
    ch_i = max(2, int(round(ch / 2)) * 2)
    cx_i = max(0, min(int(round(cx)), sw - cw_i))
    cy_i = max(0, min(int(round(cy)), sh - ch_i))
    return cw_i, ch_i, cx_i, cy_i


def ffmpeg_reframe_filter(sw: int, sh: int, tw: int, th: int, frame: dict | None) -> str:
    """The `crop=...,scale=...` chain for one segment's -vf."""
    cw, ch, cx, cy = compute_crop(sw, sh, tw, th, frame)
    return f"crop={cw}:{ch}:{cx}:{cy},scale={tw}:{th}"


def css_box(
    sw: int, sh: int, tw: int, th: int, frame: dict | None
) -> dict[str, float]:
    """Inner-<video> geometry for the Studio preview wrapper.

    The wrapper is the TW×TH canvas with overflow:hidden. The full source is
    rendered at (sw*f × sh*f) and shifted by (-cx*f, -cy*f) so the visible
    window is exactly the crop rectangle scaled to the canvas — pixel-for-
    pixel the same region ffmpeg_reframe_filter() crops.
    """
    cw, ch, cx, cy = compute_crop(sw, sh, tw, th, frame)
    f = tw / cw  # crop → canvas zoom (== th / ch, aspect preserved)
    return {
        "width": sw * f,
        "height": sh * f,
        "left": -cx * f,
        "top": -cy * f,
    }
