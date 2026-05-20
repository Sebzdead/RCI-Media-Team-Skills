# YouTube Downloader & Transcoder CLI

A premium command-line utility to download YouTube videos (or other web streams) and automatically transcode them into high-quality, editor-friendly formats:
- **Low Resolution (<= 720p):** Transcoded to **H.264 video** and **AAC audio** in a standard `.mp4` container.
- **High Resolution (> 720p, max 1080p):** Transcoded to **ProRes 422 Standard video** and uncompressed **PCM 16-bit audio** in a `.mov` container.
- **Framerate Capped:** Downsamples high-framerate clips (e.g. 60fps) to **30fps** for optimal consistency in sourcing.

Built on top of `yt-dlp` and `ffmpeg`, with a beautiful CLI dashboard powered by `rich`.

---

## 🛠 Prerequisites

This tool requires `ffmpeg` and `ffprobe` to be installed on your system.

On macOS, you can install them using Homebrew:
```bash
brew install ffmpeg
```

---

## 🚀 Quick Start (Running via `uv`)

The project is built to use `uv` for seamless dependency management and instant execution.

### Option A: Run directly without installation
Navigate to the project folder and run the command directly. `uv` will automatically download the dependencies and execute the tool in an isolated, cached virtual environment:
```bash
cd youtube-downloader
uv run yt-download "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Option B: Install globally in your environment
If you want to install the tool into your active Python or Conda environment so the `yt-download` executable is available globally from any directory:
```bash
cd youtube-downloader
uv pip install -e .
```
Now, the `yt-download` command will be globally available in your environment:
```bash
yt-download "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## ⚙️ Options & Customization

```
usage: yt-download [-h] [-o OUTPUT_DIR] [--force-transcode] [-t THRESHOLD] [-c {h264,prores}] url

Download and transcode YouTube videos to editor-friendly formats.

positional arguments:
  url                   YouTube video URL to download

options:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory to save the final video (default: current directory)
  -t THRESHOLD, --threshold THRESHOLD
                        Height threshold (in pixels) for H.264 vs ProRes (default: 720)
  -c {h264,prores}, --codec {h264,prores}
                        Force a specific codec overriding the resolution threshold
  --force-transcode     Force transcode even if downloaded format matches requirements
```

### Examples

1. **Auto-download (low res goes to H.264 mp4, high res to ProRes mov):**
   ```bash
   yt-download "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

2. **Download and save to a specific directory:**
   ```bash
   yt-download -o ~/Desktop/Footage "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

3. **Force a specific codec (e.g., download a 360p video but convert it to ProRes):**
   ```bash
   yt-download --codec prores "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```

4. **Change the threshold to 480p (only videos > 480p become ProRes):**
   ```bash
   yt-download --threshold 480 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
   ```
