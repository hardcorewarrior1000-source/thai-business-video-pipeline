# Video Production Pipeline

Automated workflow for producing long-form Thai business case study YouTube videos.

## Quick Start

```bash
# 1. Install Python 3.10+
# 2. Install edge-tts (Microsoft Neural TTS — free, no API key)
pip install edge-tts

# 3. Generate voiceover from a script
python tools/voice-generator.py output/your-topic/script.txt

# 4. Generate per-paragraph audio files
python tools/voice-generator.py output/your-topic/script.txt --split
```

## Pipeline Overview

| Phase | Tool | Time |
|-------|------|------|
| 1. Topic Selection | OpenCode (this tool) | 2 min |
| 2. Script Writing | OpenCode | 5 min |
| 3. Voice Generation | `tools/voice-generator.py` (edge-tts, free) | 5-15 min |
| 4. Shot List / Timecodes | OpenCode | 5 min |
| 5. Image Generation | Google Flow / ImageFX / Gemini API | 20-30 min |
| 6. Video Editing | CapCut | 30-60 min |
| 7. Metadata & Upload | OpenCode | 5 min |

**Total: ~2 hours per video** (down to ~1 hour with practice)

## Tools

### Voice Generation (edge-tts — Free, Production Quality)
Uses Microsoft Edge Neural TTS engine (same as Azure, but free). Best Thai voice: `th-TH-PremwadeeNeural`.

```bash
python tools/voice-generator.py <script.txt> [options]

Options:
  --output, -o    Custom output filename (default: voiceover.mp3)
  --split         Generate separate MP3 per paragraph
  --voice NAME    TTS voice (default: th-TH-PremwadeeNeural)
  --rate RATE     Speed adjustment (default: -15%, e.g. +10%, -20%)
  --max-chars N   Max characters per chunk (default: 500)
```

### Image Generation
Use Google Flow (`labs.google/fx/tools/flow`) or ImageFX (`labs.google/fx/tools/imagefx`) for AI-generated illustrations. For automation, use the Gemini API with Nano Banana models.

### Stick Figure Generator (Backup)
Open `tools/stickfigure-generator.html` in a browser for quick stick-figure scenes. Supports 12 poses, 7 expressions, batch export at 1280×720.

### Video Editing
CapCut (free) for assembling images + voiceover + BGM.

## Project Structure

```
video-production-pipeline/
├── workflow.md              ← Master workflow guide
├── config/
│   ├── content-dna.txt      ← Voice/tone rules
│   └── tools.md             ← Tool setup guide
├── templates/
│   ├── 01-topic-picker.md   ← Topic selection prompt
│   ├── 02-script-writer.md  ← Script generation prompt
│   ├── 03-shot-list.md      ← Shot list / image prompt template
│   ├── 04-metadata.md       ← SEO metadata template
│   └── 05-translate.md      ← Translation template
├── tools/
│   ├── voice-generator.py   ← Thai TTS (edge-tts, free)
│   └── stickfigure-generator.html  ← Stick figure scene builder (backup)
└── output/
    └── [topic-slug]/
        ├── script.txt       ← Thai narration
        ├── voiceover.mp3    ← Generated audio
        ├── shot-list.txt    ← Image prompts + filenames
        ├── metadata.md      ← Title, desc, tags
        └── images/          ← Generated images
```

## No API Keys Required

The voice generator uses Microsoft edge-tts — free, no API key, no account needed. Image generation via Google Flow/ImageFX is free with a Google account.

## See Also

- `workflow.md` — Full step-by-step production guide
- `config/tools.md` — Detailed tool setup instructions
- `config/content-dna.txt` — Channel voice/tone guidelines
