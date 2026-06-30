# Claude Code Karuselka

Агентская система Claude Code для создания 9-слайдовых Instagram-каруселей: research, copy, design, image/video generation, QA, upload and MCP publish.

## Отличия от оригинала (Cursor)

- **Claude Code native**: Использует Claude Code вместо Cursor
- **Hermes agents**: Интеграция с Hermes Agent через delegate_task
- **Tavily research**: Встроенный ресерч через Tavily MCP
- **Hermes slash commands**: Интеграция с Hermes CLI (/carousel-new, /carousel-publish)
- **Multi-provider image gen**: Поддержка Kie.ai, OpenRouter (Flux/SD), локальных моделей
- **Orchestration via Hermes**: Автоматическое делегирование субагентов

## Карта функционала

| Зона | Компоненты | Назначение |
| --- | --- | --- |
| Оркестрация | `rules/`, `agents/director.md`, `skills/director-carusel/` | Управляет пайплайном и handoff между агентами |
| Ресерч | `agents/carusel-researcher.md`, `skills/carusel-researcher/` | Анализ темы, аудитории, конкурентов через Tavily |
| Текст | `agents/carusel-copywriter.md`, `skills/carusel-copywriter/` | 9 слайдов, caption, CTA и структура сторителлинга |
| Дизайн | `agents/carusel-designer.md`, `skills/carusel-designer/`, `shared/CAROUSEL_DESIGN_SPEC.md` | Визуальная система, композиция, style lock |
| Image prompt | `agents/carusel-image-prompter.md`, `skills/carusel-image-prompter/` | JSON/MD prompt для image generation, 9 panel briefs |
| Генерация и slice | `agents/carusel-slice.md`, `scripts/image_gen.py`, `scripts/slice_grid.py` | Master image 3:4 @ 4K и нарезка 3×3 |
| Motion | `agents/carusel-motion-director.md`, `agents/carusel-animate.md`, `scripts/video_gen.py` | Сценарий анимации и MP4 для первого слайда |
| QA | `agents/carusel-design-guardian.md`, `scripts/video_frame_qa.py` | Проверка дизайна, bleed, aspect ratio, frame0 fidelity |
| Upload | `agents/carusel-upload.md`, `scripts/upload_carousel_assets.py` | HTTPS upload, run-scoped paths, MP4 normalization |
| Publish | `agents/carusel-publish.md`, `scripts/publish_preflight.py` | MCP publish без blind retry и дублей |
| Fixic | `agents/carusel-fixic.md`, `skills/carusel-fixic/` | Разбор инцидентов и durable fixes |
| Общие контракты | `shared/` | Playbook, API contracts, pitfalls, publish rules |

## Требования

- Claude Code CLI
- Hermes Agent с delegate_task
- Python 3.10+
- Image generation API (Kie.ai, OpenRouter, или локальная модель)
- `ffmpeg` и `ffprobe` для проверки/нормализации MP4
- Tavily API key для ресерча (опционально)
- MCP-интеграция для публикации в Instagram

## Установка

1. Склонируйте репозиторий:
```bash
git clone https://github.com/zaharenok/claude-code-karuselka.git
cd claude-code-karuselka
```

2. Установите зависимости Python:
```bash
pip install -r scripts/requirements.txt
```

3. Создайте `.env`:
```env
TAVILY_API_KEY=your_tavily_api_key_here
IMAGE_GEN_PROVIDER=kie  # kie, openrouter, or local
IMAGE_GEN_API_KEY=your_image_gen_api_key_here
UPLOAD_STORAGE=kie  # kie, s3, or local
```

4. Добавьте слэш-команды Hermes:
```bash
hermes skills install carousel-new
hermes skills install carousel-publish
```

## Использование

Создание новой карусели:
```bash
hermes /carousel-new --topic "Как AI меняет маркетинг" --reference "@neilpatel"
```

Публикация готовой карусели:
```bash
hermes /carousel-publish --session-id carusel-memory/session-2025-01-15/
```

## Пайплайн

```
director
-> researcher (Tavily)
-> copywriter
-> designer
-> image-prompter
-> slice
-> motion-director
-> animate
-> design-guardian
-> upload
-> publish
-> fixic
```

## Лицензия

MIT