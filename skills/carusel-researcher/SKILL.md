---
name: carusel-researcher
category: social-media
description: |
  Researches Instagram carousel topics via Tavily: audience analysis, competitor audit, angle discovery
version: 1.0.0
author: zaharenok
tags: [instagram, carousel, research, tavily, market-analysis]
---

# Carusel Researcher

## Роль

Исследователь для Instagram-каруселей. Анализирует тему, аудиторию, конкурентов, тренды.

## Инструменты

- **Tavily MCP** — ресерч тем, трендов, конкурентов
- **Web search** — дополнительная информация
- **File operations** — чтение/запись результатов

## Входные данные

Читает из `{SESSION_ROOT}/00-brief.md`:
```markdown
## Тема
Как AI меняет маркетинг

## Референс-аккаунт
@neilpatel

## Целевая аудитория
Маркетологи 25-45 лет, SMB owners

## CTA
Подписаться на рассылку
```

## Процесс

1. **Анализ темы** через Tavily:
```python
mcp_tavily_remote_tavily_research(
    input=f"Analyze Instagram content trends about: {topic}",
    max_results=10
)
```

2. **Аудит референса**:
```python
# Скачивать последние 20 каруселей референса
# Анализировать форматы, заголовки, CTA
# Выявлять паттерны
```

3. **Конкурентный анализ**:
```python
mcp_tavily_remote_tavily_search(
    query=f"instagram carousel {topic} examples",
    max_results=10
)
```

4. **Углы подачи** — 3-5 вариантов:
- "AI → Automation → ROI"
- "Tools → Tactics → Results"
- "Future → Now → Action"

## Выходные данные

Пишет в `{SESSION_ROOT}/01-research.md`:

```markdown
# Research Report

## Аудитория
- Поколение: Millennials (25-40) dominate Instagram carousel consumption
- Платформы: 60% mobile, 40% desktop
- Внимание: 3 seconds per slide → punchy headlines critical

## Тренды темы
- AI tool screenshots + annotations (high CTR)
- Before/After comparisons (38% higher save rate)
- Step-by-step frameworks (57% higher share rate)

## Анализ референса (@neilpatel)
- Средний слайд: 150-200 слов
- Заголовки: Question-based (70%), Numbered lists (30%)
- CTA: Link in bio only (87%), DM for template (13%)
- Цвета: Blue (#007AFF), White (#FFFFFF), Yellow (#FFD600)

## Конкуренты
- @garyvee: Short slides, heavy emoji, video-first
- @hubspot: Educational, case study format
- @ Buffer: Data-backed charts, minimal text

## Рекомендуемые углы
1. **Tool → Case Study → ROI** (для SMB owners)
2. **Problem → AI Solution → Implementation** (для маркетологов)
3. **Trend → Tool → Tutorial** (для early adopters)

## Pitfalls
- Overly technical jargon → keep it simple
- Too much text per slide → max 40 words
- Missing CTA on final slide → convert point critical
```

## Fragment contract

Создать `{SESSION_ROOT}/fragments/01-research-summary.md`:
```markdown
# Research Summary

## Done
- Analyzed 20 reference carousels
- Audited 3 competitors
- Identified 5 trend patterns

## Issues
- Reference account posts infrequently (2/month)
- Limited carousel data for B2B audience

## Recommendations
- Focus on B2C marketing angle (more data)
- Use broader reference pool
```

## Pitfalls из `shared/agent-pipeline-pitfalls.md`

- Не копировать структуру референса 1:1 → адаптировать под бренд
- Не игнорировать platform-specific форматы → Instagram vertical 4:5
- Не перегружать данными → 3 key insights max

## Environment variables

```bash
TAVILY_API_KEY=tvly-...
SESSION_ROOT=~/.hermes/karuselka/sessions/{timestamp}/
```