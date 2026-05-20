import os
import subprocess
import json
import re
from typing import Dict, Any, Optional, Callable

def get_video_info(file_path: str) -> Dict[str, Any]:
    """
    Runs ffprobe to retrieve metadata about the video, including resolution,
    framerate, duration, and codecs.
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffprobe failed: {e.stderr}") from e

def parse_fps(fps_str: str) -> float:
    """
    Parses frame rate strings from ffprobe (e.g. '30/1' or '2997/100') into a float.
    """
    try:
        if '/' in fps_str:
            num, den = fps_str.split('/')
            return float(num) / float(den)
        return float(fps_str)
    except (ValueError, ZeroDivisionError, AttributeError, TypeError):
        return 0.0

def analyze_video(file_path: str) -> Dict[str, Any]:
    """
    Analyzes the video file and returns a structured summary of its properties.
    """
    info = get_video_info(file_path)
    
    # Extract format level info
    format_info = info.get('format', {})
    duration = float(format_info.get('duration', 0.0))
    format_name = format_info.get('format_name', '')
    
    # Find video and audio streams
    video_stream = None
    audio_stream = None
    
    for stream in info.get('streams', []):
        codec_type = stream.get('codec_type')
        if codec_type == 'video' and not video_stream:
            video_stream = stream
        elif codec_type == 'audio' and not audio_stream:
            audio_stream = stream

    if not video_stream:
        raise ValueError("No video stream found in the downloaded file.")
        
    width = int(video_stream.get('width', 0))
    height = int(video_stream.get('height', 0))
    video_codec = video_stream.get('codec_name', '')
    fps = parse_fps(video_stream.get('r_frame_rate') or video_stream.get('avg_frame_rate'))
    
    audio_codec = audio_stream.get('codec_name', '') if audio_stream else 'none'
    
    return {
        'width': width,
        'height': height,
        'fps': fps,
        'video_codec': video_codec,
        'audio_codec': audio_codec,
        'duration': duration,
        'format': format_name
    }

def transcode_video(
    input_path: str,
    output_path: str,
    target_format: str,  # 'h264' or 'prores'
    source_info: Dict[str, Any],
    progress_callback: Optional[Callable[[float], None]] = None
) -> None:
    """
    Transcodes input_path to output_path using ffmpeg, matching the target_format spec:
    - 'h264': H.264 video (libx264, yuv420p) + AAC audio in .mp4
    - 'prores': ProRes 422 Standard (prores_ks, profile 2) + PCM audio (pcm_s16le) in .mov
    Restricts frame rate to max 30 fps using video filters.
    """
    # Build ffmpeg command
    cmd = ['ffmpeg', '-y', '-i', input_path]
    
    # Video filters list
    vf_filters = []
    
    # Downsample framerate if it exceeds 30 fps
    if source_info['fps'] > 30.5:
        vf_filters.append('fps=fps=30')
        
    # Configure codecs based on target format
    if target_format == 'h264':
        cmd.extend([
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'medium',
            '-crf', '22',
            '-c:a', 'aac',
            '-b:a', '192k'
        ])
    elif target_format == 'prores':
        cmd.extend([
            '-c:v', 'prores_ks',
            '-profile:v', '2',  # 2 = ProRes 422 Standard
            '-vendor', 'ap10',
            '-pix_fmt', 'yuv422p10le',
            '-c:a', 'pcm_s16le'
        ])
    else:
        raise ValueError(f"Unknown target format: {target_format}")
        
    # Apply video filters if any
    if vf_filters:
        cmd.extend(['-vf', ','.join(vf_filters)])
        
    # Use -progress to output machine-readable statistics for progress bar
    cmd.extend([
        '-progress', '-',
        '-nostats',
        output_path
    ])
    
    # Start ffmpeg process
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Read progress updates
    duration = source_info['duration']
    
    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            
            # Look for out_time_us key-value pair
            if line.startswith('out_time_us='):
                try:
                    us = int(line.split('=')[1].strip())
                    current_time = us / 1_000_000.0
                    if duration > 0:
                        percentage = min(100.0, (current_time / duration) * 100.0)
                        if progress_callback:
                            progress_callback(percentage)
                except (ValueError, IndexError):
                    pass
                    
        process.wait()
        if process.returncode != 0:
            stderr_output = process.stderr.read()
            raise RuntimeError(f"ffmpeg transcoding failed with exit code {process.returncode}: {stderr_output}")
            
    except Exception as e:
        process.kill()
        raise e
