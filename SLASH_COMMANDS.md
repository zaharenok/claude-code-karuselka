# Hermes Slash Commands Integration

## Добавление команд

Копируйте команды в `~/.hermes/commands/`:

```bash
cp commands/carousel-new.md ~/.hermes/commands/
cp commands/carousel-publish.md ~/.hermes/commands/
```

## /carousel-new

Создаёт новую Instagram-карусель через пайплайн агентов.

### Параметры

```bash
/carousel-new --topic "Тема" --reference "@аккаунт" --cta "CTA" --audience "Аудитория"
```

### Примеры

```bash
# Базовое
/carousel-new --topic "AI automation tools"

# С референсом
/carousel-new --topic "Facebook ads" --reference "@garyvee" --cta "Book audit"

# Dry run (только текст)
/carousel-new --topic "AI SEO" --dry-run
```

## /carousel-publish

Публикует готовую карусель.

### Параметры

```bash
/carousel-publish --session-id ~/.hermes/karuselka/sessions/{timestamp}/
```

### Примеры

```bash
/carousel-publish --session-id ~/.hermes/karuselka/sessions/2025-01-15-143022/
```

## Реализация через delegate_task

```
/carousel-new --topic "X"
```

делегирует в `skills/director-carusel/`, который затем:

```python
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

Каждый субагент использует `delegate_task` для следующего шага.