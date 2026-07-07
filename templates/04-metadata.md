=== TEMPLATE: Metadata & Thumbnail ===

This template defines how OpenCode generates your YouTube/TikTok metadata.
Say "seo pack for [topic]" and I follow these rules.

---

## WHAT OPENCODE GENERATES

### 1. Title (≤60 characters)
- Clickbait but deliverable
- Thai language
- Include curiosity gap or number
- Business analysis examples:
  - "ทำไมเซเว่นฯ ครองไทยได้? เบื้องหลังที่คุณไม่รู้"
  - "ความล้มเหลวพันล้านของ [brand]"
  - "[Company A] vs [Company B] ใครชนะ?"

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

SOURCES:
- [Source 1 with link]
- [Source 2 with link]
- [Source 3 with link]

---
 กด Subscribe กดกระดิ่ง 🔔 เพื่อไม่พลาดคลิปใหม่
 Comment บอกว่าคุณคิดยังไง!
```

### 3. Tags (10-15 keywords)
Mix of:
- Broad tags: ธุรกิจ, วิเคราะห์ธุรกิจ, เคสสตัดดี้
- Company-specific: [company name], [brand name], [founder name]
- Thai tags: สาระดีๆ, ความรู้ธุรกิจ, ทำไม, เบื้องหลัง
- Format tags: เคสสตัดดี้, วิเคราะห์, สรุปให้
- Trending tags: [check YouTube trending Thailand]

### 4. Thumbnail Concepts (3 options)
Each concept includes:
- Visual description
- Text overlay (ALL CAPS, 3-5 words in Thai)
- Color scheme
- Google Flow image prompt

Example:
```
THUMBNAIL CONCEPT 1:
- Visual: 7-Eleven storefront with dramatic orange glow, money raining
- Text: "ทำไมถึงครอง?" in WHITE on blue
- Colors: Deep blue bg, orange accent, white text
- Prompt: "Flat 2D infographic illustration, 7-Eleven convenience store storefront with dramatic orange glow effect, Thai baht bills floating around, deep blue background, bold white text space at top, business magazine style, 16:9, no photorealism"

THUMBNAIL CONCEPT 2:
- Visual: Split screen — 7-Eleven logo vs competitor logos
- Text: "ใครชนะ?" in RED
- Colors: Split bg, green left, red right

THUMBNAIL CONCEPT 3:
- Visual: Giant 7-Eleven number "13,000+" with Thai map
- Text: "13,000 สาขา" in ORANGE
- Colors: Light bg, orange number, blue accents
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
- Prompt: "[full Google Flow image generation prompt]"

### Concept 2: [Name]
...

### Concept 3: [Name]
...
```

---

## RULES

- Titles must be ≤60 characters (YouTube limit)
- Description must include timestamps (helps with SEO)
- Tags should mix broad + specific + company-specific + trending
- Thumbnail text must be ALL CAPS Thai, max 5 words
- Thumbnails should work at small size (mobile — most Thai viewers)
- No misleading claims — clickbait must deliver
- Business/finance CPM is $3-8 in Thailand — optimize for watch time
