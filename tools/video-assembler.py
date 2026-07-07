#!/usr/bin/env python3
"""
Video Assembler — Images + Voiceover → MP4

Creates a video from a sequence of images timed to voiceover audio.
Uses ffmpeg (via imageio-ffmpeg) for encoding.

Usage:
  python tools/video-assembler.py <image-dir> <audio-file> [options]

Options:
  --output, -o FILE      Output video file (default: output.mp4)
  --timecodes FILE       Timecodes file (default: auto-detect from shot-list)
  --transition SEC       Crossfade duration (default: 0.3)
  --fps FPS              Output FPS (default: 30)
  --width W              Output width (default: 1280)
  --height H             Output height (default: 720)
  --zoom ZOOM            Ken Burns zoom factor (default: 1.03)
  --fade-in SEC          Fade in duration (default: 0.5)
  --fade-out SEC         Fade out duration (default: 1.0)
  --bgm FILE             Background music file (optional)
  --bgm-volume VOL       BGM volume 0.0-1.0 (default: 0.1)

Examples:
  python tools/video-assembler.py output/why-7eleven-dominates-thailand/images output/why-7eleven-dominates-thailand/voiceover_combined.mp3
  python tools/video-assembler.py output/why-7eleven-dominates-thailand/images output/why-7eleven-dominates-thailand/voiceover_combined.mp3 --zoom 1.05 --transition 0.5
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Find ffmpeg
try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = "ffmpeg"

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def get_audio_duration(audio_path):
    """Get audio duration in seconds using ffprobe."""
    try:
        cmd = [
            FFMPEG, '-i', str(audio_path),
            '-show_entries', 'format=duration',
            '-v', 'quiet', '-of', 'csv=p=0'
        ]
        # Use ffprobe equivalent via ffmpeg
        cmd_probe = [
            FFMPEG.replace('ffmpeg', 'ffprobe').replace('.exe', '-probe.exe') if 'imageio_ffmpeg' in str(FFMPEG) else 'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_path)
        ]
        # Fallback: use ffmpeg to get duration
        cmd_ff = [
            FFMPEG, '-i', str(audio_path),
            '-f', 'null', '-'
        ]
        result = subprocess.run(cmd_ff, capture_output=True, text=True, timeout=30)
        # Parse duration from stderr
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+)\.(\d+)', result.stderr)
        if match:
            h, m, s, cs = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
            return h * 3600 + m * 60 + s + cs / 100.0
    except Exception as e:
        print(f"Warning: Could not get audio duration: {e}")
    return 0


def parse_timecodes_from_shotlist(shotlist_path):
    """Extract timecodes from shot-list.txt file."""
    timecodes = []
    with open(shotlist_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match patterns like "00:01:23" or "01:23" or "[00:01:23]"
    pattern = re.compile(r'(\d{1,2}):(\d{2}):(\d{2})')
    for match in pattern.finditer(content):
        h, m, s = int(match.group(1)), int(match.group(2)), int(match.group(3))
        timecodes.append(h * 3600 + m * 60 + s)

    # Also try MM:SS format
    pattern2 = re.compile(r'(?<!:)(\d{1,2}):(\d{2})(?!\d)')
    for match in pattern2.finditer(content):
        m, s = int(match.group(1)), int(match.group(2))
        tc = m * 60 + s
        if tc not in timecodes:
            timecodes.append(tc)

    timecodes.sort()
    return timecodes


def distribute_images_evenly(image_files, audio_duration):
    """Distribute images evenly across the audio duration."""
    if not image_files or audio_duration <= 0:
        return []

    interval = audio_duration / len(image_files)
    schedule = []
    for i, img in enumerate(image_files):
        start = i * interval
        end = (i + 1) * interval if i < len(image_files) - 1 else audio_duration
        schedule.append({
            'image': img,
            'start': start,
            'end': end,
            'duration': end - start
        })
    return schedule


def build_filter_complex(schedule, width, height, zoom=1.03, fade_in=0.5, fade_out=1.0):
    """Build ffmpeg filter_complex for image sequence with Ken Burns effect."""
    filters = []
    inputs = []

    for i, item in enumerate(schedule):
        dur = item['duration']
        zoom_speed = 1.0 / (dur * 25)  # Smooth zoom over duration

        # Ken Burns: slow zoom in
        z = zoom
        zoompan_filter = (
            f"zoompan=z='min({z},{z}+on*{zoom_speed})':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={int(dur * 30)}:s={width}x{height}:fps=30"
        )
        filters.append(zoompan_filter)

        # Fade in on first image
        if i == 0 and fade_in > 0:
            filters.append(f"fade=t=in:st=0:d={fade_in}")

        # Fade out on last image
        if i == len(schedule) - 1 and fade_out > 0:
            filters.append(f"fade=t=out:st={max(0, dur - fade_out)}:d={fade_out}")

        inputs.append(f"[{i}:v]")

    return filters, inputs


def assemble_video(image_dir, audio_file, output_file, shotlist_path=None,
                   width=1280, height=720, fps=30, zoom=1.03,
                   fade_in=0.5, fade_out=1.0, bgm_file=None, bgm_volume=0.1):
    """Main assembly function."""
    image_dir = Path(image_dir)
    audio_file = Path(audio_file)

    # Get image files (sorted), excluding character sheets and non-shot files
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    exclude_patterns = {'CHARACTER_SHEET', 'character_sheet', 'thumbnail'}
    image_files = sorted([
        f for f in image_dir.iterdir()
        if f.suffix.lower() in image_extensions
        and not any(p in f.name.upper() for p in exclude_patterns)
    ])

    if not image_files:
        print(f"ERROR: No images found in {image_dir}")
        return False

    print(f"Found {len(image_files)} images in {image_dir}")

    # Get audio duration
    audio_duration = get_audio_duration(audio_file)
    if audio_duration <= 0:
        print("ERROR: Could not determine audio duration")
        return False
    print(f"Audio duration: {audio_duration:.1f}s ({audio_duration/60:.1f} min)")

    # Try to parse timecodes from shot list
    if shotlist_path and Path(shotlist_path).exists():
        timecodes = parse_timecodes_from_shotlist(shotlist_path)
        if timecodes:
            print(f"Found {len(timecodes)} timecodes from shot list")

    # Distribute images evenly across audio
    schedule = distribute_images_evenly(image_files, audio_duration)
    print(f"Schedule: {len(schedule)} images, ~{schedule[0]['duration']:.1f}s each")

    # Build ffmpeg command
    print("Building video...")

    # Create concat file for ffmpeg
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as concat_file:
        concat_path = concat_file.name

    try:
        # Generate individual image videos with Ken Burns effect
        temp_videos = []
        for i, item in enumerate(schedule):
            temp_video = Path(tempfile.gettempdir()) / f"segment_{i:04d}.mp4"
            temp_videos.append(temp_video)

            dur = item['duration']
            img_path = item['image']

            # Ken Burns zoom filter
            zoompan = (
                f"zoompan=z='min({zoom},{zoom}+on/{int(dur*30)*2})':"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d={int(dur * fps)}:s={width}x{height}:fps={fps}"
            )

            # Add fade effects
            fade_filters = []
            if i == 0 and fade_in > 0:
                fade_filters.append(f"fade=t=in:st=0:d={fade_in}")
            if i == len(schedule) - 1 and fade_out > 0:
                fade_filters.append(f"fade=t=out:st={max(0, dur - fade_out)}:d={fade_out}")

            vf = zoompan
            if fade_filters:
                vf += "," + ",".join(fade_filters)

            cmd = [
                FFMPEG, '-y',
                '-loop', '1', '-i', str(img_path),
                '-vf', vf,
                '-t', f'{dur:.3f}',
                '-pix_fmt', 'yuv420p',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                str(temp_video)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"  WARNING: Segment {i} failed: {result.stderr[-200:]}")
                continue

            print(f"  Segment {i+1}/{len(schedule)}: {item['image'].name} ({dur:.1f}s)")

        # Write concat file
        with open(concat_path, 'w', encoding='utf-8') as f:
            for tv in temp_videos:
                if tv.exists():
                    f.write(f"file '{tv}'\n")

        # Concatenate all segments
        print("Concatenating segments...")
        temp_concat = Path(tempfile.gettempdir()) / "concat_video.mp4"
        cmd_concat = [
            FFMPEG, '-y',
            '-f', 'concat', '-safe', '0',
            '-i', concat_path,
            '-c', 'copy',
            str(temp_concat)
        ]
        result = subprocess.run(cmd_concat, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"ERROR: Concat failed: {result.stderr[-300:]}")
            return False

        # Add audio
        print("Adding audio...")
        cmd_audio = [
            FFMPEG, '-y',
            '-i', str(temp_concat),
            '-i', str(audio_file),
            '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', '256k',
            '-shortest',
        ]

        # Add BGM if provided
        if bgm_file and Path(bgm_file).exists():
            cmd_audio.extend(['-i', str(bgm_file)])
            # Mix audio: voiceover at full volume, BGM at reduced volume
            cmd_audio.extend([
                '-filter_complex',
                f'[1:a]volume=1.0[voice];[2:a]volume={bgm_volume}[bgm];[voice][bgm]amix=inputs=2:duration=shortest[out]',
                '-map', '0:v', '-map', '[out]'
            ])

        cmd_audio.append(str(output_file))
        result = subprocess.run(cmd_audio, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"ERROR: Audio mux failed: {result.stderr[-300:]}")
            return False

        # Get output file size
        output_size = Path(output_file).stat().st_size
        print()
        print(f"SUCCESS! Video saved to: {output_file}")
        print(f"  Size: {output_size / 1024 / 1024:.1f} MB")
        print(f"  Duration: ~{audio_duration:.1f}s")
        return True

    finally:
        # Cleanup temp files
        os.unlink(concat_path)
        for tv in temp_videos:
            if tv.exists():
                tv.unlink()
        temp_concat_path = Path(tempfile.gettempdir()) / "concat_video.mp4"
        if temp_concat_path.exists():
            temp_concat_path.unlink()


def main():
    parser = argparse.ArgumentParser(description='Assemble images + voiceover into MP4 video')
    parser.add_argument('image_dir', help='Directory containing images')
    parser.add_argument('audio_file', help='Voiceover audio file')
    parser.add_argument('--output', '-o', default='output.mp4', help='Output video file')
    parser.add_argument('--timecodes', help='Timecodes file (shot-list.txt)')
    parser.add_argument('--transition', type=float, default=0.3, help='Transition duration')
    parser.add_argument('--fps', type=int, default=30, help='Output FPS')
    parser.add_argument('--width', type=int, default=1280, help='Output width')
    parser.add_argument('--height', type=int, default=720, help='Output height')
    parser.add_argument('--zoom', type=float, default=1.03, help='Ken Burns zoom factor')
    parser.add_argument('--fade-in', type=float, default=0.5, help='Fade in duration')
    parser.add_argument('--fade-out', type=float, default=1.0, help='Fade out duration')
    parser.add_argument('--bgm', help='Background music file')
    parser.add_argument('--bgm-volume', type=float, default=0.1, help='BGM volume (0.0-1.0)')
    args = parser.parse_args()

    output = Path(args.image_dir).parent / args.output if not os.path.isabs(args.output) else Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    success = assemble_video(
        args.image_dir, args.audio_file, str(output),
        shotlist_path=args.timecodes,
        width=args.width, height=args.height, fps=args.fps,
        zoom=args.zoom, fade_in=args.fade_in, fade_out=args.fade_out,
        bgm_file=args.bgm, bgm_volume=args.bgm_volume
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
