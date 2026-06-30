---
name: director-carusel
category: social-media
description: |
  Orchestrates Instagram carousel creation pipeline via Hermes delegate_task:
  researcher -> copywriter -> designer -> image-prompter -> slice -> motion-director -> animate -> guardian -> upload -> publish -> fixic
version: 1.0.0
author: zaharenok
tags: [instagram, carousel, hermes, delegation, pipeline]
---

# Director - Каруселька

## Роль

Директор пайплайна Instagram-карусели (9 слайдов, сетка 3×3). Оркестрирует цепочку субагентов через `delegate_task`.

## Источники

- `HERMES_AGENTS.md` — маппинг агентов на навыки Hermes
- `AGENT-PIPELINE.md` — визуальный пайплайн
- `shared/subagent-end-of-task-contract.md` — контракт завершения
- `shared/agent-pipeline-pitfalls.md` — подводные камни

## Память сессии

```bash
SESSION_ROOT=~/.hermes/karuselka/sessions/{timestamp}/
```

Структура:
```
SESSION_ROOT/
├── 00-brief.md          # Исходный бриф (тема, референс, CTA)
├── 01-research.md       # Результат ресерчера
├── 02-copy.md           # Текст 9 слайдов + caption
├── 03-design.md         # Дизайн-система 3×3 grid
├── 04-prompts.md        # Промпты для image gen
├── 05-master.png        # Сгенерированный master image
├── 06-slices/           # 9 нарезанных слайдов
├── 07-motion.md         # Сценарий анимации
├── 08-anim-01.mp4       # Анимированный первый слайд
├── 09-qa.md             # QA отчёт
├── 10-upload.json       # URL загруженных ассетов
├── 11-publish.md        # Результат публикации
└── pipeline-fix-queue.md  # Очередь исправлений
```

## Цепочка исполнения

1. **researcher** — Анализ темы, аудитории, конкурентов через Tavily
2. **copywriter** — Текст для 9 слайдов + caption + CTA
3. **designer** — Визуальная концепция для 3×3 grid
4. **image-prompter** — Компактные промпты для image gen
5. **slice** — Генерация master image + нарезка 3×3
6. **motion-director** — Сценарий анимации для slide-01
7. **animate** — Генерация loop-видео для slide-01
8. **design-guardian** — QA проверки (design, bleed, aspect ratio)
9. **upload** — Загрузка ассетов на HTTPS-хранилище
10. **publish** — Публикация через MCP
11. **fixic** — Разбор инцидентов и durable fixes

## Команда создания новой карусели

```
/carousel-new --topic "Как AI меняет маркетинг" --reference "@neilpatel"
```

## Пример делегирования

```python
# Вызывается из skills/director-carusel/
delegate_task(
    goal="Research Instagram carousel topic: {topic}",
    skills=["carusel-researcher"],
    context=f"""
    Topic: {topic}
    Reference: {reference}
    Session root: {SESSION_ROOT}
    """,
    toolsets=["web", "file"]
)
```

## Контракт субагента

Каждый субагент должен:
1. Читать входные данные из `{SESSION_ROOT}/{step}-{prev}.md`
2. Писать результат в `{SESSION_ROOT}/{step}-{name}.md`
3. Если есть проблемы → добавлять в `pipeline-fix-queue.md`
4. В конце создавать fragment в `fragments/{step}-summary.md`

## Проверка pipeline-fix-queue

После каждого шага:
- Если есть `status: open` → вызывать `carusel-fixic`
- Fixic разбирает инциденты и возвращает durable fix

## Фоллбэк если delegate_task недоступен

Если `delegate_task` недоступен → выполнить шаги локально:
- Читать `skills/{skill-name}/SKILL.md`
- Выполнять инструкции напрямую
- Писать результаты в `{SESSION_ROOT}/`

## Интеграция с Tavily

Ресерчер использует Tavily MCP:
```python
mcp_tavily_remote_tavily_research(
    input="Analyze Instagram carousel trends for: {topic}"
)
```

## Интеграция с image generation

Slice агент поддерживает:
- **Kie.ai** (primary): API ключ из `KIE_API_KEY`
- **OpenRouter**: `IMAGE_GEN_PROVIDER=openrouter`
- **Local**: `IMAGE_GEN_PROVIDER=local` с `ollama serve`

## Publish через MCP

Publish агент использует Instagram MCP:
```python
# POST /instagram/publish-carousel
{
  "slides": [url1, url2, ..., url9],
  "caption": "...",
  "hashtags": ["#ai", "#marketing", ...]
}
```