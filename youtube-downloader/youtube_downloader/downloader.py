import os
import yt_dlp
from typing import Callable, Dict, Any, Optional

def download_video(
    url: str,
    output_dir: str,
    progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None
) -> str:
    """
    Downloads a video from YouTube (or any supported URL) to output_dir.
    Forces maximum 1080p resolution and prefers <= 30fps streams.
    Returns the absolute path to the downloaded file.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Progress hook wrapper to invoke custom callback
    def ytdl_hook(d: Dict[str, Any]):
        if progress_callback:
            progress_callback(d)

    # yt-dlp configuration
    ydl_opts = {
        # Select best video up to 1080p, preferring <= 30fps (the '?' makes it optional if not available)
        # plus the best audio, or fallback to the best combined format under 1080p
        'format': 'bestvideo[height<=1080][fps<=?30]+bestaudio/best[height<=1080][fps<=?30]',
        # We write to a temporary template inside output_dir first
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [ytdl_hook],
        'quiet': True,
        'no_warnings': True,
        'noprogress': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info first to get target filename
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        
        # In case merging happened and extension changed (e.g. mkv/mp4), 
        # let's make sure we find the actual final file on disk
        if not os.path.exists(filename):
            base, _ = os.path.splitext(filename)
            for ext in ['mp4', 'mkv', 'webm', 'mov']:
                test_path = f"{base}.{ext}"
                if os.path.exists(test_path):
                    filename = test_path
                    break
                    
        return os.path.abspath(filename)
