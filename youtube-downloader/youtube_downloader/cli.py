import os
import sys
import argparse
import shutil
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

from youtube_downloader.downloader import download_video
from youtube_downloader.transcoder import analyze_video, transcode_video

console = Console()

def check_dependencies() -> None:
    """
    Checks that ffmpeg and ffprobe are installed and available on PATH.
    """
    ffmpeg_exists = shutil.which("ffmpeg") is not None
    ffprobe_exists = shutil.which("ffprobe") is not None
    
    if not ffmpeg_exists or not ffprobe_exists:
        console.print("[bold red]Dependency Error:[/bold red]")
        if not ffmpeg_exists:
            console.print(" - [yellow]ffmpeg[/yellow] was not found on your system PATH.")
        if not ffprobe_exists:
            console.print(" - [yellow]ffprobe[/yellow] was not found on your system PATH.")
        console.print("\nPlease install ffmpeg via Homebrew or your package manager:")
        console.print("  [bold cyan]brew install ffmpeg[/bold cyan]\n")
        sys.exit(1)

def display_header() -> None:
    """
    Renders a premium visual header for the CLI tool.
    """
    console.print(
        Panel(
            "[bold white]🎥 YouTube Download & Transcode CLI[/bold white]\n"
            "[dim]Downloads up to 1080p30. Autoconverts: <=720p to H.264 (MP4) | >720p to ProRes 422 Standard (MOV)[/dim]",
            border_style="bold blue",
            expand=False
        )
    )

def main() -> None:
    # 1. Parse arguments
    parser = argparse.ArgumentParser(
        description="Download and transcode YouTube videos to editor-friendly formats."
    )
    parser.add_argument("url", help="YouTube video URL to download")
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Directory to save the final video (default: current directory)"
    )
    parser.add_argument(
        "--force-transcode",
        action="store_true",
        help="Force transcode even if downloaded format matches requirements"
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=720,
        help="Height threshold (in pixels) for H.264 vs ProRes (default: 720)"
    )
    parser.add_argument(
        "-c", "--codec",
        choices=["h264", "prores"],
        help="Force a specific codec overriding the resolution threshold"
    )
    
    args = parser.parse_args()
    
    # 2. Check system tools
    check_dependencies()
    
    # 3. Print Header
    display_header()
    
    output_dir = os.path.abspath(args.output_dir)
    
    # 4. Download Video
    downloaded_path = None
    try:
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            download_task = progress.add_task("Downloading video...", total=100)
            
            def progress_callback(d: Dict[str, Any]):
                if d['status'] == 'downloading':
                    total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                    downloaded = d.get('downloaded_bytes', 0)
                    if total > 0:
                        progress.update(download_task, total=total, completed=downloaded)
                    else:
                        progress.update(download_task, completed=downloaded)
                elif d['status'] == 'finished':
                    progress.update(download_task, description="Download complete!")
            
            downloaded_path = download_video(args.url, output_dir, progress_callback)
            
    except Exception as e:
        console.print(f"\n[bold red]Download Failed:[/bold red] {e}")
        sys.exit(1)
        
    if not downloaded_path or not os.path.exists(downloaded_path):
        console.print("\n[bold red]Error:[/bold red] Download completed but output file could not be found.")
        sys.exit(1)
        
    # 5. Analyze Downloaded File
    console.print("\n[bold blue]🔍 Analyzing file metadata...[/bold blue]")
    try:
        source_info = analyze_video(downloaded_path)
    except Exception as e:
        console.print(f"[bold red]Metadata analysis failed:[/bold red] {e}")
        sys.exit(1)
        
    # Show metadata table
    table = Table(title="Downloaded File Metadata", show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Filename", os.path.basename(downloaded_path))
    table.add_row("Resolution", f"{source_info['width']}x{source_info['height']}")
    table.add_row("Framerate", f"{source_info['fps']:.2f} fps")
    table.add_row("Video Codec", source_info['video_codec'])
    table.add_row("Audio Codec", source_info['audio_codec'])
    table.add_row("Duration", f"{source_info['duration']:.2f} seconds")
    console.print(table)
    
    # 6. Determine target format and file path
    height = source_info['height']
    if args.codec:
        target_format = args.codec
    else:
        target_format = 'h264' if height <= args.threshold else 'prores'
        
    ext = '.mp4' if target_format == 'h264' else '.mov'
    
    base_name = os.path.splitext(os.path.basename(downloaded_path))[0]
    final_output_path = os.path.join(output_dir, f"{base_name}{ext}")
    
    # 7. Check if transcoding is required
    skip_transcode = False
    
    # We can skip if target codecs match, framerate <= 30, container matches, and no force flag
    current_ext = os.path.splitext(downloaded_path)[1].lower()
    
    if not args.force_transcode:
        codec_matches = False
        if target_format == 'h264':
            codec_matches = (source_info['video_codec'] == 'h264' and 
                             current_ext == '.mp4' and
                             source_info['audio_codec'] in ['aac', 'mp3'])
        elif target_format == 'prores':
            codec_matches = ('prores' in source_info['video_codec'].lower() and 
                             current_ext == '.mov')
            
        fps_matches = source_info['fps'] <= 30.5
        
        if codec_matches and fps_matches:
            skip_transcode = True

    if skip_transcode:
        console.print(f"\n[bold green]✓[/bold green] Video already meets requirements ({target_format.upper()} at <= 30fps). Skipping transcoding.")
        if downloaded_path != final_output_path:
            shutil.move(downloaded_path, final_output_path)
        console.print(Panel(f"[bold green]Success![/bold green]\nOutput saved to: [cyan]{final_output_path}[/cyan]", border_style="green"))
        return

    # 8. Transcode Video
    codec_label = "H.264 (.mp4)" if target_format == 'h264' else "ProRes 422 Standard (.mov)"
    fps_label = "30 fps (capped)" if source_info['fps'] > 30.5 else f"{source_info['fps']:.2f} fps"
    
    console.print(f"\n[bold yellow]⚙ Transcoding video to {codec_label} @ {fps_label}...[/bold yellow]")
    
    # Set up temp transcode path ending with target extension so ffmpeg selects correct muxer
    temp_transcode_path = os.path.join(output_dir, f"{base_name}.transcoding{ext}")
    
    try:
        with Progress(
            TextColumn("[bold green]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:
            transcode_task = progress.add_task("Transcoding...", total=100)
            
            def transcode_callback(pct: float):
                progress.update(transcode_task, completed=pct)
                
            transcode_video(
                downloaded_path,
                temp_transcode_path,
                target_format,
                source_info,
                transcode_callback
            )
            
        # Clean up downloaded file if it's different from our target output path
        if downloaded_path != final_output_path and os.path.exists(downloaded_path):
            os.remove(downloaded_path)
            
        # Rename tmp output to final destination
        if os.path.exists(final_output_path):
            os.remove(final_output_path)
        os.rename(temp_transcode_path, final_output_path)
        
        # Verify the transcoded file
        final_info = analyze_video(final_output_path)
        
        console.print(
            Panel(
                f"[bold green]🎉 Transcoding Completed Successfully![/bold green]\n\n"
                f"• [bold]Output File:[/bold] [cyan]{final_output_path}[/cyan]\n"
                f"• [bold]Format:[/bold] {codec_label}\n"
                f"• [bold]Resolution:[/bold] {final_info['width']}x{final_info['height']}\n"
                f"• [bold]Framerate:[/bold] {final_info['fps']:.2f} fps\n"
                f"• [bold]File Size:[/bold] {os.path.getsize(final_output_path) / (1024*1024):.2f} MB",
                border_style="green"
            )
        )
        
    except Exception as e:
        console.print(f"\n[bold red]Transcoding Failed:[/bold red] {e}")
        # Clean up temp file on failure
        if os.path.exists(temp_transcode_path):
            os.remove(temp_transcode_path)
        sys.exit(1)

if __name__ == "__main__":
    main()
