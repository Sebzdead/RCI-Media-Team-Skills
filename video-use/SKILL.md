---
name: video-use
description: Edit any video by conversation. Transcribe, brainstorm segments, confirm the cut, extract frame-accurate raw select clips, and hand them off to Premiere Pro via Adobe Creative Cloud. Audio-first reasoning, on-demand visual drill-down. Ask questions, confirm the plan, execute, persist.
---

# Video Use

## Principle

1. **LLM reasons from raw transcript + on-demand visuals.** The only derived
   artifact that earns its keep is a packed phrase-level transcript
   (`takes_packed.md`). Everything else — filler tagging, retake detection, shot
   classification — you derive at decision time.
2. **Audio is primary, visuals follow.** Cut candidates come from speech
   boundaries and silence gaps. Drill into visuals only at decision points.
3. **Ask → confirm → execute → persist.** Before proposing any cut, surface the
   source's strongest material as three concrete segment ideas and let the user
   pick. Never touch the cut until the user has confirmed the strategy in plain
   English.
4. **Generalize.** Do not assume what kind of video this is. Look at the
   material, ask the user, then edit.
5. **You cut; Premiere finishes.** This skill produces *raw select clips* — the
   chosen moments, trimmed frame-accurately with safety handles, nothing baked
   in. Transitions, grade, reframing, titles, music, and the final render happen
   in Premiere Pro. Do not bake decisions the editor needs to own.
6. **Verify your own output before handing it off.** If a clip is wrong, the
   editor inherits the mistake. Check before you declare done.

## Hard Rules (production correctness — non-negotiable)

These produce silent failures or a broken handoff if violated. Memorize them.

1. **Strategy confirmation before execution.** Never extract a clip until the
   user has approved the plain-English plan (the three-ideas gate in step 3).
2. **Surgical precision on word boundaries.** Never cut inside a word. Snap every cut edge exactly to the millisecond-accurate word boundaries (the start timestamp of the first word and the end timestamp of the last word) from the cached Scribe transcript. Never manually pad the `edl.json` ranges with silence or breathing room; let the automated `--handles` manage safety margins. Pacing depends on exact boundaries.
3. **Pad every cut edge with handles.** `cut_clips.py` adds `--handles` seconds (default 1.0) of pre-roll and post-roll on each side so the Premiere editor has trim room and Scribe's 50–100ms timestamp drift is absorbed. Handles are clamped to the source bounds.
4. **Raw selects only — bake nothing.** No audio fades, no reframe crop, no
   color grade in the handoff clips. `edl.json` `target`/`frame`/`grade`/
   `overlays`/`subtitles` are **ignored** by the handoff: reframing and grading
   are the editor's job in Premiere.
5. **Word-level verbatim ASR only.** Never SRT/phrase mode (loses sub-second
   gap data). Never normalized fillers (loses editorial signal).
6. **Cache transcripts per source.** Never re-transcribe unless the source file
   itself changed.
7. **Creative Cloud Files, not Libraries.** Upload clips to CC **Files** storage
   (`asset_create_folders` + block upload). Libraries do not carry raw footage
   into Premiere. One flat folder per session; clips name-sorted = timeline
   order.
8. **Verify before declaring done.** After upload, `asset_search` the
   destination folder and reconcile every clip against `manifest.json`. A clip
   that is missing or size-mismatched is a failed handoff — report it, don't
   claim success.
9. **All session outputs in `<videos_dir>/edit/`.** Never write inside the
   `video-use/` project directory.

Everything else in this document is a worked example. Deviate when the material
calls for it.

## Directory layout

The skill lives in `video-use/`. User footage lives wherever they put it. All
session outputs go into `<videos_dir>/edit/`.

```
<videos_dir>/
├── <source files, untouched>
└── edit/
    ├── project.md                 ← memory; appended every session
    ├── takes_packed.md            ← phrase-level transcripts, the LLM's reading view
    ├── edl.json                   ← cut decisions (source of truth)
    ├── transcripts/<name>.json    ← cached raw Scribe JSON
    ├── clips_premiere/            ← raw select clips for the Premiere handoff
    │   ├── seg_00_HOOK_<src>.mov
    │   ├── seg_01_CLAIM_<src>.mov
    │   └── manifest.json          ← per-clip record; drives upload + idempotent re-runs
    └── verify/                    ← optional debug frames / timeline PNGs
```

The clips also land in Adobe Creative Cloud Files under
`<root>/<project>/<YYYY-MM-DD_segment-title>/`, which the Creative Cloud desktop
app syncs to `~/Creative Cloud Files/...` for import into Premiere.

## Setup

First-time install lives in `install.md` (clone, deps, ffmpeg, skill
registration, API key). On cold start just verify:

- `ELEVENLABS_API_KEY` resolves — in the environment or in `.env` at the
  video-use repo root. If missing, ask the user to paste one and write it to
  `.env` (never to the user's `<videos_dir>`).
- `ffmpeg` + `ffprobe` on PATH. ProRes uses ffmpeg's built-in `prores_ks`.
- Python deps installed (`uv sync` or `pip install -e .` inside the repo).
- **Adobe "Adobe for Creativity" MCP connector** connected and authenticated.
  Verified at runtime by `adobe_mandatory_init` succeeding — if it fails, stop
  and ask the user to connect/authorize the connector (one-time, user action).
- **Creative Cloud desktop app** installed, signed into the same Adobe account,
  with Files sync enabled. Required for clips to reach Premiere. Heuristic
  check: `~/Creative Cloud Files/` exists.
- Node.js / HyperFrames / Remotion are **no longer required** — the interactive
  HyperFrames timeline was removed; the mainline is transcribe → cut → handoff.

## Helpers

Helpers live in `helpers/` next to this SKILL.md (resolve paths relative to the
directory containing this file; the skill is typically symlinked at
`~/.claude/skills/video-use/`).

- **`transcribe.py <video>`** — single-file Scribe call. `--num-speakers N`
  optional. Cached.
- **`transcribe_batch.py <videos_dir>`** — 4-worker parallel transcription. Use
  for multi-take.
- **`pack_transcripts.py --edit-dir <dir>`** — `transcripts/*.json` →
  `takes_packed.md` (phrase-level, break on silence ≥ 0.5s).
- **`timeline_view.py <video> <start> <end>`** — filmstrip + waveform PNG.
  On-demand visual drill-down at decision points. **Not a scan tool.**
- **`cut_clips.py --edit-dir <dir>`** — extract raw select clips from
  `edl.json`. Frame-accurate, handle-padded, no fades/reframe/grade. Writes
  `clips_premiere/seg_NN_<BEAT>_<src>.mov` + `manifest.json`. Flags:
  `--handles <sec>` (default 1.0), `--codec prores|h264` (default `prores` =
  ProRes 422 HQ; `h264` for smaller files), `--ranges 0,2,5` (default all).
  Idempotent: an unchanged clip is skipped on re-run; exits non-zero if any
  range failed.

`render.py`, `grade.py`, `framing.py` remain in `helpers/` for reference but are
**not** part of this pipeline (final render now happens in Premiere).

## The process

1. **Inventory.** `ffprobe` every source. `transcribe_batch.py` on the
   directory. `pack_transcripts.py` to produce `takes_packed.md`. Sample one or
   two `timeline_view`s for a visual first impression.
2. **Pre-scan for problems.** One pass over `takes_packed.md` to note verbal
   slips, mis-speaks, or phrasings to avoid. Plain list, feed into the editor
   brief.
3. **Brainstorm three segment ideas — before any cut.** From `takes_packed.md`,
   find the strongest material and propose **exactly three** distinct ideas,
   each a self-contained segment built around one core idea. For each: a short
   title, the core idea in one line, the hook, the approximate source span(s),
   and one line on why it lands. Present all three and **wait for the user to
   pick one or redirect.** This is Hard Rule 1's gate. Never transcribe-then-cut
   in one move.
4. **Converse (on the chosen idea).** Describe what you see in plain English.
   Ask questions *shaped by the chosen segment*: pacing feel, must-preserve
   moments, must-cut moments, target length. Do not use a fixed checklist.
   (Aspect ratio, grade, and titles are Premiere's job — don't ask about them
   here unless the user volunteers a constraint that affects which takes to
   pick.)
5. **Propose strategy.** 4–8 sentences for the chosen segment: shape, take
   choices, cut direction, length estimate. **Wait for confirmation.**
6. **Execute (draft EDL).** Produce `edl.json` via the editor sub-agent brief,
   scoped to the confirmed segment. Drill into `timeline_view` at ambiguous
   moments. Leave `grade` `""`; do not add `overlays`/`subtitles`/`target` —
   the handoff ignores them.
7. **Extract raw selects.** Confirm `edl.json` is the user-approved cut, then
   run `cut_clips.py --edit-dir <edit>` (add `--handles`/`--codec` if the user
   asked). Read the printed summary. `ffprobe` 1–2 outputs to confirm: codec as
   requested, duration ≈ `(end−start)+2·handles`, frame size **equals the
   source** (proves no reframe crop), audio present. Any range reported
   `failed` → diagnose (usually a bad source path in `edl.json`), fix, re-run
   (unchanged clips are skipped).
8. **Upload to Creative Cloud.** See "Creative Cloud handoff" below:
   `adobe_mandatory_init` → create the session folder → block-upload each clip
   → record the asset URN + status into `manifest.json`.
9. **Verify + Premiere handoff.** `asset_search` (entityScope `CCAsset`,
   `filters.directoryIds=[folder_urn]`); reconcile every clip vs the manifest by
   name and size. Print a per-clip status table. Then print the import
   instructions: the clips appear under
   `~/Creative Cloud Files/<root>/<project>/<session>/` once the Creative Cloud
   desktop app syncs; in Premiere, **File → Import** that folder (or drag it
   in) — name-sort = timeline order. The Premiere import itself is manual and
   not scriptable; stop after confirming the clips are in CC and (best-effort)
   that the synced folder has begun to appear.
10. **Persist.** Append the session to `project.md`, including the CC folder
    path/URN and a pointer to `manifest.json` so re-runs are idempotent and the
    handoff is reproducible.

## Creative Cloud handoff

**Folder hierarchy (flat per session):**
`<root>/<project>/<session_folder>` where `root` defaults to `VideoStudio`,
`project` is the footage directory name (or a user-supplied name), and
`session_folder` is `<YYYY-MM-DD>_<kebab(segment-title)>`. All of a session's
clips go directly in that one folder so a Premiere name-sorted import lands them
in timeline order.

**Upload mechanics:**

1. `adobe_mandatory_init` once (mandatory before any Adobe tool; also the
   auth/connectivity check — failure ⇒ stop, ask the user to connect the
   connector).
2. `asset_create_folders` with `name="<root>/<project>/<session_folder>"`
   (nested in one call). **Capture the returned folder name + URN** — Adobe
   auto-renames on conflict (e.g. `… (1)`), so never assume the requested name.
   Write `cc.project`, `cc.session_folder`, `cc.folder_urn` into the manifest.
3. For each clip with `status:"ok"` in the manifest, skipping any that
   `asset_search` already shows present in the folder with a matching size
   (resumable / idempotent):
   - `asset_initialize_file_upload` with
     `path="<returned folder path>/<filename>"`, `file_size=<bytes>`,
     `media_type="video/quicktime"` (ProRes/`.mov`; `video/mp4` for h264-in-mp4),
     `block_size=52428800` (50 MB — fewest requests for large ProRes). It
     returns a transfer document with presigned block URLs.
   - Push the bytes to the presigned block URLs with `curl` via `Bash`
     (per-block `Content-Range`). The exact transfer-document JSON shape is read
     from the live response on the first run; if a programmatic block PUT can't
     be formed, fall back to the `asset_add_file` interactive picker.
   - `asset_finalize_file_upload` with the returned `filename`, the used
     block/transfer links, `name_conflict_policy="rename"`.
   - Record `cc_asset_urn` and `status:"uploaded"` in the manifest.

**Error handling:** per file — init fail → 1 retry; a block PUT fail → retry
that block ≤3×; finalize fail → 1 retry; persistent failure → mark the clip
`failed` in the manifest, continue the batch, report at the end. Re-runs skip
clips already present in CC. ProRes files are large; the 50 MB blocks +
per-block retry are what make a big-file upload survivable — `--codec h264`
is the smaller-file escape hatch if uploads are too slow.

## Cut craft (techniques)

- **Audio-first.** Candidate cuts from word boundaries and silence gaps.
- **Preserve peaks.** Laughs, punchlines, emphasis beats. Extend past punchlines
  to include reactions — the laugh IS the beat.
- **Speaker handoffs & Word Pacing.** You MUST be surgical and precise: even though
  `--handles` padding exists, the `edl.json` start and end timestamps must align
  exactly with the start and end of the target words' audio boundaries. This ensures
  that when the rough clips are laid back-to-back in Premiere, the pacing of the words
  is tight, natural, and consistent. Do not include trailing/leading silence inside the EDL range.
- **Audio events as signals.** `(laughs)`, `(sighs)`, `(applause)` mark beats.
- **Silence gaps are cut candidates.** ≥400ms are usually cleanest. 150–400ms
  phrase boundaries are usable with a visual check. <150ms is unsafe.
- **Never reason audio and video independently.** Every cut must work on both.

## The packed transcript (primary reading view)

`pack_transcripts.py` reads all `transcripts/*.json` and produces one markdown
file where each take is a list of phrase-level lines prefixed with their
`[start-end]` time range. Phrases break on any silence ≥ 0.5s OR speaker change.
This is the artifact the editor sub-agent reads to pick cuts — word-boundary
precision from text alone at 1/10 the tokens of raw JSON.

Example line:
```
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

## Editor sub-agent brief (for multi-take selection)

When the task is "pick the best take of each beat across many clips," spawn a
dedicated sub-agent with a brief shaped like this. The structure is
load-bearing; the archetype list is not.

```
You are editing a <type> video. Pick the best take of each beat and
assemble them chronologically by beat, not by source clip order.

INPUTS:
  - takes_packed.md (time-annotated phrase-level transcripts of all takes)
  - Product/narrative context: <2 sentences from the user>
  - Speaker(s): <name, role, delivery style note>
  - Expected structure: <pick an archetype or invent one>
  - Verbal slips to avoid: <list from the pre-scan pass>
  - Target runtime: <seconds>

Common structural archetypes (pick, adapt, or invent):
  - Tech launch / demo:   HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA
  - Tutorial:             INTRO → SETUP → STEPS → GOTCHAS → RECAP
  - Interview:            (QUESTION → ANSWER → FOLLOWUP) repeat
  - Travel / event:       ARRIVAL → HIGHLIGHTS → QUIET MOMENTS → DEPARTURE
  - Documentary:          THESIS → EVIDENCE → COUNTERPOINT → CONCLUSION
  - Or invent your own.

RULES:
  - Start/end times must fall on word boundaries from the transcript.
  - Prefer silences ≥ 400ms as cut targets.
  - Unavoidable slips are kept if no better take exists. Note them in "reason".
  - If over budget, revise: drop a beat or trim tails. Report total.

OUTPUT (JSON array, no prose):
  [{"source": "C0103", "start": 2.42, "end": 6.85, "beat": "HOOK",
    "quote": "...", "reason": "..."}, ...]

Return the final EDL and a one-line total runtime check.
```

## EDL format

```json
{
  "version": 1,
  "sources": {"C0103": "/abs/path/C0103.MP4", "C0108": "/abs/path/C0108.MP4"},
  "ranges": [
    {"source": "C0103", "start": 2.42, "end": 6.85,
     "beat": "HOOK", "quote": "...", "reason": "Cleanest delivery."},
    {"source": "C0108", "start": 14.30, "end": 28.90,
     "beat": "SOLUTION", "quote": "...", "reason": "Only take without the false start."}
  ],
  "grade": ""
}
```

`sources` maps EDL keys to **absolute** source paths. Each range's `start`/`end`
are raw source-seconds on word boundaries; `beat` names the editorial moment and
becomes part of the clip filename; `quote`/`reason` are editorial metadata
carried into the manifest. `cut_clips.py` reads only `sources` + `ranges`
(+ optional per-range `beat`/`quote`). Any `grade`, `target`, `frame`,
`overlays`, or `subtitles` keys are **ignored** — those decisions belong to the
Premiere editor.

## Memory — `project.md`

Append one section per session at `<edit>/project.md`:

```markdown
## Session N — YYYY-MM-DD

**Strategy:** one paragraph describing the approach
**Decisions:** take choices, cuts + why
**Handoff:** CC folder path + URN, clip count, manifest path
**Outstanding:** deferred items
```

On startup, read `project.md` if it exists and summarize the last session in one
sentence before asking whether to continue.

## Anti-patterns

- **Baking the edit.** Fades, grade, reframe crop, titles, or music in the
  handoff clips. The editor owns those — ship raw selects.
- **Uploading to CC Libraries.** Libraries don't carry raw footage into
  Premiere. Use Files storage.
- **Declaring success without verifying CC.** Always reconcile the destination
  folder against `manifest.json`.
- **Loose or sloppy EDL boundaries.** Manually padding EDL ranges or not using exact word-boundary timestamps results in bad pacing in the rough-cut timeline. Let the automated handles handle trim room; keep EDL timestamps surgically tight to the speech.
- **Whisper SRT / phrase-level output.** Loses sub-second gap data. Always
  word-level verbatim.
- **Re-transcribing cached sources.** Immutable outputs of immutable inputs.
- **Editing before confirming the strategy.** Never.
- **Assuming what kind of video it is.** Look first, ask second, edit last.
