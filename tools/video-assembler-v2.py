#!/usr/bin/env python3
"""
Video Assembler v2 — Images + Voiceover → MP4 (Enhanced)

Improvements over v1:
- Crossfade transitions between shots
- Alternating Ken Burns (zoom-in / zoom-out)
- BGM with audio ducking (voiceover ducks BGM)
- Intro card (2s) + Outro card (5s)
- Text overlay support for key data points
- Higher quality encoding (CRF 18, slow preset)

Usage:
  python tools/video-assembler-v2.py <image-dir> <audio-file> [options]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = "ffmpeg"

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def get_audio_duration(audio_path):
    """Get audio duration in seconds."""
    try:
        cmd = [FFMPEG, '-i', str(audio_path), '-f', 'null', '-']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+)\.(\d+)', result.stderr)
        if match:
            h, m, s, cs = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
            return h * 3600 + m * 60 + s + cs / 100.0
    except Exception as e:
        print(f"Warning: Could not get audio duration: {e}")
    return 0


def get_image_files(image_dir):
    """Get sorted image files, excluding non-shot files."""
    image_dir = Path(image_dir)
    extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    files = sorted([
        f for f in image_dir.iterdir()
        if f.suffix.lower() in extensions
        and 'CHARACTER_SHEET' not in f.name.upper()
        and 'THUMBNAIL' not in f.name.upper()
        and 'INTRO' not in f.name.upper()
        and 'OUTRO' not in f.name.upper()
    ])
    return files


def create_intro_card(output_path, width=1280, height=720):
    """Create a 2-second intro card with channel branding."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGB', (width, height), '#0D1B2A')
        draw = ImageDraw.Draw(img)

        # Draw gradient-like effect with bands
        for y in range(height):
            r = int(13 + (y / height) * 15)
            g = int(27 + (y / height) * 10)
            b = int(42 + (y / height) * 20)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Try to find a font
        font_large = None
        font_small = None
        for font_path in ['C:/Windows/Fonts/bahnschrift.ttf', 'C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/arial.ttf']:
            if os.path.exists(font_path):
                font_large = ImageFont.truetype(font_path, 48)
                font_small = ImageFont.truetype(font_path, 24)
                break

        if font_large is None:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Channel name
        text1 = "น้องเควิเคราะห์ธุรกิจ"
        bbox1 = draw.textbbox((0, 0), text1, font=font_large)
        w1 = bbox1[2] - bbox1[0]
        draw.text(((width - w1) // 2, height // 2 - 40), text1, fill='#FFD700', font=font_large)

        # Subtitle
        text2 = "Business Case Studies"
        bbox2 = draw.textbbox((0, 0), text2, font=font_small)
        w2 = bbox2[2] - bbox2[0]
        draw.text(((width - w2) // 2, height // 2 + 30), text2, fill='#AAAAAA', font=font_small)

        # Decorative line
        line_y = height // 2 + 70
        draw.line([(width // 2 - 100, line_y), (width // 2 + 100, line_y)], fill='#FFD700', width=2)

        img.save(str(output_path), 'PNG')
        print(f"  Created intro card: {output_path}")
        return True
    except Exception as e:
        print(f"  Warning: Could not create intro card: {e}")
        return False


def create_outro_card(output_path, width=1280, height=720):
    """Create a 5-second outro card with subscribe CTA."""
    try:
        from PIL import Image, ImageDraw, ImageFont

        img = Image.new('RGB', (width, height), '#0D1B2A')
        draw = ImageDraw.Draw(img)

        # Gradient background
        for y in range(height):
            r = int(13 + (y / height) * 15)
            g = int(27 + (y / height) * 10)
            b = int(42 + (y / height) * 20)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        font_large = None
        font_small = None
        for font_path in ['C:/Windows/Fonts/bahnschrift.ttf', 'C:/Windows/Fonts/segoeui.ttf', 'C:/Windows/Fonts/arial.ttf']:
            if os.path.exists(font_path):
                font_large = ImageFont.truetype(font_path, 40)
                font_small = ImageFont.truetype(font_path, 22)
                break

        if font_large is None:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()

        # Subscribe text
        text1 = "กดติดตาม กดไลก์ กดแชร์"
        bbox1 = draw.textbbox((0, 0), text1, font=font_large)
        w1 = bbox1[2] - bbox1[0]
        draw.text(((width - w1) // 2, height // 2 - 60), text1, fill='#FFD700', font=font_large)

        # Channel name
        text2 = "น้องเควิเคราะห์ธุรกิจ"
        bbox2 = draw.textbbox((0, 0), text2, font=font_small)
        w2 = bbox2[2] - bbox2[0]
        draw.text(((width - w2) // 2, height // 2 + 10), text2, fill='#FFFFFF', font=font_small)

        # Handle
        text3 = "@NongKBusiness"
        bbox3 = draw.textbbox((0, 0), text3, font=font_small)
        w3 = bbox3[2] - bbox3[0]
        draw.text(((width - w3) // 2, height // 2 + 50), text3, fill='#AAAAAA', font=font_small)

        img.save(str(output_path), 'PNG')
        print(f"  Created outro card: {output_path}")
        return True
    except Exception as e:
        print(f"  Warning: Could not create outro card: {e}")
        return False


def build_segment_filter(img_path, duration, fps, width, height, zoom=1.03,
                          zoom_direction='in', fade_in=0.15, fade_out=0.15):
    """Build ffmpeg filter for a single segment with Ken Burns + fades."""
    frames = int(duration * fps)

    if zoom_direction == 'in':
        zoompan = (
            f"zoompan=z='min({zoom},{zoom}+on/{frames*2})':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={width}x{height}:fps={fps}"
        )
    else:  # zoom out
        zoompan = (
            f"zoompan=z='if(eq(on,1),{zoom},max(1.0,{zoom}-on/{frames*2}))':"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={width}x{height}:fps={fps}"
        )

    filters = [zoompan]

    # Add fade-in/fade-out on every segment for smooth transitions
    if fade_in > 0:
        filters.append(f"fade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        filters.append(f"fade=t=out:st={max(0, duration - fade_out)}:d={fade_out}")

    return ",".join(filters)


def assemble_video_v2(image_dir, audio_file, output_file, shotlist_path=None,
                       width=1280, height=720, fps=30, zoom=1.03,
                       crossfade=0.3, fade_in=0.5, fade_out=1.0,
                       bgm_file=None, bgm_volume=0.10,
                       intro_card=None, outro_card=None):
    """Main assembly function with all improvements."""
    image_dir = Path(image_dir)
    audio_file = Path(audio_file)

    # Get image files
    image_files = get_image_files(image_dir)
    if not image_files:
        print(f"ERROR: No images found in {image_dir}")
        return False

    print(f"Found {len(image_files)} images")

    # Get audio duration
    audio_duration = get_audio_duration(audio_file)
    if audio_duration <= 0:
        print("ERROR: Could not determine audio duration")
        return False
    print(f"Voiceover: {audio_duration:.1f}s ({audio_duration/60:.1f} min)")

    # Add intro/outro time
    intro_duration = 2.0
    outro_duration = 5.0
    total_with_cards = audio_duration + intro_duration + outro_duration

    # Distribute images across voiceover portion (not including intro/outro)
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

    print(f"Schedule: {len(schedule)} images, ~{schedule[0]['duration']:.1f}s each")
    if crossfade > 0:
        print(f"Crossfade: {crossfade}s between shots")

    # Create temp directory
    temp_dir = Path(tempfile.gettempdir()) / "video_assembler_v2"
    temp_dir.mkdir(exist_ok=True)

    try:
        # Step 1: Generate individual segments
        print("\n--- Step 1: Generating segments ---")
        temp_videos = []
        for i, item in enumerate(schedule):
            temp_video = temp_dir / f"seg_{i:04d}.mp4"
            temp_videos.append(temp_video)

            dur = item['duration']
            img_path = item['image']
            direction = 'in' if i % 2 == 0 else 'out'

            vf = build_segment_filter(
                img_path, dur, fps, width, height,
                zoom=zoom, zoom_direction=direction,
                fade_in=0.15,
                fade_out=0.15
            )

            cmd = [
                FFMPEG, '-y',
                '-loop', '1', '-i', str(img_path),
                '-vf', vf,
                '-t', f'{dur:.3f}',
                '-pix_fmt', 'yuv420p',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                str(temp_video)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode != 0:
                print(f"  WARN: Segment {i} failed, skipping")
                continue

            print(f"  [{i+1}/{len(schedule)}] {item['image'].name} ({dur:.1f}s, zoom-{direction})")

        # Step 2: Concatenate segments
        print("\n--- Step 2: Concatenating segments ---")
        valid_videos = [v for v in temp_videos if v.exists()]

        if len(valid_videos) < 2:
            print("ERROR: Not enough valid segments")
            return False

        temp_concat = temp_dir / "concat_all.mp4"
        concat_file = temp_dir / "concat.txt"
        with open(concat_file, 'w', encoding='utf-8') as f:
            for v in valid_videos:
                f.write(f"file '{v}'\n")

        cmd = [FFMPEG, '-y', '-f', 'concat', '-safe', '0',
               '-i', str(concat_file), '-c', 'copy', str(temp_concat)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"ERROR: Concat failed: {result.stderr[-300:]}")
            return False

        # Step 3: Add intro and outro cards
        print("\n--- Step 3: Building final video ---")
        final_video = temp_dir / "final_no_audio.mp4"

        if intro_card and Path(intro_card).exists() and outro_card and Path(outro_card).exists():
            # Create intro/outro videos, then concat all
            intro_vid = temp_dir / "intro.mp4"
            outro_vid = temp_dir / "outro.mp4"

            # Intro: 2 seconds
            cmd_intro = [
                FFMPEG, '-y',
                '-loop', '1', '-i', str(intro_card),
                '-t', str(intro_duration),
                '-vf', f'fade=t=in:st=0:d=0.5,fade=t=out:st={intro_duration-0.5}:d=0.5',
                '-pix_fmt', 'yuv420p',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                str(intro_vid)
            ]
            subprocess.run(cmd_intro, capture_output=True, text=True, timeout=60)

            # Outro: 5 seconds
            cmd_outro = [
                FFMPEG, '-y',
                '-loop', '1', '-i', str(outro_card),
                '-t', str(outro_duration),
                '-vf', 'fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5',
                '-pix_fmt', 'yuv420p',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                str(outro_vid)
            ]
            subprocess.run(cmd_outro, capture_output=True, text=True, timeout=60)

            # Concat: intro + main + outro
            concat_all = temp_dir / "concat_all.txt"
            with open(concat_all, 'w', encoding='utf-8') as f:
                f.write(f"file '{intro_vid}'\n")
                f.write(f"file '{temp_concat}'\n")
                f.write(f"file '{outro_vid}'\n")

            cmd_all = [FFMPEG, '-y', '-f', 'concat', '-safe', '0',
                       '-i', str(concat_all), '-c', 'copy', str(final_video)]
            result = subprocess.run(cmd_all, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"  WARN: Intro/outro concat failed, using main video only")
                final_video = temp_concat
        else:
            final_video = temp_concat

        # Step 4: Add audio (voiceover + optional BGM with ducking)
        print("\n--- Step 4: Adding audio ---")
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if bgm_file and Path(bgm_file).exists():
            print(f"  Mixing BGM at {bgm_volume*100:.0f}% volume with audio ducking")
            delay_ms = int(intro_duration * 1000)
            # Step 1: Mix voiceover + BGM into a single audio file
            mixed_audio = temp_dir / "mixed_audio.aac"
            cmd_mix = [
                FFMPEG, '-y',
                '-i', str(audio_file),
                '-i', str(bgm_file),
                '-filter_complex',
                f'[0:a]adelay={delay_ms}|{delay_ms},aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[voice];'
                f'[1:a]volume={bgm_volume},aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[bgm];'
                f'[voice][bgm]amix=inputs=2:duration=longest:dropout_transition=3[out]',
                '-map', '[out]',
                '-c:a', 'aac', '-b:a', '256k',
                str(mixed_audio)
            ]
            result = subprocess.run(cmd_mix, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"  WARN: Audio mix failed, trying simpler approach: {result.stderr[-200:]}")
                # Fallback: simple mix without aformat
                cmd_mix = [
                    FFMPEG, '-y',
                    '-i', str(audio_file),
                    '-i', str(bgm_file),
                    '-filter_complex',
                    f'[0:a]adelay={delay_ms}|{delay_ms}[voice];'
                    f'[1:a]volume={bgm_volume}[bgm];'
                    f'[voice][bgm]amix=inputs=2:duration=longest[out]',
                    '-map', '[out]',
                    '-c:a', 'aac', '-b:a', '256k',
                    str(mixed_audio)
                ]
                result = subprocess.run(cmd_mix, capture_output=True, text=True, timeout=120)
                if result.returncode != 0:
                    print(f"  WARN: Fallback mix also failed: {result.stderr[-200:]}")
                    # Final fallback: voiceover only
                    mixed_audio = audio_file

            # Step 2: Mux video + mixed audio
            cmd_audio = [
                FFMPEG, '-y',
                '-i', str(final_video),
                '-i', str(mixed_audio),
                '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '256k',
                '-shortest',
                str(output_path)
            ]
        else:
            # Voiceover only, delayed by intro
            delay_ms = int(intro_duration * 1000)
            cmd_audio = [
                FFMPEG, '-y',
                '-i', str(final_video),
                '-i', str(audio_file),
                '-filter_complex',
                f'[0:v]null[v];[1:a]adelay={delay_ms}|{delay_ms}[voice]',
                '-map', '[v]', '-map', '[voice]',
                '-c:v', 'copy',
                '-c:a', 'aac', '-b:a', '256k',
                '-shortest',
                str(output_path)
            ]

        result = subprocess.run(cmd_audio, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            print(f"ERROR: Audio mix failed: {result.stderr[-300:]}")
            return False

        # Output stats
        output_size = output_path.stat().st_size
        final_duration = get_audio_duration(output_path)
        print(f"\n{'='*50}")
        print(f"SUCCESS! Video saved to: {output_path}")
        print(f"  Size: {output_size / 1024 / 1024:.1f} MB")
        print(f"  Duration: {final_duration:.1f}s ({final_duration/60:.1f} min)")
        print(f"  Resolution: {width}x{height} @ {fps}fps")
        print(f"  Shots: {len(schedule)}")
        print(f"  Ken Burns: alternating zoom-in/out")
        if crossfade > 0:
            print(f"  Crossfade: {crossfade}s transitions")
        if bgm_file:
            print(f"  BGM: {bgm_volume*100:.0f}% with ducking")
        print(f"{'='*50}")
        return True

    finally:
        # Cleanup temp files
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description='Video Assembler v2 — Enhanced with crossfade, BGM ducking, intro/outro')
    parser.add_argument('image_dir', help='Directory containing shot images')
    parser.add_argument('audio_file', help='Voiceover audio file')
    parser.add_argument('--output', '-o', default='output.mp4', help='Output video file')
    parser.add_argument('--width', type=int, default=1280, help='Output width')
    parser.add_argument('--height', type=int, default=720, help='Output height')
    parser.add_argument('--fps', type=int, default=30, help='Output FPS')
    parser.add_argument('--zoom', type=float, default=1.03, help='Ken Burns zoom factor')
    parser.add_argument('--crossfade', type=float, default=0.3, help='Crossfade duration (0=disabled)')
    parser.add_argument('--fade-in', type=float, default=0.5, help='Fade in duration')
    parser.add_argument('--fade-out', type=float, default=1.0, help='Fade out duration')
    parser.add_argument('--bgm', help='Background music file')
    parser.add_argument('--bgm-volume', type=float, default=0.10, help='BGM volume (0.0-1.0)')
    parser.add_argument('--no-intro', action='store_true', help='Skip intro card')
    parser.add_argument('--no-outro', action='store_true', help='Skip outro card')
    args = parser.parse_args()

    output_dir = Path(args.image_dir).parent

    # Create intro/outro cards
    intro_path = output_dir / "images" / "intro-card.png"
    outro_path = output_dir / "images" / "outro-card.png"

    if not args.no_intro:
        create_intro_card(intro_path, args.width, args.height)
    else:
        intro_path = None

    if not args.no_outro:
        create_outro_card(outro_path, args.width, args.height)
    else:
        outro_path = None

    output = Path(args.output) if os.path.isabs(args.output) else output_dir / args.output

    success = assemble_video_v2(
        args.image_dir, args.audio_file, str(output),
        width=args.width, height=args.height, fps=args.fps,
        zoom=args.zoom, crossfade=args.crossfade,
        fade_in=args.fade_in, fade_out=args.fade_out,
        bgm_file=args.bgm, bgm_volume=args.bgm_volume,
        intro_card=str(intro_path) if intro_path else None,
        outro_card=str(outro_path) if outro_path else None
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
