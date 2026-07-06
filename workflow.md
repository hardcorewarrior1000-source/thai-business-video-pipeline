=== VIDEO PRODUCTION WORKFLOW ===

This is your master guide. Follow these steps for every video.

---

## QUICK START (30 seconds)

1. Tell OpenCode: "new video: [your topic]"
2. Pick from 5 angles I give you
3. I write the script → you download it
4. Paste script to ElevenLabs → get MP3
5. Send me timestamps → I make shot list
6. Generate images → edit in CapCut → upload

---

## FULL WORKFLOW

### PHASE 1: Topic Selection (2 min)

YOU SAY:
  "new video: [topic idea]"
  or
  "pick topics for me"

OPENCODE GENERATES:
  → 5 viral angle options in a table

YOU DO:
  → Pick one number (1-5)

---

### PHASE 2: Script Writing (5 min)

OPENCODE GENERATES:
  → Full Thai narration script (1800-2500 words)
  → Saved as: output/[topic-slug]/script.txt

YOU DO:
  → Download the script file
  → Review, suggest edits if needed
  → Confirm final version

---

### PHASE 3: Voice Generation (10-15 min)

YOU DO:
  → Go to elevenlabs.io
  → Paste the script (or upload script.txt)
  → Select your Thai voice
  → Generate audio
  → Download as MP3/WAV
  → Save to: output/[topic-slug]/voiceover.mp3

---

### PHASE 4: Timecode Mapping (5 min)

YOU SAY:
  "timestamps for [topic]:"
  "[0:00] first line of audio..."
  "[0:04] second line..."
  "[0:08] ..."
  (list every segment with its start time)

OPENCODE GENERATES:
  → Timecode map (OUTPUT 3)
  → Shot list with filenames (OUTPUT 5)
  → Saved to: output/[topic-slug]/shot-list.txt

TIP: Listen to your MP3, pause and note timestamps as you go.
     You don't need to be exact — I'll split/merge segments.

---

### PHASE 5: Image Generation (20-30 min)

YOU DO (pick one method):

METHOD A — Stick Figure Generator (free, fast):
  → Open tools/stickfigure-generator.html in browser
  → Enter scene descriptions from shot list
  → Download each image
  → Name them exactly as listed: 00_00_05.png etc.

METHOD B — Gemini/Google Flow:
  → Copy AGENT BRIEF from shot-list.txt
  → Paste into Gemini
  → Generate images one by one or in batch
  → Download and rename to match shot list

METHOD C — Leonardo.ai:
  → Copy prompts from shot list
  → Paste into Leonardo
  → Generate, download, rename

SAVE ALL IMAGES TO: output/[topic-slug]/images/

---

### PHASE 6: Editing (30-60 min)

YOU DO:
  → Open CapCut
  → Import all images from output/[topic-slug]/images/
  → Drag images to timeline in filename order
  → Each image = 2-3 seconds (adjust as needed)
  → Import voiceover.mp3 to audio track
  → Sync images to voice timing
  → Add BGM (music track at -18 to -24 dB)
  → Add transitions (cuts only, except chapter changes)
  → Export video

---

### PHASE 7: Metadata & Upload (5 min)

YOU SAY:
  "seo pack for [topic]"

OPENCODE GENERATES:
  → Title (≤60 chars, clickbait but real)
  → Description (200-300 words + timestamps)
  → Tags (10-15 keywords)
  → Thumbnail concepts (3 options)
  → Saved to: output/[topic-slug]/metadata.md

YOU DO:
  → Upload video to YouTube/TikTok
  → Copy-paste metadata
  → Generate thumbnail (use one of the concepts)
  → Publish!

---

## COMMAND REFERENCE

Say these to OpenCode to trigger each step:

| Command | What I Do |
|---------|-----------|
| `new video: [topic]` | Generate 5 angles for topic |
| `pick number [1-5]` | Write full script for chosen angle |
| `timestamps for [topic]: [data]` | Generate timecode map + shot list |
| `seo pack for [topic]` | Generate title, desc, tags, thumbnail |
| `translate [topic] to english` | Translate script to English |
| `remake shot list` | Regenerate shots with different style |
| `thumbnail prompt for [topic]` | Generate image prompts for thumbnails |

---

## OUTPUT FOLDER STRUCTURE

After each video, your output folder looks like:

```
output/
└── why-ai-hallucinates/
    ├── script.txt           ← Thai narration
    ├── voiceover.mp3        ← Your voice file (you save this)
    ├── shot-list.txt        ← Image prompts + filenames
    ├── metadata.md          ← Title, desc, tags
    ├── images/              ← All generated images
    │   ├── 00_00_00.png
    │   ├── 00_00_02_5.png
    │   ├── 00_00_05.png
    │   └── ...
    └── english/
        └── script.txt       ← Translated version (later)
```

---

## TIPS

- Save everything. You can reuse shots/scripts for future videos.
- Batch your work: record 3-4 voiceovers at once, then generate all images.
- First video will be slow. By video 5, you'll have the rhythm down.
- The stick figure generator is your friend for speed and consistency.
- When in doubt, ask OpenCode: "help me with [step]"

---

## ESTIMATED TIME PER VIDEO

| Phase | Time |
|-------|------|
| Topic + Script | 10 min |
| Voice generation | 15 min |
| Timestamps + Shot list | 10 min |
| Image generation | 30 min |
| Editing | 45 min |
| Metadata + Upload | 10 min |
| **TOTAL** | **~2 hours** |

With practice: down to ~1 hour per video.
