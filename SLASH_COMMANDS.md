# Hermes Slash Commands Integration

## Installation

Copy commands to `~/.hermes/commands/`:

```bash
cp commands/carousel-new.md ~/.hermes/commands/
cp commands/carousel-publish.md ~/.hermes/commands/
```

## /carousel-new

Creates a new social media carousel through the agent pipeline.

### Syntax

```bash
/carousel-new --topic "Topic" --platform [instagram|meta-ads|facebook|linkedin] --reference "@account" --cta "CTA" --audience "Audience" --research-service [tavily|brave] --image-provider [kie|openrouter|fal|local]
```

### Examples

```bash
# Instagram with default settings
/carousel-new --topic "AI automation tools" --platform instagram

# Meta Ads with reference and CTA
/carousel-new --topic "Facebook ads strategy" --platform meta-ads --reference "@garyvee" --cta "Book audit"

# LinkedIn with Brave Search and fal.ai
/carousel-new --topic "LinkedIn growth" --platform linkedin --reference "@justinwelsh" --research-service brave --image-provider fal

# Dry run (text only)
/carousel-new --topic "AI SEO tips" --platform instagram --dry-run
```

### Platform Options

| Platform | Aspect Ratio | Video Support |
|----------|--------------|---------------|
| instagram | 1:1 or 4:5 | Yes (loop 5s) |
| meta-ads | 1:1, 4:5, or 9:16 | Optional |
| facebook | 1:1 | Optional |
| linkedin | 1:1 or 16:9 | Not recommended |

### Research Services

| Service | API Key | Description |
|---------|---------|-------------|
| tavily | `TAVILY_API_KEY` | Web research, competitor analysis |
| brave | `BRAVE_API_KEY` | Privacy-focused web search |

### Image Generation Providers

| Provider | API Key | Description |
|----------|---------|-------------|
| kie | `KIE_API_KEY` | Fast, high-quality (recommended) |
| openrouter | `OPENROUTER_API_KEY` | Flux, Stable Diffusion, more |
| fal | `FAL_API_KEY` | Fast inference |
| local | `LOCAL_MODEL` | Ollama with image models |

## /carousel-publish

Publishes a ready carousel.

### Syntax

```bash
/carousel-publish --session-id ~/.hermes/frameforge/sessions/{timestamp}/
```

### Examples

```bash
/carousel-publish --session-id ~/.hermes/frameforge/sessions/2025-01-15-143022/
```

## Implementation via delegate_task

When you run:

```
/carousel-new --topic "X" --platform instagram
```

It delegates to `skills/director-carusel/`, which then:

```python
delegate_task(
    goal="Research Instagram carousel topic: {topic}",
    skills=["carusel-researcher"],
    context=f"""
    Topic: {topic}
    Platform: {platform}
    Reference: {reference}
    CTA: {cta}
    Audience: {audience}
    Research service: {research_service}
    Session root: {SESSION_ROOT}
    """,
    toolsets=["web", "file"]
)
```

Each subagent uses `delegate_task` for the next step.

## Session Structure

Each session is stored at `~/.hermes/frameforge/sessions/{timestamp}/`:

```
├── 00-brief.md          # Initial brief
├── 01-research.md       # Research report
├── 02-copy.md           # Copy for 9 slides
├── 03-design.md         # Visual system
├── 04-prompts.md        # Image generation prompts
├── 05-master.png        # Master image
├── 06-slices/           # 9 sliced slides
├── 07-motion.md         # Animation scenario
├── 08-anim-01.mp4       # Video slide-01
├── 09-qa.md             # QA report
├── 10-upload.json       # Uploaded asset URLs
├── 11-publish.md        # Publish result
└── fragments/           # Summary fragments
```

## Platform-Specific Notes

### Instagram
- Requires Instagram MCP or Make automation
- Video animation for slide-01 is recommended
- Hashtag optimization is important

### Meta Ads
- Requires Meta Ads API access
- Aspect ratio flexibility (1:1, 4:5, 9:16)
- Compliance with ad policies

### Facebook
- Requires Facebook API access
- Square format only (1:1)
- Organic posting focus

### LinkedIn
- Requires LinkedIn API access
- Professional tone
- Limited video support