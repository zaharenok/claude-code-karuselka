---
name: carousel-new
description: Create new Instagram carousel via Karuselka pipeline
version: 1.0.0
author: zaharenok
---

# /carousel-new

Создаёт новую Instagram-карусель (9 слайдов, сетка 3×3) через пайплайн агентов.

## Использование

```
/carousel-new --topic "Как AI меняет маркетинг" --reference "@neilpatel" --cta "Подписаться на рассылку"
```

## Параметры

| Параметр | Обязательный | Описание | Пример |
|----------|--------------|----------|--------|
| `--topic` | Да | Тема карусели | `--topic "AI marketing tips"` |
| `--reference` | Нет | Референс-аккаунт Instagram | `--reference "@neilpatel"` |
| `--cta` | Нет | Call-to-action | `--cta "Download free guide"` |
| `--audience` | Нет | Целевая аудитория | `--audience "Marketers 25-45"` |

## Пайплайн

1. **Init**: Создаёт `~/.hermes/karuselka/sessions/{timestamp}/`
2. **Research**: Делегирует `carusel-researcher` → ресерч через Tavily
3. **Copy**: Делегирует `carusel-copywriter` → текст 9 слайдов
4. **Design**: Делегирует `carusel-designer` → визуальная система
5. **Image Prompt**: Делегирует `carusel-image-prompter` → промпты для генерации
6. **Generate**: Генерирует master image через `image_gen.py`
7. **Slice**: Нарезает master image на 9 слайдов
8. **Motion**: Создаёт сценарий анимации для slide-01
9. **Animate**: Генерирует видео для slide-01
10. **QA**: Проверяет дизайн, bleed, aspect ratio
11. **Upload**: Загружает ассеты на хранилище
12. **Publish**: Публикует через MCP (если `--auto-publish`)

## Опции

| Опция | Описание |
|-------|----------|
| `--auto-publish` | Автоматически публиковать после QA |
| `--dry-run` | Не генерировать изображения, только текст |
| `--skip-upload` | Пропустить загрузку ассетов |
| `--session-id` | Использовать существующую сессию |

## Примеры

### Базовое создание
```
/carousel-new --topic "AI automation tools"
```

### С референсом и CTA
```
/carousel-new --topic "Facebook ads strategy" --reference "@garyvee" --cta "Book free audit"
```

### С описанием аудитории
```
/carousel-new --topic "LinkedIn growth" --reference "@justinwelsh" --cta "Join community" --audience "B2B founders"
```

### Dry run (только текст)
```
/carousel-new --topic "AI SEO tips" --dry-run
```

## Выходные файлы

Сессия создаётся в `~/.hermes/karuselka/sessions/{timestamp}/`:

```
├── 00-brief.md          # Бриф
├── 01-research.md       # Ресерч
├── 02-copy.md           # Текст
├── 03-design.md         # Дизайн
├── 04-prompts.md        # Промпты
├── 05-master.png        # Master image
├── 06-slices/           # 9 слайдов
│   ├── slide-01.png
│   ├── slide-02.png
│   └── ...
├── 07-motion.md         # Сценарий анимации
├── 08-anim-01.mp4       # Видео slide-01
├── 09-qa.md             # QA отчёт
├── 10-upload.json       # URL ассетов
├── 11-publish.md        # Результат публикации
└── fragments/           # Суммарные фрагменты
```

## Environment variables

```bash
TAVILY_API_KEY=tvly-...
IMAGE_GEN_PROVIDER=kie
KIE_API_KEY=...
SESSION_ROOT=~/.hermes/karuselka/sessions
```

## После создания

Для публикации:
```
/carousel-publish --session-id ~/.hermes/karuselka/sessions/{timestamp}/
```