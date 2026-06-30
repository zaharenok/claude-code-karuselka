# FrameForge

Агентская система для создания социальных каруселей: ресерч, текст, дизайн, генерация изображений/видео, QA, загрузка и публикация.

Платформы: Instagram, Meta Ads, Facebook, LinkedIn.

## Быстрый старт

```bash
git clone https://github.com/zaharenok/frameforge.git
cd frameforge
pip install -r scripts/requirements.txt
cp .env.example .env  # Добавьте свои API ключи
```

Создать карусель:
```bash
/carousel-new --topic "AI маркетинг" --platform instagram --reference "@neilpatel"
```

Публиковать:
```bash
/carousel-publish --session-id ~/.hermes/frameforge/sessions/{timestamp}/
```

## Возможности

- **Мультиплатформенность**: Instagram, Meta Ads, Facebook, LinkedIn
- **Полный пайплайн**: Ресерч → Текст → Дизайн → Генерация изображений/видео → QA → Загрузка → Публикация
- **Интеграция ресерча**: Tavily MCP, Brave Search
- **Генерация изображений**: Kie.ai, OpenRouter, fal.ai, локальные модели
- **Генерация видео**: Grok Video, fal.ai
- **Хранилище**: Kie.ai, S3, локальное
- **Интеграция с Hermes**: Слэш-команды, delegate_task оркестрация

## Архитектура

FrameForge использует оркестрацию Hermes Agent со специализированными субагентами:

| Агент | Роль | Инструменты |
|-------|------|-------------|
| researcher | Ресерч рынка, анализ конкурентов | Tavily MCP, Brave Search |
| copywriter | Текст 9 слайдов + caption + CTA | — |
| designer | Визуальная система 3×3 сетка | — |
| image-prompter | Промпты для генерации изображений | — |
| slice | Генерация master image + нарезка | Kie.ai / OpenRouter / fal.ai / local |
| motion-director | Сценарий анимации | — |
| animate | Loop видео для slide-01 | Grok Video / fal.ai |
| design-guardian | QA: дизайн, bleed, aspect ratio | — |
| upload | Загрузка ассетов на HTTPS хранилище | Kie.ai / S3 / local |
| publish | Публикация через MCP | Instagram / Meta Ads / Facebook / LinkedIn |
| fixic | Разбор инцидентов | — |

## Пайплайн

```
research → copy → design → image-prompt → generate → slice → motion → animate → QA → upload → publish → fixic
```

Подробнее в [AGENT-PIPELINE.md](AGENT-PIPELINE.md).

## Поддерживаемые сервисы

### Ресерч
- **Tavily MCP**: Веб-ресерч, анализ конкурентов, детекция трендов
- **Brave Search**: Альтернативный поиск с фокусом на приватность

### Генерация изображений
- **Kie.ai**: Быстрая генерация изображений (начните с [реферальной ссылкой](https://kie.ai?ref=80779f6a33a1f5311277ef1c44c0f665))
- **OpenRouter**: Доступ к Flux, Stable Diffusion и другим моделям
- **fal.ai**: Быстрая инференция для моделей изображений
- **Local**: Ollama с поддерживаемыми моделями

### Генерация видео
- **Seedance 1.5 Pro (ByteDance)**: Самый дешёвый вариант на Kie.ai ($0.0175/s, 720p, 5s loop, без аудио) — рекомендуется
- **Grok Video**: Loop видео для первого слайда (требуется отдельный API ключ)
- **fal.ai**: Альтернативная генерация видео

### Хранилище
- **Kie.ai**: Интегрированный CDN
- **S3**: AWS S3 или совместимый
- **Local**: Локальное файловое хранилище

### Публикация
- **Instagram**: Через MCP или Make автоматизацию
- **Meta Ads**: Создание карусельной рекламы
- **Facebook**: Органические посты
- **LinkedIn**: Профессиональные посты

## Установка

### Требования
- Python 3.10+
- Claude Code CLI (опционально, для нативного режима)
- Hermes Agent с поддержкой delegate_task
- API ключи для выбранных сервисов

### Настройка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/zaharenok/frameforge.git
cd frameforge
```

2. Установите зависимости:
```bash
pip install -r scripts/requirements.txt
```

3. Настройте окружение:
```bash
cp .env.example .env
# Отредактируйте .env с вашими API ключами
```

4. Установите навыки Hermes (опционально):
```bash
hermes skills add skills/director-carusel/
hermes skills add skills/carusel-researcher/
# ... добавьте другие навыки по необходимости
```

## Использование

### Создать карусель

```bash
/carousel-new --topic "AI маркетинг" --platform instagram --reference "@neilpatel"
```

Параметры:
- `--topic`: Тема карусели (обязательно)
- `--platform`: Платформа (instagram, meta-ads, facebook, linkedin)
- `--reference`: Референс-аккаунт (опционально)
- `--cta`: Call-to-action (опционально)
- `--audience`: Целевая аудитория (опционально)
- `--auto-publish`: Публиковать после QA (опционально)
- `--dry-run`: Пропустить генерацию изображений (опционально)

### Опубликовать карусель

```bash
/carousel-publish --session-id ~/.hermes/frameforge/sessions/{timestamp}/
```

### Специфика платформ

**Instagram**: Стандартная сетка 3×3, 1080×1350 (по умолчанию) или 1080×1080 на слайд, видео: Seedance 1.5 Pro (5s loop)

**Meta Ads**: Соотношения сторон 1080×1350 (по умолчанию) или 1080×1080, 1080×1920, видео: Seedance 1.5 Pro (5s loop, опционально)

**Facebook**: Квадратный формат 1080×1080, видео: Seedance 1.5 Pro (5s loop, опционально)

**LinkedIn**: 1080×1080 или 1200×627 (альбомный), видео: Не рекомендуется

## Лицензия

MIT License - см. [LICENSE](LICENSE).

## Благодарности

- Оригинальный [Karuselka](https://github.com/Horosheff/Karuselka) для Cursor
- Hermes Agent framework
- Tavily за API ресерча
- Kie.ai за генерацию изображений (начните с [реферальной ссылкой](https://kie.ai?ref=80779f6a33a1f5311277ef1c44c0f665))