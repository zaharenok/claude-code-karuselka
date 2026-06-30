# Hermes Agent Configuration

This directory contains Hermes Agent configurations for Karuselka agents.

Each agent is defined as a Hermes skill that can be invoked via delegate_task.

## Skills Mapping

| Cursor Agent | Hermes Skill | Description |
|--------------|--------------|-------------|
| director | `skills/director-carusel/` | Orchestrates the pipeline |
| carusel-researcher | `skills/carusel-researcher/` | Research via Tavily |
| carusel-copywriter | `skills/carusel-copywriter/` | Copy for 9 slides + caption |
| carusel-designer | `skills/carusel-designer/` | Visual system 3×3 grid |
| carusel-image-prompter | `skills/carusel-image-prompter/` | Image generation prompts |
| carusel-slice | `skills/carusel-slice/` | Master image slicing |
| carusel-motion-director | `skills/carusel-motion-director/` | Motion direction |
| carusel-animate | `skills/carusel-animate/` | Video generation |
| carusel-design-guardian | `skills/carusel-design-guardian/` | QA checks |
| carusel-upload | `skills/carusel-upload/` | Asset upload |
| carusel-publish | `skills/carusel-publish/` | MCP publish |
| carusel-fixic | `skills/carusel-fixic/` | Incident resolution |

## Installation

Add these skills to Hermes:

```bash
cd claude-code-karuselka
hermes skills add skills/director-carusel/
hermes skills add skills/carusel-researcher/
hermes skills add skills/carusel-copywriter/
# ... etc
```

## Usage

Via delegate_task:

```python
delegate_task(
    goal="Create Instagram carousel on topic X",
    skills=["director-carusel"],
    context="..."
)
```

Via slash commands:

```
/carousel-new --topic "AI marketing" --reference "@user"
/carousel-publish --session-id path/to/session
```