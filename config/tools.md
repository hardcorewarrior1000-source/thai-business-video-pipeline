=== TOOLS SETUP ===

This file lists all tools needed for the video production pipeline.
Update this as you set up each tool.

---

## 1. AI Writing (OpenCode — you're here)
- Status: READY
- Used for: Scripts, shot lists, metadata, translations
- Cost: Free tier available

---

## 2. Voice Generation — edge-tts (Microsoft Neural TTS)
- Status: READY (free, no API key needed)
- Engine: Microsoft Edge Neural TTS (same engine as Azure, but free)
- Voice: `th-TH-PremwadeeNeural` (best Thai female voice)
- Used for: Thai text-to-speech narration
- Cost: FREE (uses Microsoft Edge online service)
- Script: `tools/voice-generator.py`

Setup:
1. Install Python 3.10+
2. Install dependency:
   ```
   pip install edge-tts
   ```
3. No API key, no account needed

Usage:
  python tools/voice-generator.py <script.txt> [options]

  Options:
    --output, -o NAME   Output filename (default: voiceover.mp3)
    --split             Generate separate MP3 per paragraph
    --voice NAME        TTS voice (default: th-TH-PremwadeeNeural)
    --rate RATE         Speed adjustment (default: -15%, e.g. +10%, -20%)
    --max-chars N       Max characters per chunk (default: 500)
    --list-voices       List all available Thai voices

  Examples:
    python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt
    python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt --split
    python tools/voice-generator.py output/why-7eleven-dominates-thailand/script.txt --rate=-10%

Output: MP3 format, 24kHz mono

Available Thai voices:
  - th-TH-PremwadeeNeural (female, most natural) — DEFAULT
  - th-TH-NiwatNeural (male)
  - th-TH-AcharaNeural (female)
  - th-TH-KanyaNeural (female)

Notes:
  - Thai speech rate is ~845 chars/min at default rate
  - Use --rate=-15% for slower, more deliberate narration
  - Rate below -20% may cause intermittent failures

---

## 3. Image Generation — Google Flow / ImageFX
- Status: READY (free with Google account)
- Google Flow: https://labs.google/fx/tools/flow (AI filmmaking studio, $19.99/mo for Pro)
- ImageFX: https://labs.google/fx/tools/imagefx (standalone image generator, free)
- Used for: AI-generated illustrations and scene images
- Style: Good for cartoon/illustration with prompting

Usage:
  1. Open Google Flow or ImageFX in browser
  2. Copy prompts from your shot-list.txt
  3. Generate images, download as PNG
  4. Save to: output/[topic-slug]/images/

Tips:
  - Use descriptive prompts: "simple cartoon illustration of a person at a desk, minimal style, 16:9"
  - For consistency, describe the same character appearance across all prompts
  - Google Flow offers scene building and video capabilities
  - ImageFX is free and sufficient for still images

For automation (batch generation):
  - Use the Gemini API with Nano Banana models
  - Model: `gemini-3.1-flash-image` (~$0.039/image)
  - Requires Google Cloud API key

---

## 4. Stick Figure Generator (Backup/Quick Scenes)
- Status: READY
- Location: tools/stickfigure-generator.html
- Used for: Quick stick-figure scenes when AI gen isn't needed
- Features: 12 poses, 7 expressions, 2 characters, props, batch export
- Resolution: 1280×720
- Cost: Free, unlimited

Usage:
  1. Open tools/stickfigure-generator.html in browser
  2. Select preset or build custom scene
  3. Click "Download PNG" or use batch export

---

## 5. Video Editing — CapCut
- Status: SET UP (free account)
- Used for: Assembling images + voiceover + BGM
- Free tier: Sufficient for basic editing
- Tips:
  - Import images by filename (matches timecodes)
  - Layer voiceover on track 1
  - Add BGM on track 2 at -18 to -24 dB

---

## 6. BGM / Sound Effects
- Status: TBD
- Options:
  - YouTube Audio Library (free, safe for copyright)
  - Pixabay Music (free)
  - Epidemic Sound (paid, better quality)
  - Artlist (paid, best for YouTube)

---

## QUICK REFERENCE

| Tool | Account | Status |
|------|---------|--------|
| OpenCode | Active | Ready |
| edge-tts (voice) | None (free) | Ready |
| Google Flow | Google | Ready |
| ImageFX | Google | Ready |
| Stick Figure Tool | Local | Backup |
| CapCut | Free | Ready |

---

## NEED TO SET UP:
- [ ] Pick BGM source
- [ ] Test full pipeline with one video
