#!/usr/bin/env python3
"""
Create YouTube Shorts from long-form video assets.
Extracts audio segments, crops images to 9:16, assembles vertical videos.
"""

import os
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
        import re
        match = re.search(r'Duration:\s*(\d+):(\d+):(\d+)\.(\d+)', result.stderr)
        if match:
            h, m, s, cs = int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4))
            return h * 3600 + m * 60 + s + cs / 100.0
    except:
        pass
    return 0


def extract_audio_segment(audio_file, start_sec, duration_sec, output_file):
    """Extract a segment from audio file."""
    cmd = [
        FFMPEG, '-y',
        '-i', str(audio_file),
        '-ss', f'{start_sec:.2f}',
        '-t', f'{duration_sec:.2f}',
        '-c:a', 'libmp3lame', '-b:a', '192k',
        str(output_file)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return result.returncode == 0


def crop_image_vertical(input_img, output_img, target_w=1080, target_h=1920):
    """Crop/resize image to 9:16 vertical format (center crop)."""
    cmd = [
        FFMPEG, '-y',
        '-i', str(input_img),
        '-vf', f'scale={target_w}:{target_h}:force_original_aspect_ratio=increase,crop={target_w}:{target_h}',
        str(output_img)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.returncode == 0


def create_short(image_dir, audio_file, output_file, image_list, audio_start, audio_duration,
                  width=1080, height=1920, fps=30, zoom=1.05):
    """Create a single Short video."""
    image_dir = Path(image_dir)
    temp_dir = Path(tempfile.gettempdir()) / "shorts_temp"
    temp_dir.mkdir(exist_ok=True)

    try:
        # Step 1: Extract audio segment
        audio_seg = temp_dir / "audio_seg.mp3"
        print(f"  Extracting audio: {audio_start:.1f}s - {audio_start + audio_duration:.1f}s")
        if not extract_audio_segment(audio_file, audio_start, audio_duration, audio_seg):
            print("  ERROR: Audio extraction failed")
            return False

        # Step 2: Prepare vertical images
        vert_dir = temp_dir / "vertical"
        vert_dir.mkdir(exist_ok=True)

        print(f"  Preparing {len(image_list)} vertical images...")
        for i, img_name in enumerate(image_list):
            src = image_dir / img_name
            dst = vert_dir / f"v_{i:03d}.png"
            if src.exists():
                crop_image_vertical(src, dst, width, height)
            else:
                print(f"  WARNING: Missing image {img_name}")

        # Step 3: Distribute images across audio duration
        vert_images = sorted([f for f in vert_dir.iterdir() if f.suffix == '.png'])
        if not vert_images:
            print("  ERROR: No vertical images")
            return False

        interval = audio_duration / len(vert_images)
        temp_videos = []

        for i, img in enumerate(vert_images):
            seg_dur = interval
            temp_video = temp_dir / f"seg_{i:03d}.mp4"
            temp_videos.append(temp_video)

            # Ken Burns zoom
            frames = int(seg_dur * fps)
            zoompan = (
                f"zoompan=z='min({zoom},{zoom}+on/{frames*2})':"
                f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                f"d={frames}:s={width}x{height}:fps={fps}"
            )

            # Add fade in/out
            fade_in = 0.1
            fade_out = 0.1
            vf = f"{zoompan},fade=t=in:st=0:d={fade_in},fade=t=out:st={max(0, seg_dur - fade_out)}:d={fade_out}"

            cmd = [
                FFMPEG, '-y',
                '-loop', '1', '-i', str(img),
                '-vf', vf,
                '-t', f'{seg_dur:.3f}',
                '-pix_fmt', 'yuv420p',
                '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
                str(temp_video)
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode != 0:
                print(f"  WARNING: Segment {i} failed")

        # Step 4: Concatenate segments
        valid_videos = [v for v in temp_videos if v.exists()]
        concat_file = temp_dir / "concat.txt"
        with open(concat_file, 'w', encoding='utf-8') as f:
            for v in valid_videos:
                f.write(f"file '{v}'\n")

        temp_concat = temp_dir / "concat.mp4"
        cmd = [FFMPEG, '-y', '-f', 'concat', '-safe', '0',
               '-i', str(concat_file), '-c', 'copy', str(temp_concat)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

        # Step 5: Add audio
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            FFMPEG, '-y',
            '-i', str(temp_concat),
            '-i', str(audio_seg),
            '-c:v', 'copy',
            '-c:a', 'aac', '-b:a', '192k',
            '-shortest',
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            size = output_path.stat().st_size
            dur = get_audio_duration(output_path)
            print(f"  SUCCESS: {output_path.name} ({dur:.1f}s, {size/1024/1024:.1f} MB)")
            return True
        else:
            print(f"  ERROR: Audio mux failed")
            return False

    finally:
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    base = Path(r"C:\Users\sambo\Downloads\OC\thai-business-video-pipeline\output\why-bigc-lost-to-7eleven")
    image_dir = base / "images"
    audio_file = base / "voiceover.mp3"
    output_dir = base / "shorts"
    output_dir.mkdir(exist_ok=True)

    # Define 3 Shorts
    shorts = [
        {
            "name": "short-1-168-vs-15430",
            "title": "168 vs 15,430 สาขา — ทำไมบิ๊กซีแพ้?",
            "audio_start": 102.0,  # ~1:42 in voiceover
            "audio_duration": 25.0,
            "images": [
                "data-01.png", "data-02.png", "data-03.png", "data-04.png",
                "data-05.png", "data-06.png", "data-07.png", "data-08.png"
            ]
        },
        {
            "name": "short-2-chicken-farm",
            "title": "ไก่ข้าวมันไก่เซเว่น... CP Group เป็นคนเลี้ยง",
            "audio_start": 189.0,  # ~3:09 in voiceover
            "audio_duration": 18.0,
            "images": [
                "franchise-08.png", "franchise-09.png", "franchise-10.png",
                "franchise-11.png"
            ]
        },
        {
            "name": "short-3-business-model",
            "title": "บิ๊กซีออกแบบมาให้มาสัปดาห์ละครั้ง",
            "audio_start": 381.0,  # ~6:21 in voiceover
            "audio_duration": 33.0,
            "images": [
                "conclusion-01.png", "conclusion-02.png", "conclusion-03.png",
                "conclusion-04.png", "conclusion-05.png", "conclusion-06.png",
                "conclusion-07.png", "conclusion-08.png"
            ]
        }
    ]

    print("=" * 50)
    print("CREATING 3 YOUTUBE SHORTS")
    print("=" * 50)

    for short in shorts:
        print(f"\n--- {short['name']} ---")
        print(f"  Title: {short['title']}")
        output_file = output_dir / f"{short['name']}.mp4"
        create_short(
            image_dir, audio_file, output_file,
            short['images'], short['audio_start'], short['audio_duration'],
            width=1080, height=1920, fps=30, zoom=1.05
        )

    print("\n" + "=" * 50)
    print("ALL SHORTS CREATED!")
    print("=" * 50)


if __name__ == '__main__':
    main()
