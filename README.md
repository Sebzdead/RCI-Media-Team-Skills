# 🎬 RCI Media Team — Workflows, Skills & Tools

Welcome to the central repository for the **Revolutionary Communist International (RCI) Media Team**. 

This repository serves as a shared hub for automation workflows, AI coding assistant skills, design systems, and custom utilities. Our goal is to streamline, automate, and standardize our media production and video editing workflows—covering everything from visual design to footage sourcing and encoding.

---

## 📂 Repository Structure

The repository is organized into four primary areas:

```
RCI Media Team Skills/
├── Design System/                  # 🎨 Brand guidelines, typography, textures, and UI templates
├── Video Essay Script Drafter/     # 📝 Workspace-scoped YouTube video essay scripting skill
├── footage-sourcer/                # 🔍 AI-assisted footage sourcing and credit logging skill
└── youtube-downloader/             # 📥 CLI tool to download and transcode media for editors
```

---

## 🎨 1. Design System

The [Design System](./Design%20System) folder contains the visual guidelines, brand fonts, textures, and templates that define the RCI Media identity. It is built to ensure a professional, serious, and revolutionary visual presence across all platforms (Instagram, YouTube, Podcasts, and internal presentations).

### Key Features
* **Brand Colors:** Strict palette utilizing RCI Red (`#da0d10`), Alarm Red (`#e6002b`), Off-white paper (`#f6efef`), and Ink (`#222222`).
* **Typography:** Pre-configured font stacks using display faces like **Built Titling** and **Trade Gothic Next LT Pro**.
* **Textures:** Over 70 web-ready paper, film grain, and grunge textures to give media a tactile, hand-printed press aesthetic.
* **UI Templates:** Pre-designed templates for Instagram (posts and stories), YouTube (thumbnails and title cards), and presentation slides.

### How to Use
1. **Web prototyping:** Link the pre-configured [colors_and_type.css](./Design%20System/colors_and_type.css) stylesheet to any HTML file:
   ```html
   <link rel="stylesheet" href="Design System/colors_and_type.css">
   ```
2. **Aesthetic Rules:** 
   * Headlines should be in **ALL CAPS** using the display face.
   * Always overlay a low-opacity texture (e.g. paper or film grain) over flat backgrounds and photos.
   * No emojis, soft shadows, or rounded corners larger than 4px.
   * Refer to the [Design System README](./Design%20System/README.md) for full design standards.

---

## 🔍 2. Footage Sourcer

The [Footage Sourcer](./footage-sourcer) directory contains the `footage-sourcer` workspace-scoped agent skill. This helps researchers and video editors locate open-licensed historical and current events footage, verify licensing terms, and maintain a credit manifest.

### Key Features
* **AI Sourcing Agent:** Formulates optimal search queries for historical archives (like the Library of Congress or Wikimedia Commons).
* **Licensing Guardrails:** Automatically checks assets against open licensing profiles (Public Domain, CC0, CC BY).
* **Automated Credit Logging:** Appends sourced assets directly to a central manifest file.

### How to Use
1. **Via Antigravity Chat:** If you are using an AI coding assistant in this workspace, you can trigger the skill using the `/footage-sourcer` command:
   ```
   /footage-sourcer Search for historical clips of the 1919 Seattle General Strike
   ```
2. **Manual Script Execution:** Run the Python script to log manually sourced assets directly to the central manifest:
   ```bash
   python3 footage-sourcer/.agent/skills/footage-sourcer/scripts/log_credits.py "[Source Name]" "[URL]" "[Licensing Profile]"
   ```
   Sourced assets will accumulate in [credits_manifest.txt](./footage-sourcer/credits_manifest.txt).

---

## 📥 3. YouTube Downloader

The [YouTube Downloader](./youtube-downloader) directory contains a CLI application built in Python that downloads videos or audio from YouTube (or other streaming platforms supported by `yt-dlp`) and automatically transcodes them into editor-friendly formats.

### Key Features
* **Resolution-based Transcoding:**
  * **≤ 720p:** Transcoded to **H.264 video** & **AAC audio** (`.mp4` container).
  * **> 720p (up to 1080p):** Transcoded to **ProRes 422 Standard video** & uncompressed **16-bit PCM audio** (`.mov` container).
* **Framerate Capping:** Automatically downsamples high-framerate clips (e.g., 60fps) to **30fps** for timeline consistency.
* **Rich Dashboard:** Features a terminal UI dashboard to display download progress and transcoding status.

### How to Use
The tool is set up to run instantly using `uv`:

1. Navigate to the directory:
   ```bash
   cd youtube-downloader
   ```
2. Run the tool using `uv` (it will automatically handle environment setup and dependencies):
   ```bash
   uv run yt-download "https://www.youtube.com/watch?v=VIDEO_ID"
   ```
3. For full options, run:
   ```bash
   uv run yt-download --help
   ```
   *(See [YouTube Downloader README](./youtube-downloader/README.md) for full commands and installation options).*

---

## 📝 4. Video Essay Script Drafter

The [Video Essay Script Drafter](./Video%20Essay%20Script%20Drafter) directory contains the `youtube-video-essay-script` workspace-scoped agent skill. This helps writers and editors adapt text essays, articles, and outlines into a production-ready YouTube video essay script.

### Key Features
* **Spoken-Prose Adaptation:** Rewrites written prose specifically "for the ear," prioritizing natural conversational flow, pacing, and verbal signposting.
* **Directorial Cue Layering:** Automatically generates specific, actionable visual/footage cues `[V]`, on-screen graphics `[G]`, and music `[M]` to support the narration.
* **Strict Message Faithfulness:** Adheres to the "Prime Directive" of preserving the source material's flow, vocabulary, argument, and political message without softening or neutralizing it.
* **Punch-Up Humour:** Adds sharp, deadpan, and dry humour targeting powerful entities and figures, while ensuring it never punches down at ordinary or marginalized people.
* **Runtime Calibration:** Targets standard video essay runtimes of 20–30 minutes (~3,000–4,500 spoken words at 150 wpm) and outputs runtime estimates.
* **Built-in Fact Checking:** Appends a production notes section listing facts, statistics, recent events, and quotes to verify before filming.

### How to Use
1. **Via an AI coding assistant:** If you are using an AI coding assistant in this workspace, this skill is pre-configured. You can trigger it during a chat by asking it to adapt text for a video essay or outline:
   ```
   Turn this article into a 25-minute YouTube video essay script: [article text or file link]
   ```
   Alternatively, trigger it explicitly by prompting the assistant to use the `youtube-video-essay-script` skill.

2. **Via Claude (Web/Projects):** You can also use this skill natively in Claude. Simply upload the `youtube-video-essay-script.skill` file (or unzip it and upload the `SKILL.md` and `references/example_script.md` files) to a Claude Project's knowledge base or directly to a chat session, and instruct Claude to follow the provided guidelines to write your script.

---

## 🤝 Sharing & Contribution

Since this repository is managed with Git:
* **Workspace Skills:** The `footage-sourcer` and `youtube-video-essay-script` agent skills are version-controlled inside the repository. When a teammate clones or pulls the repository and opens it in an AI coding assistant, the editor will automatically register the skills.
* **Adding New Tools:** When adding new utilities, ensure they are self-contained in their own directory, include a setup/run guide (preferring modern lightweight tools like `uv` or standard npm commands), and follow the RCI Media visual identity.
