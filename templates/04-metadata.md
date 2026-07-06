=== TEMPLATE: Metadata & Thumbnail ===

This template defines how OpenCode generates your YouTube/TikTok metadata.
Say "seo pack for [topic]" and I follow these rules.

---

## WHAT OPENCODE GENERATES

### 1. Title (≤60 characters)
- Clickbait but deliverable
- Thai language
- Include curiosity gap or number
- Examples:
  - "ทำไม AI ชอบโกหก? ความจริงที่น่าตกใจ"
  - "สิ่งที่ Google รู้เกี่ยวกับคุณมากกว่าครอบครัว"
  - "สมองของคุณ vs ChatGPT ใครชนะ?"

### 2. Description (200-300 words)
Structure:
- Hook sentence (matches title)
- Brief summary of video content
- Timestamps for each chapter/section
- Call to subscribe/comment
- Links to sources mentioned

Format:
```
[Hook sentence that matches title]

[Brief summary - 2-3 sentences about what viewer will learn]

TIMESTAMPS:
0:00 - Hook
[XX:XX] - [Chapter 1 title]
[XX:XX] - [Chapter 2 title]
...

OURCES:
- [Source 1 with link]
- [Source 2 with link]
- [Source 3 with link]

---
 Subscribe กดกระดิ่ง 🔔 เพื่อไม่พลาดคลิปใหม่
 Comment บอกว่าคุณคิดยังไง!
```

### 3. Tags (10-15 keywords)
Mix of:
- Broad tags: เทคโนโลยี, AI, ปัญญาประดิษฐ์
- Specific tags: ChatGPT, machine learning, neural network
- Thai tags: สาระดีๆ, ความรู้, สรุปให้
- Trending tags: [check YouTube trending]

### 4. Thumbnail Concepts (3 options)
Each concept includes:
- Visual description
- Text overlay (ALL CAPS, 3-5 words)
- Color scheme
- Image prompt for generation

Example:
```
THUMBNAIL CONCEPT 1:
- Visual: Stick figure looking shocked at phone screen
- Text: "AI โกหก?" in RED
- Colors: White bg, red text, blue phone
- Prompt: "Stick figure cartoon, shocked expression, looking at glowing phone screen, bold red text overlay 'AI โกหก?', white background, 16:9"

THUMBNAIL CONCEPT 2:
- Visual: Brain vs computer chip side by side
- Text: "ใครฉลาดกว่า?" in YELLOW
- Colors: Split bg, brain pink, chip green

THUMBNAIL CONCEPT 3:
- Visual: Magnifying glass over code lines
- Text: "ความลับ" in RED
- Colors: Dark bg, green code, red magnifier
```

---

## OUTPUT FORMAT

Saved to: output/[topic-slug]/metadata.md

```markdown
# [Video Title]

## Title
[Title in Thai, ≤60 chars]

## Description
[Full description with timestamps and sources]

## Tags
[tag1, tag2, tag3, ...]

## Thumbnail Concepts

### Concept 1: [Name]
- Visual: [description]
- Text: "[text overlay]"
- Colors: [scheme]
- Prompt: "[full image generation prompt]"

### Concept 2: [Name]
...

### Concept 3: [Name]
...
```

---

## RULES

- Titles must be ≤60 characters (YouTube limit)
- Description must include timestamps (helps with SEO)
- Tags should mix broad + specific + trending
- Thumbnail text must be ALL CAPS, max 5 words
- Thumbnails should work at small size (mobile)
- No misleading claims — clickbait must deliver
