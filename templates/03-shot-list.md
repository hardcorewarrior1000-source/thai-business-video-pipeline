=== TEMPLATE: Shot List (Image Production) ===

This template defines how OpenCode generates your shot list.
After you send timestamps, OpenCode follows these rules to create image prompts.

---

## HOW IT WORKS

1. You send timestamps from your voiceover (e.g., [0:00] first line...)
2. OpenCode splits/merges segments to hit 2-3 second shots
3. OpenCode generates shot list with filenames matching timecodes
4. You use the prompts in your image generator

---

## TIMESTAMPS FORMAT (what you send)

```
[0:00] ลองจินตนาการว่าคุณกำลังพิมพ์ข้อความหาเพื่อน
[0:04] คุณพิมพ์ "อรุณสวัสดิ์" แล้วกดส่ง
[0:08] ในเสี้ยววินาทีนั้น ข้อความของคุณเดินทางผ่านสายไฟใต้ทะเล
[0:12] ผ่านดาวเทียม ผ่านศูนย์ข้อมูลที่มีขนาดเท่าสนามฟุตบอล
...
[9:56] โปรดติดตามตอนต่อไป
```

ACCEPTED FORMATS: [M:SS] or [MM:SS] or [H:MM:SS]

---

## SHOT SPLITTING RULES (OpenCode follows these)

Target shot duration: 2.5s (average)
Min shot duration: 2.0s (prevent flicker)
Max shot duration: 3.0s (force change even if no silence)
Silence threshold: 0.25s (change shot if silence + min duration met)

Logic:
- Long segments (>3s) → split into multiple shots
- Short segments (<2s) → merge with next
- Always aim for 2-3 seconds per image

---

## OUTPUT FORMAT

OpenCode generates two things:

### A) TIMECODE MAP (OUTPUT 3)

Table format:

| Timecode | Filename | Text Segment |
|----------|----------|--------------|
| 0:00 | 00_00_00.png | ลองจินตนาการว่าคุณกำลังพิมพ์ข้อความหาเพื่อน |
| 0:02.5 | 00_00_02_5.png | คุณพิมพ์ "อรุณสวัสดิ์" แล้วกดส่ง |
| ... | ... | ... |

### B) SHOT LIST / AGENT BRIEF (OUTPUT 5)

```
═══════════════════════════════════════════════
AGENT BRIEF
═══════════════════════════════════════════════

[STYLE BIBLE]
<visual style DNA — see content-dna.txt>

[CHARACTER LOCK]
<character definitions with @ref tags>

[RULES]
- Keep character appearance IDENTICAL across all shots
- Use the EXACT filename given for each shot
- No text/letters baked into images
- Aspect ratio 16:9 for ALL images
- Apply STYLE BIBLE to every single image

[SHOT LIST]

00_00_00.png SHOT 01 | Chars: @user | Env: simple room, desk with phone | Action: @user sits at desk, looking at phone, neutral expression | Frame: medium shot

00_00_02_5.png SHOT 02 | Chars: @user | Env: same room | Action: @user types on phone, thumbs moving | Frame: close-up on hands and phone

00_00_05.png SHOT 03 | Chars: none | Env: cross-section of earth showing cables under ocean | Action: glowing line travels along cable from left to right | Frame: wide infographic style

... (until all shots)
```

---

## SHOT PROMPT RULES

Each shot must include:
- Filename (matches timecode)
- Characters present (@ref tags or "none")
- Environment/background
- Action/pose
- Frame type (wide/medium/close-up)

Separate fields with |
Separate shots with blank line

Frame types to use:
- wide shot = full scene, context
- medium shot = character from waist up
- close-up = face or hands or detail
- extreme close-up = eye, screen, specific object
- overhead/bird's eye = top-down view
- infographic = data/chart/flow visualization

---

## STYLE BIBLE (auto-included)

The style bible is included in every agent brief:

ART STYLE:
- Hand-drawn 2D doodle cartoon
- Flat colors, bold black outlines
- Slightly imperfect sketchy lines

CHARACTERS:
- Simple stick figures with large circular heads
- Dot eyes, expressive thick brow lines
- Color coding: red = hot/embarrassed, white = neutral, blue = cold/sad

BACKGROUNDS:
- Flat solid color blocks only
- White = default, green strip = ground, blue = sky/outdoor
- ZERO gradients, shadows, textures

ON-SCREEN TEXT:
- Bold ALL CAPS marker font only
- RED, BLACK, or YELLOW colors
- Top of frame

COLOR PALETTE:
- Orange #F5820D, Cobalt #2D5FBF, Green #3A9E3A
- Yellow #F5C518, Red #D94040, Brown #8B5E3C
- Sky blue #6EB5E8, Tan #C4965A, White #FFFFFF

ASPECT RATIO: Always 16:9

---

## SAVED TO

  output/[topic-slug]/shot-list.txt

Contains both timecode map and agent brief.
