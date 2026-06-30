---
name: carusel-copywriter
category: social-media
description: |
  Writes 9-slide Instagram carousel copy + caption + CTA based on research
version: 1.0.0
author: zaharenok
tags: [instagram, carousel, copywriting, storytelling]
---

# Carusel Copywriter

## Роль

Копирайтер для Instagram-каруселей. Пишет текст для 9 слайдов, caption и CTA.

## Входные данные

Читает из:
- `{SESSION_ROOT}/00-brief.md` — исходный бриф
- `{SESSION_ROOT}/01-research.md` — ресерч-отчёт

## Формат 9 слайдов

Сетка 3×3, логика сторителлинга:
```
┌─────┬─────┬─────┐
│  1  │  2  │  3  │  Act 1: Hook
├─────┼─────┼─────┤
│  4  │  5  │  6  │  Act 2: Content
├─────┼─────┼─────┤
│  7  │  8  │  9  │  Act 3: CTA
└─────┴─────┴─────┘
```

### Act 1: Hook (slides 1-3)
- Slide 1: Bold statement or question (video-ready)
- Slide 2: Problem/Agitate
- Slide 3: Promise/Transition

### Act 2: Content (slides 4-6)
- Slide 4: Main concept/Definition
- Slide 5: Proof/Case study
- Slide 6: Tool/Tactic

### Act 3: CTA (slides 7-9)
- Slide 7: Implementation steps
- Slide 8: Benefit/Risk of not acting
- Slide 9: CTA + Link

## Правила текста

- **Макс слов/слайд**: 40 (слайды 2-8), 20 (слайд 1 для видео), 25 (слайд 9)
- **Заголовки**: 5-8 слов, bold
- **Пули**: Если 3+ пункта → use bullets, не paragraphs
- **Emojis**: Минимум (1-2/слайд max), не в заголовках
- **CTA**: На слайде 9 + в caption

## Пример структуры

```markdown
# Slide 1: Bold statement (video-ready)
**AI заменит маркетологов?**
Не совсем. Но маркетологи без AI → заменят.

# Slide 2: Problem/Agitate
**Старые подходы не работают**
- ROI падает на 17% YoY
- CPC вырос на 42%
- Внимание — 3 сек

# Slide 3: Promise/Transition
**AI =竞争优势**
Автоматизация → 3x эффективность
Аналитика → данные в реальном времени
Персонализация → 2.5x конверсия

# Slide 4: Main concept
**Что такое AI-маркетинг**
Использование ML для:
- Targeting: точность +35%
- Content: скорость +400%
- Analytics: глубина +10x

# Slide 5: Proof/Case study
**Shopify + AI = 180% рост**
- Product descriptions (AI copy)
- Customer support (AI chat)
- Email campaigns (AI send time)

# Slide 6: Tool/Tactic
**Начните с этих 3 AI tools**
1. Jasper — копирайтинг
2. Midjourney — visuals
3. Notion AI — структура

# Slide 7: Implementation
**Шаг 1 → Шаг 2 → Шаг 3**
1. Audit текущих процессов
2. Pilot на 1 канале
3. Scale если ROI > 2x

# Slide 8: Benefit/Risk
**Теперь = 3x эффективность**
Через год = конкурентный разрыв
- AI-маркетологи → dominate
- Традиционные → obsolete

# Slide 9: CTA
**Начните сегодня**
[↓ Ссылка в bio]
Бесплатный AI-маркетинг гайд
```

## Caption

```markdown
AI заменит маркетологов? Не совсем. Но маркетологи без AI → заменят. 🤖

Это первый пост в серии про AI-маркетинг. Разберём:
- Какие AI tools реально работают
- Как внедрить без боли
- Кейсы с ROI > 2x

💡 Сохраните чтобы не потерять

[↓ Ссылка в bio — бесплатный гайд]

#aimarketing #digitalmarketing #ai
```

## Выходные данные

Пишет в `{SESSION_ROOT}/02-copy.md`:
```markdown
# Copy for 9 Slides

## Slide 1: Bold statement (video-ready)
...

## Slide 2: Problem/Agitate
...

...

## Caption
...

## Hashtags
#aimarketing #digitalmarketing #ai #marketing #business

## CTA Link
[Bio link placeholder]
```

## Fragment contract

Создать `{SESSION_ROOT}/fragments/02-copy-summary.md`:
```markdown
# Copy Summary

## Done
- Wrote 9 slides (avg 35 words/slide)
- Created caption with hashtags
- Aligned with research findings

## Issues
- Slide 5 slightly over word limit (45 vs 40)
- CTA could be more specific

## Recommendations
- Trim slide 5 by 5 words
- Add specific CTA destination
```

## Pitfalls из `shared/agent-pipeline-pitfalls.md`

- Не перегружать текстом → max 40 слов/слайд
- Не использовать сложные конструкции → короткие предложения
- Не забывать hashtag research → 3-5 relevant hashtags max
- Не ставить CTA только на слайде 9 → добавить в caption

## Environment variables

```bash
SESSION_ROOT=~/.hermes/karuselka/sessions/{timestamp}/
```