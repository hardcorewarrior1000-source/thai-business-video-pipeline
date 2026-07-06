"""
ElevenLabs Voice Generator — Video Production Tool
Generates voiceover audio from script files.

SETUP:
1. Install: pip install elevenlabs python-dotenv
2. Create .env file with: ELEVENLABS_API_KEY=your_key_here
3. Run: python tools/voice-generator.py output/why-ai-hallucinates/script.txt

FREE TIER LIMITS:
- 10,000 credits/month (~10 min audio)
- 1 credit = 1 character
- Voice Library voices NOT available via API
- Use Voice Design or default voices instead
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

try:
    from elevenlabs.client import ElevenLabs
except ImportError:
    print("ERROR: elevenlabs not installed. Run: pip install elevenlabs python-dotenv")
    sys.exit(1)

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    print("ERROR: No API key found.")
    print("Create .env file in project root with:")
    print("  ELEVENLABS_API_KEY=your_key_here")
    print("Get your key at: https://elevenlabs.io/app/settings/api-keys")
    sys.exit(1)

client = ElevenLabs(api_key=API_KEY)

# Default voices that work well with Thai
# These are pre-built voices available on all plans
DEFAULT_VOICES = {
    "george": "JBFqnCBsd6RMkjVDRZzb",
    "alice": "Xb7hH8MSUJpSbSDYk0k2",
    "daniel": "onwK4e9ZLuTAKqWW03F9",
}

def get_voices():
    """List available voices."""
    try:
        voices = client.voices.get_all()
        return voices.voices
    except Exception as e:
        print(f"Error fetching voices: {e}")
        return []

def generate_voice(text, voice_id, output_path, model_id="eleven_v3", speed=1.0):
    """Generate audio from text."""
    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format="mp3_44100_128",
            voice_settings={
                "stability": 0.5,
                "similarity_boost": 0.75,
                "speed": speed,
            }
        )
        
        # Save audio
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"Error generating voice: {e}")
        return False

def split_script(text, max_chars=2500):
    """Split script into chunks for API limits."""
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    
    for para in paragraphs:
        if len(current) + len(para) > max_chars:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current += "\n\n" + para if current else para
    
    if current:
        chunks.append(current.strip())
    
    return chunks

def main():
    if len(sys.argv) < 2:
        print("Usage: python voice-generator.py <script.txt> [voice_name] [speed]")
        print("")
        print("Arguments:")
        print("  script.txt   Path to narration script")
        print("  voice_name   Voice to use (default: george)")
        print("               Options: george, alice, daniel, or any voice ID")
        print("  speed        Speaking speed 0.7-1.2 (default: 1.0)")
        print("")
        print("Examples:")
        print("  python voice-generator.py output/why-ai-hallucinates/script.txt")
        print("  python voice-generator.py output/why-ai-hallucinates/script.txt alice")
        print("  python voice-generator.py output/why-ai-hallucinates/script.txt george 0.9")
        sys.exit(1)
    
    script_path = Path(sys.argv[1])
    voice_name = sys.argv[2] if len(sys.argv) > 2 else "george"
    speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        sys.exit(1)
    
    # Resolve voice ID
    voice_id = DEFAULT_VOICES.get(voice_name.lower(), voice_name)
    
    # Read script
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    
    char_count = len(text)
    est_minutes = char_count / 150  # ~150 chars/min for Thai
    
    print(f"Script: {script_path.name}")
    print(f"Characters: {char_count}")
    print(f"Estimated duration: {est_minutes:.1f} minutes")
    print(f"Voice: {voice_name} ({voice_id})")
    print(f"Speed: {speed}x")
    print("")
    
    # Check credit estimate
    print(f"Credits needed: ~{char_count} (1 credit per character)")
    print("")
    
    # Split if needed
    chunks = split_script(text)
    print(f"Split into {len(chunks)} chunk(s) for processing")
    print("")
    
    # Output path
    output_dir = script_path.parent
    output_path = output_dir / "voiceover.mp3"
    
    if len(chunks) == 1:
        # Single chunk — generate directly
        print("Generating audio...")
        if generate_voice(chunks[0], voice_id, output_path, speed=speed):
            print(f"SUCCESS: Saved to {output_path}")
        else:
            print("FAILED: Could not generate audio")
            sys.exit(1)
    else:
        # Multiple chunks — generate and combine
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_path = output_dir / f"voiceover_chunk_{i:02d}.mp3"
            print(f"Generating chunk {i+1}/{len(chunks)}...")
            if generate_voice(chunk, voice_id, chunk_path, speed=speed):
                chunk_files.append(chunk_path)
                print(f"  Saved: {chunk_path.name}")
            else:
                print(f"  FAILED on chunk {i+1}")
                sys.exit(1)
            time.sleep(1)  # Rate limit courtesy
        
        # Combine chunks (simple concatenation)
        print("Combining chunks...")
        with open(output_path, "wb") as outfile:
            for cf in chunk_files:
                with open(cf, "rb") as infile:
                    outfile.write(infile.read())
        
        # Clean up chunk files
        for cf in chunk_files:
            cf.unlink()
        
        print(f"SUCCESS: Saved to {output_path}")
    
    print("")
    print("NEXT STEP: Use this audio with your video editor")
    print(f"  File: {output_path}")

if __name__ == "__main__":
    main()
