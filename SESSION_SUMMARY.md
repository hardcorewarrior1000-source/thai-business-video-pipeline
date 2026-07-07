# Session Summary — July 7, 2026

## What We Built

Transformed a generic video production pipeline into a fully functional Thai business case study YouTube channel pipeline. First video fully produced end-to-end.

---

## Starting Point

Cloned `hardcorewarrior1000-source/video-production-pipeline` — a skeleton repo with:
- Manual markdown workflow instructions
- Hardcoded ElevenLabs API key (security risk)
- Dead files (capture.js, puppeteer dependency)
- No actual automation

## Ending Point

Fully automated pipeline: **Script → Voiceover → Images → Video** in under 2 hours.

---

## What We Did

### 1. Pipeline Audit & Cleanup
- Deleted `voice-generator.ps1` (hardcoded ElevenLabs API key)
- Deleted `capture.js` (dead weight, 400MB puppeteer dependency)
- Deleted `tools/package.json` + `package-lock.json`
- Deleted duplicate `output/why-ai-hallucinates/script-extension.txt`
- Updated `.env.example`, `.gitignore`

### 2. Niche Selection: วิเคราะห์ธุรกิจไทย (Thai Business Case Studies)
- Researched Thai YouTube landscape
- Identified gap: no Thai channel doing animated business case studies
- Selected format: Kurzgesagt-inspired flat vector illustrations
- CPM potential: $3-8 (business/finance adjacent)

### 3. Voice Generation
- **MMS-TTS** (Facebook): Tested, poor Thai quality, robotic
- **edge-tts** (Microsoft Neural TTS): Winner — free, no API key, production quality
- Voice: `th-TH-PremwadeeNeural`
- Fixed regex bug in voice-generator.py (Thai word boundary matching)
- Output: MP3, ~845 chars/min at -15% rate

### 4. Image Generation
- **Gemini API**: Tested, billing not enabled (quota = 0)
- **Pollinations.ai**: Free, no API key, FLUX model, decent quality
- **Google Flow**: User generates manually for best quality
- Created `tools/image-generator.py` for batch Pollinations.ai generation

### 5. Visual Style: Kurzgesagt-Inspired
- Created `config/visual-style-guide.md`
- Color palette: Deep Navy #1A1A3E, Thai Gold #FFB347, Coral #FF6B6B
- Mascot character: "น้องเค" (Nong K) — golden orange rounded body, dot eyes, tiny glasses
- 10 scene types: Hero, Data, Character, Comparison, Timeline, Map, Framework, Crisis, Success, Echo

### 6. First Video: "ทำไมเซเว่นอีเลฟเว่น ครองประเทศไทยได้"
- **Script**: 6,606 Thai characters, Curiosity Loop narrative structure
- **Voiceover**: 7.8 minutes (470 seconds), 9 chunks
- **Shot list**: 136 shots, ~3.5 seconds average (fast cut style)
- **Images**: 136 Kurzgesagt-style illustrations (user generated via Google Flow)
- **Video**: 31.6 MB, 1280x720, H264+AAC, Ken Burns zoom effect

### 7. Video Assembly
- Created `tools/video-assembler.py`
- Uses ffmpeg (via imageio-ffmpeg)
- Ken Burns zoom effect per image
- Fade in/out on first/last image
- Quality tuning: CRF 18, preset medium, audio 256k

---

## Tools Created

| Tool | Purpose | Status |
|------|---------|--------|
| `tools/voice-generator.py` | Thai TTS via edge-tts | ✅ Working |
| `tools/image-generator.py` | Batch image gen via Pollinations.ai | ✅ Working |
| `tools/video-assembler.py` | Images + voiceover → MP4 | ✅ Working |
| `config/visual-style-guide.md` | Kurzgesagt style guide | ✅ Complete |
| `config/content-dna.txt` | Channel voice/tone rules | ✅ Updated |
| `templates/01-05` | Pipeline prompt templates | ✅ Updated |

---

## Key Decisions

1. **Niche**: Thai business case studies (not tech/AI explainers)
2. **Voice**: edge-tts (free) over ElevenLabs (paid) or MMS-TTS (poor quality)
3. **Images**: Google Flow (manual, high quality) over Pollinations.ai (auto, mid quality)
4. **Style**: Kurzgesagt-inspired flat vector over stick figures
5. **Video**: Fast cut (3.5s avg) over slow pacing

---

## Metrics

- **Total time**: ~8 hours (research, setup, production)
- **First video**: 7.8 min, 136 images, fully produced
- **Cost**: $0 (all free tools)
- **Pipeline speed**: ~2 hours per video (with practice)

---

## Next Steps

1. Upload first video to YouTube
2. Generate thumbnail (prompt in metadata.md)
3. Add BGM from YouTube Audio Library
4. Set up YouTube channel (name, logo, banner, description)
5. Produce second video to validate pipeline consistency

---

## Files in This Repo

```
video-production-pipeline/
├── workflow.md                    ← Master workflow guide
├── config/
│   ├── content-dna.txt            ← Channel voice/tone rules
│   ├── tools.md                   ← Tool setup guide
│   └── visual-style-guide.md      ← Kurzgesagt style system
├── templates/
│   ├── 01-topic-picker.md         ← Topic selection prompt
│   ├── 02-script-writer.md        ← Script generation prompt
│   ├── 03-shot-list.md            ← Shot list template
│   ├── 04-metadata.md             ← SEO metadata template
│   └── 05-translate.md            ← Translation template
├── tools/
│   ├── voice-generator.py         ← Thai TTS (edge-tts)
│   ├── image-generator.py         ← Batch image gen (Pollinations.ai)
│   └── video-assembler.py         ← Images + audio → MP4
└── output/why-7eleven-dominates-thailand/
    ├── script.txt                 ← Thai narration (6,606 chars)
    ├── shot-list.txt              ← 136 shots with timecodes
    ├── google-flow-prompts.txt    ← 136 image generation prompts
    └── metadata.md                ← Title, description, tags, thumbnails
```
