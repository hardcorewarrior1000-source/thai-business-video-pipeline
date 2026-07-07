"""
Thai Voice Generator — Video Production Pipeline
Generates Thai voiceover audio from script files using Microsoft Edge Neural TTS.

SETUP:
1. Install Python 3.10+
2. Install dependency: pip install edge-tts
3. No API key needed — uses Microsoft Edge's free TTS service

USAGE:
  python tools/voice-generator.py <script.txt> [options]

Examples:
  python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt
  python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt --split
  python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt --voice th-TH-NiwatNeural
  python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt --rate "-10%"

VOICES:
  th-TH-PremwadeeNeural  — Female (recommended, most natural)
  th-TH-KanyaNeural      — Female
  th-TH-AcharaNeural     — Female
  th-TH-NiwatNeural      — Male

MODEL: Microsoft Edge Neural TTS (via edge-tts)
  - Production-quality neural voices
  - Free, no API key, no usage limits
  - Output: MP3
  - Supports rate/pitch adjustment
"""

import os
import sys
import re
import asyncio
import time
from pathlib import Path

try:
    import edge_tts
except ImportError:
    print("ERROR: Missing dependency. Install with:")
    print("  pip install edge-tts")
    sys.exit(1)

DEFAULT_VOICE = "th-TH-PremwadeeNeural"
DEFAULT_RATE = "+5%"  # Slightly faster for YouTube pacing


def split_script(text: str, max_chars: int = 400) -> list[str]:
    """
    Split script into chunks by paragraph/sentence boundaries.
    Works well with edge-tts which handles longer text better than MMS-TTS.
    """
    # Split by double newline (paragraphs)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    # Further split long paragraphs by Thai sentence endings
    sentences = []
    for para in paragraphs:
        parts = re.split(r'(?:ครับ|ค่ะ|นะคะ|คับ|เนาะ)\s+', para)
        if len(parts) > 1:
            sentences.extend([p.strip() for p in parts if p.strip()])
        else:
            sentences.append(para)

    # Group sentences into chunks under max_chars
    chunks = []
    current = ""
    for sent in sentences:
        if len(current) + len(sent) > max_chars and current:
            chunks.append(current.strip())
            current = sent
        else:
            current = current + " " + sent if current else sent

    if current.strip():
        chunks.append(current.strip())

    return chunks


async def generate_audio(text: str, voice: str, rate: str, output_path: Path, retries: int = 5):
    """Generate audio from text using edge-tts with retry logic."""
    for attempt in range(retries):
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            await communicate.save(str(output_path))
            return
        except Exception as e:
            if attempt < retries - 1:
                wait = (attempt + 1) * 2
                print(f"    Retry {attempt+1}/{retries} after {wait}s: {e}")
                await asyncio.sleep(wait)
            else:
                raise


async def generate_split(chunks: list[str], voice: str, rate: str, output_dir: Path):
    """Generate individual audio files per chunk."""
    durations = []
    for i, chunk in enumerate(chunks):
        chunk_path = output_dir / f"voiceover_{i:02d}.mp3"
        print(f"  [{i+1}/{len(chunks)}] Generating ({len(chunk)} chars)...")
        await generate_audio(chunk, voice, rate, chunk_path)
        # Get file size as rough duration indicator
        size_kb = chunk_path.stat().st_size / 1024
        print(f"    -> {chunk_path.name} ({size_kb:.0f} KB)")
        durations.append(chunk_path)
        # Small delay to avoid rate limiting
        if i < len(chunks) - 1:
            await asyncio.sleep(1)
    return durations


async def generate_combined(chunks: list[str], voice: str, rate: str, output_path: Path):
    """Generate single combined audio file."""
    if len(chunks) == 1:
        print("Generating audio...")
        await generate_audio(chunks[0], voice, rate, output_path)
        size_kb = output_path.stat().st_size / 1024
        print(f"SUCCESS: {output_path.name} ({size_kb:.0f} KB)")
    else:
        # Generate chunks then combine
        import tempfile
        temp_dir = output_path.parent / ".voice_chunks"
        temp_dir.mkdir(exist_ok=True)

        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_path = temp_dir / f"chunk_{i:02d}.mp3"
            print(f"  [{i+1}/{len(chunks)}] Generating ({len(chunk)} chars)...")
            await generate_audio(chunk, voice, rate, chunk_path)
            chunk_files.append(chunk_path)

        # Combine MP3 files using ffmpeg if available, otherwise keep separate
        try:
            import subprocess
            # Create concat list
            list_file = temp_dir / "concat.txt"
            with open(list_file, "w") as f:
                for cf in chunk_files:
                    f.write(f"file '{cf.name}'\n")

            result = subprocess.run(
                ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file), "-c", "copy", str(output_path)],
                capture_output=True, text=True, cwd=str(temp_dir)
            )
            if result.returncode == 0:
                size_kb = output_path.stat().st_size / 1024
                print(f"SUCCESS: {output_path.name} ({size_kb:.0f} KB)")
            else:
                print(f"WARNING: ffmpeg concat failed. Keeping separate chunks.")
                print(f"  Chunks saved to: {temp_dir}")
                return
        except FileNotFoundError:
            print("WARNING: ffmpeg not found. Keeping separate chunks.")
            print(f"  Install ffmpeg to combine: winget install ffmpeg")
            print(f"  Chunks saved to: {temp_dir}")
            return

        # Clean up temp files
        for cf in chunk_files:
            cf.unlink()
        list_file.unlink()
        temp_dir.rmdir()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Thai voiceover from script")
    parser.add_argument("script", help="Path to script .txt file")
    parser.add_argument("--output", "-o", help="Output filename (default: voiceover.mp3)")
    parser.add_argument("--split", action="store_true", help="Generate per-paragraph MP3 files")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Voice name (default: th-TH-PremwadeeNeural)")
    parser.add_argument("--rate", default=DEFAULT_RATE, help="Speech rate (default: +5%%)")
    parser.add_argument("--max-chars", type=int, default=800, help="Max characters per chunk (default: 800)")
    parser.add_argument("--list-voices", action="store_true", help="List available Thai voices")
    args = parser.parse_args()

    if args.list_voices:
        print("Available Thai voices:")
        print("  th-TH-PremwadeeNeural  — Female (recommended)")
        print("  th-TH-KanyaNeural      — Female")
        print("  th-TH-AcharaNeural     — Female")
        print("  th-TH-NiwatNeural      — Male")
        return

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        sys.exit(1)

    # Read script
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("ERROR: Script is empty")
        sys.exit(1)

    char_count = len(text)
    print(f"Script: {script_path.name}")
    print(f"Characters: {char_count}")
    print(f"Voice: {args.voice}")
    print(f"Rate: {args.rate}")
    print()

    # Split into chunks
    chunks = split_script(text, max_chars=args.max_chars)
    print(f"Split into {len(chunks)} chunk(s)")
    print()

    output_dir = script_path.parent

    if args.split:
        asyncio.run(generate_split(chunks, args.voice, args.rate, output_dir))
        print(f"\nSUCCESS: {len(chunks)} MP3 files saved to {output_dir}")
    else:
        output_name = args.output or "voiceover.mp3"
        output_path = output_dir / output_name
        asyncio.run(generate_combined(chunks, args.voice, args.rate, output_path))

    print()
    print("NEXT STEP: Use this audio with your video editor")
    print(f"  Output: {output_dir / (args.output or 'voiceover.mp3')}")


if __name__ == "__main__":
    main()
