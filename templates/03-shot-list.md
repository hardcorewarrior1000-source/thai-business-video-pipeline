=== TEMPLATE: Shot List (Image Production) ===

This template defines how OpenCode generates your shot list.
After you send timestamps, OpenCode follows these rules to create image prompts.

---

## HOW IT WORKS

1. You send timestamps from your voiceover (e.g., [0:00] first line...)
2. OpenCode splits/merges segments to hit 2-3 second shots
3. OpenCode generates shot list with filenames matching timecodes
4. You use the prompts in Google Flow to generate images

---

## VISUAL STYLE: "Thai Business Infographic"

Inspired by: Company Man, MagnatesMedia, Kurzgesagt visual language
This style is UNOCCUPIED in Thai YouTube — massive differentiation opportunity.

### Core Visual DNA:
- **Flat 2D vector illustrations** with bold outlines
- **Animated data visualizations** — charts that build, numbers counting up
- **Clean iconography** — business concepts as simple icons
- **Consistent 4-color palette** across all videos
- **Text overlays** — key quotes, stats, timeline markers
- **No photorealism** — stylized, clean, modern infographic look

### Color Palette (use in EVERY video):
| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary | Deep Blue | #1A3A6B | Headers, key text, backgrounds |
| Accent | Orange | #F5820D | Highlights, CTAs, important numbers |
| Success | Green | #2ECC71 | Growth, positive data, wins |
| Danger | Red | #E74C3C | Decline, failure, warnings |
| Neutral | Dark Gray | #2C3E50 | Body text, secondary elements |
| Background | Light | #F8F9FA | Main backgrounds |
| Background Alt | Warm White | #FFF8F0 | Accent backgrounds |

### Visual Elements Per Scene Type:

| Scene Type | What to Show | Style |
|------------|-------------|-------|
| Company Intro | Logo + building silhouette + founding year | Icon + bold text |
| Financial Data | Bar chart / line graph / pie chart | Animated infographic |
| Timeline | Horizontal timeline with milestone icons | Clean vector |
| Comparison | Split screen A vs B with stats | Side-by-side cards |
| Map/Expansion | Stylized map with dots/arrows showing growth | Flat vector map |
| Quote | Large text card with attribution | Bold typography |
| Framework | SWOT / diagram / flowchart | Clean infographic |
| Crisis | Red-shifted palette, downward arrows, warning icons | Dramatic contrast |
| Success | Green-shifted palette, upward trends, trophy icons | Celebratory |

### Character Style (when people are shown):
- Simplified, semi-realistic illustrations (NOT stick figures)
- Business attire, recognizable poses
- Consistent proportions across all characters
- Face is simplified but recognizable (iconic, not detailed)
- Think: editorial illustration style, like a well-designed business magazine

---

## TIMESTAMPS FORMAT (what you send)

```
[0:00] ลองจินตนาการว่าคุณกำลังยืนอยู่หน้าร้านสะดวกซื้อ
[0:04] คุณเห็นโลโก้สีเขียว-ส้มที่คุณเห็นมาตั้งแต่เด็ก
[0:08] แต่คุณเคยสงสัยไหมว่าทำไมร้านนี้ถึงมีอยู่ทุกมุมถนน
...
[10:05] โปรดติดตามตอนต่อไป
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
- Data-heavy segments → hold on chart/infographic longer (3-4s)

---

## OUTPUT FORMAT

OpenCode generates two things:

### A) TIMECODE MAP (OUTPUT 3)

Table format:

| Timecode | Filename | Text Segment |
|----------|----------|--------------|
| 0:00 | 00_00_00.png | ลองจินตนาการว่าคุณกำลังยืนอยู่หน้าร้านสะดวกซื้อ |
| 0:02.5 | 00_00_02_5.png | คุณเห็นโลโก้สีเขียว-ส้ม |
| ... | ... | ... |

### B) SHOT LIST / AGENT BRIEF (OUTPUT 5)

```
═══════════════════════════════════════════════
AGENT BRIEF
═══════════════════════════════════════════════

[STYLE BIBLE]
<visual style DNA — see style section above>

[CHARACTER LOCK]
<character definitions with @ref tags>

[RULES]
- Keep character appearance IDENTICAL across all shots
- Use the EXACT filename given for each shot
- No text/letters baked into images (text added in post)
- Aspect ratio 16:9 for ALL images
- Apply STYLE BIBLE to every single image
- Infographic style: clean, flat, modern, bold colors

[SHOT LIST]

00_00_00.png SHOT 01 | Type: company-intro | Env: 7-Eleven storefront silhouette | Elements: green-orange logo glow, "1989" founding year text | Frame: wide | Mood: inviting

00_00_02_5.png SHOT 02 | Type: data-card | Env: clean background | Elements: bar chart showing 13,000+ stores in Thailand | Frame: centered infographic | Mood: impressive

00_00_05.png SHOT 03 | Type: timeline | Env: horizontal timeline | Elements: milestone dots from 1989 to 2025, key expansion moments | Frame: wide | Mood: narrative

... (until all shots)
```

---

## SHOT PROMPT RULES

Each shot must include:
- Filename (matches timecode)
- Scene type (company-intro, data-card, timeline, comparison, map, quote, framework, crisis, success, narrator-illustration)
- Environment/background
- Key visual elements
- Frame type (wide/medium/close-up/infographic)
- Mood (inviting, dramatic, impressive, cautionary, celebratory)

Separate fields with |
Separate shots with blank line

Frame types to use:
- wide shot = full scene, context
- medium shot = character from waist up
- close-up = face or hands or detail
- infographic = data/chart/flow visualization (MOST COMMON for this niche)
- split-screen = A vs B comparison

---

## STYLE BIBLE (auto-included)

The style bible is included in every agent brief:

ART STYLE:
- Flat 2D vector illustration, bold outlines
- Infographic/motion graphic aesthetic
- Modern, clean, professional — like a well-designed business magazine
- No photorealism, no 3D, no stick figures

COLOR PALETTE:
- Primary: Deep Blue #1A3A6B
- Accent: Orange #F5820D
- Success: Green #2ECC71
- Danger: Red #E74C3C
- Neutral: Dark Gray #2C3E50
- Background: Light #F8F9FA

TYPOGRAPHY:
- Bold, sans-serif, high contrast
- Key numbers LARGE (revenue, percentages)
- Timeline markers clean and readable

DATA VISUALIZATION:
- Charts: clean, labeled, animated-feel (show growth/decline)
- Icons: simple, consistent stroke weight
- Maps: flat vector, key cities/regions highlighted

ASPECT RATIO: Always 16:9

GOOGLE FLOW PROMPT TEMPLATE:
"Flat 2D infographic illustration, [SCENE DESCRIPTION], bold outline style, [COLOR] accent on [ELEMENT], clean white/light background, business magazine aesthetic, 16:9 aspect ratio, no text, no photorealism"

---

## SAVED TO

  output/[topic-slug]/shot-list.txt

Contains both timecode map and agent brief.
