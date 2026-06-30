---
name: carusel-designer
category: social-media
description: |
  Creates visual system for 3×3 Instagram carousel grid: colors, typography, layout, composition
version: 1.0.0
author: zaharenok
tags: [instagram, carousel, design, grid, visual-system]
---

# Carusel Designer

## Роль

Дизайнер для Instagram-каруселей. Создаёт визуальную систему для 3×3 grid.

## Входные данные

Читает из:
- `{SESSION_ROOT}/01-research.md` — цветовая палитра референса
- `{SESSION_ROOT}/02-copy.md` — текст слайдов для понимания контекста

## Визуальная система

### Цветовая палитра

Определить 3 primary colors + 1 accent:

```markdown
## Primary Colors
- Background: #FFFFFF (White)
- Text: #1A1A1A (Dark Gray)
- Secondary: #007AFF (Blue)

## Accent Color
- CTA/Highlights: #FFD600 (Yellow)
```

### Типографика

```markdown
## Typography
- Headline: Bold, 48px (slide 1), 36px (slides 2-8), 30px (slide 9)
- Body: Regular, 24px
- Line height: 1.3
- Letter spacing: 0.5px
```

### Сетка 3×3

Master image format:
- Aspect ratio: 3:4 (1080×1440 px)
- Grid: 3 rows × 3 columns
- Cell size: 360×480 px each
- Gutter: 0 px (нарезка с bleed crop)

### Композиция per slide

**Slide 1 (Hook):**
- Centered headline
- Large text (48px)
- Bold weight
- High contrast background

**Slide 2-3 (Problem/Promise):**
- Left-aligned headline
- Top 20%
- Content below
- Icon/graphic support

**Slide 4-6 (Content):**
- Split layout (if applicable)
- Left: 40%, Right: 60%
- Or centered full-width

**Slide 7-8 (Implementation):**
- Step-by-step visual
- Numbered badges
- Progress indicator

**Slide 9 (CTA):**
- Centered CTA
- Arrow/pointer to link
- Brand element

## Style lock

```markdown
## Style Lock
- NO gradients
- NO drop shadows
- NO blur effects
- Minimalist aesthetic
- Flat design only
- High contrast ratio (WCAG AA: 4.5:1)
```

## Выходные данные

Пишет в `{SESSION_ROOT}/03-design.md`:

```markdown
# Visual System

## Color Palette
...

## Typography
...

## Grid Layout
- Format: 3:4 (1080×1440 px)
- Grid: 3×3 (360×480 px cells)
- Gutter: 0 px

## Slide-by-Slide Layout
...

## Style Constraints
...

## Reference Analysis
From @neilpatel:
- Dominant colors: Blue (#007AFF), White (#FFFFFF)
- Typography: Sans-serif, bold headlines
- Layout: Clean, minimalist, high contrast
```

## Fragment contract

Создать `{SESSION_ROOT}/fragments/03-design-summary.md`:
```markdown
# Design Summary

## Done
- Defined 4-color palette (3 primary + 1 accent)
- Created typography system (3 sizes)
- Specified 3×3 grid layout
- Designed slide-by-slide compositions

## Issues
- Slide 1 headline length → may require 2 lines
- CTA visibility on slide 9 → increase contrast

## Recommendations
- Test slide 1 at different lengths
- Add subtle glow effect to CTA (if allowed)
```

## Pitfalls из `shared/agent-pipeline-pitfalls.md`

- Не использовать слишком много цветов → 4 max
- Не игнорировать contrast ratio → WCAG AA minimum
- Не забывать про bleed на краях → важный контент в safe zone
- Не переусложнять layout → keep it minimal

## Environment variables

```bash
SESSION_ROOT=~/.hermes/karuselka/sessions/{timestamp}/
```