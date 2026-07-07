#!/usr/bin/env python3
"""
Image Generator — Pollinations.ai (Free, No API Key)

Batch-generates images from a prompts file using Pollinations.ai.
Uses the FLUX model on their servers — no local GPU needed.

Usage:
  python tools/image-generator.py <prompts-file> [options]

Options:
  --output-dir, -o DIR   Output directory (default: images/ in same folder as prompts)
  --width W              Image width (default: 1280)
  --height H             Image height (default: 720)
  --delay SECONDS        Delay between requests (default: 16)
  --start N              Start from shot N (default: 1)
  --end N                Stop at shot N (default: all)
  --retry N              Max retries per image (default: 3)
  --seed BASE            Base seed for reproducibility (default: 42)

Examples:
  python tools/image-generator.py output/why-7eleven-dominates-thailand/google-flow-prompts.txt
  python tools/image-generator.py output/why-7eleven-dominates-thailand/google-flow-prompts.txt --start 1 --end 10
  python tools/image-generator.py output/why-7eleven-dominates-thailand/google-flow-prompts.txt --delay 20
"""

import argparse
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# Fix Windows console encoding for Thai/emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def parse_prompts_file(filepath):
    """Parse the prompts file and extract shot info."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    shots = []
    # Pattern: SHOT XX — filename.png — description\nprompt text
    pattern = re.compile(
        r'SHOT\s+(\d+)\s+—\s+(\S+)\s+—\s+(.+?)\n(.+?)(?=\n\n|\n═══|\Z)',
        re.DOTALL
    )

    for match in pattern.finditer(content):
        shot_num = int(match.group(1))
        filename = match.group(2).strip()
        description = match.group(3).strip()
        prompt = match.group(4).strip()

        shots.append({
            'num': shot_num,
            'filename': filename,
            'description': description,
            'prompt': prompt,
        })

    return shots


def generate_image(prompt, output_path, width=1280, height=720, seed=42, max_retries=3):
    """Generate a single image via Pollinations.ai."""
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true"

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=120)
            data = response.read()

            if len(data) < 1000:
                raise ValueError(f"Image too small ({len(data)} bytes) — likely an error")

            with open(output_path, 'wb') as f:
                f.write(data)

            return True, len(data)

        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 5
                print(f"    Retry {attempt + 1}/{max_retries} after {wait}s: {e}")
                time.sleep(wait)
            else:
                return False, str(e)

    return False, "Max retries exceeded"


def main():
    parser = argparse.ArgumentParser(description='Batch image generator using Pollinations.ai')
    parser.add_argument('prompts_file', help='Path to prompts file')
    parser.add_argument('--output-dir', '-o', help='Output directory')
    parser.add_argument('--width', type=int, default=1280, help='Image width (default: 1280)')
    parser.add_argument('--height', type=int, default=720, help='Image height (default: 720)')
    parser.add_argument('--delay', type=float, default=16, help='Delay between requests in seconds (default: 16)')
    parser.add_argument('--start', type=int, default=1, help='Start from shot N (default: 1)')
    parser.add_argument('--end', type=int, default=999, help='Stop at shot N (default: all)')
    parser.add_argument('--retry', type=int, default=3, help='Max retries per image (default: 3)')
    parser.add_argument('--seed', type=int, default=42, help='Base seed (default: 42)')
    args = parser.parse_args()

    # Parse prompts
    print(f"Reading prompts from: {args.prompts_file}")
    shots = parse_prompts_file(args.prompts_file)
    print(f"Found {len(shots)} shots")

    # Filter by range
    shots = [s for s in shots if args.start <= s['num'] <= args.end]
    print(f"Generating shots {shots[0]['num']} to {shots[-1]['num']} ({len(shots)} images)")
    print(f"Resolution: {args.width}x{args.height}")
    print(f"Delay: {args.delay}s between requests")
    print()

    # Output directory
    if args.output_dir:
        out_dir = Path(args.output_dir)
    else:
        out_dir = Path(args.prompts_file).parent / "images"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output: {out_dir}")
    print()

    # Generate images
    success = 0
    failed = 0
    skipped = 0
    start_time = time.time()

    for i, shot in enumerate(shots):
        outpath = out_dir / shot['filename']

        # Skip if already exists
        if outpath.exists() and outpath.stat().st_size > 1000:
            print(f"[{i+1}/{len(shots)}] SKIP {shot['filename']} (exists)")
            skipped += 1
            continue

        print(f"[{i+1}/{len(shots)}] {shot['filename']} — {shot['description']}")
        print(f"  Prompt: {shot['prompt'][:80]}...")

        ok, result = generate_image(
            shot['prompt'], str(outpath),
            width=args.width, height=args.height,
            seed=args.seed + shot['num'],
            max_retries=args.retry
        )

        if ok:
            print(f"  ✓ Saved ({result} bytes)")
            success += 1
        else:
            print(f"  ✗ FAILED: {result}")
            failed += 1

        # Rate limit — wait between requests (except after last image)
        if i < len(shots) - 1:
            time.sleep(args.delay)

    # Summary
    elapsed = time.time() - start_time
    print()
    print("=" * 50)
    print(f"DONE in {elapsed:.0f}s ({elapsed/60:.1f} min)")
    print(f"  Success: {success}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed:  {failed}")
    print(f"  Output:  {out_dir}")


if __name__ == '__main__':
    main()
