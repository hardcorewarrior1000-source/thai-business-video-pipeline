=== TOOLS SETUP ===

This file lists all tools needed for the video production pipeline.
Update this as you set up each tool.

---

## 1. AI Writing (OpenCode — you're here)
- Status: READY
- Used for: Scripts, shot lists, metadata, translations
- Cost: Free tier available

---

## 2. Voice Generation — ElevenLabs
- Status: SET UP (free account)
- URL: https://elevenlabs.io
- Used for: Text-to-speech narration
- Free tier: ~10,000 characters/month (~10 min audio)
- API: Available (Python + JavaScript SDKs)
- Script: tools/voice-generator.py

Setup steps:
1. Create account at elevenlabs.io
2. Get API key: https://elevenlabs.io/app/settings/api-keys
3. Install Python package: pip install elevenlabs python-dotenv
4. Create .env file in project root with: ELEVENLABS_API_KEY=your_key
5. Test with: python tools/voice-generator.py output/why-ai-hallucinates/script.txt

API Key: [PASTE YOUR ELEVENLABS API KEY HERE]

Voice options (free tier):
- Default voices: george, alice, daniel (built-in)
- Voice Design: Create custom voices from text description
- Voice Library: NOT available via API on free tier

Usage:
  python tools/voice-generator.py <script.txt> [voice] [speed]
  
  Examples:
    python tools/voice-generator.py output/why-ai-hallucinates/script.txt
    python tools/voice-generator.py output/why-ai-hallucinates/script.txt alice
    python tools/voice-generator.py output/why-ai-hallucinates/script.txt george 0.9

---

## 3. Image Generation — Primary
- Status: NOT YET SET UP
- Options (pick one):

### Option A: Stick Figure Generator (Recommended for start)
- Custom HTML tool built for this project
- Free, unlimited, consistent style
- Location: tools/stickfigure-generator.html
- Use for: All stick-figure character scenes

### Option B: Google Gemini / Flow Agent
- URL: https://gemini.google.com
- Used for: Complex scenes, backgrounds, detailed illustrations
- Gemini Pro plan: Available
- Use for: Scenes that need more than stick figures

### Option C: Leonardo.ai (Fallback)
- URL: https://leonardo.ai
- Free tier: 150 images/day
- Used for: When you need photorealistic or complex art

---

## 4. Video Editing — CapCut
- Status: SET UP (free account)
- Used for: Assembling images + voiceover + BGM
- Free tier: Sufficient for basic editing
- Tips:
  - Import images by filename (matches timecodes)
  - Layer voiceover on track 1
  - Add BGM on track 2 at -18 to -24 dB

---

## 5. BGM / Sound Effects
- Status: TBD
- Options:
  - YouTube Audio Library (free, safe for copyright)
  - Pixabay Music (free)
  - Epidemic Sound (paid, better quality)
  - Artlist (paid, best for YouTube)

---

## QUICK REFERENCE — Your Accounts

| Tool | Account | Status |
|------|---------|--------|
| OpenCode | Active | Ready |
| ElevenLabs | Free | Ready |
| CapCut | Free | Ready |
| Gemini Pro | Available | Ready |
| Leonardo.ai | Not set up | Optional |

---

## NEED TO SET UP:
- [ ] ElevenLabs API key (paste above)
- [ ] Choose primary image generator
- [ ] Pick BGM source
- [ ] Test full pipeline with one video
