# Hermes Agent Configuration

This directory contains Hermes Agent configurations for Karuselka agents.

Each agent is defined as a Hermes skill that can be invoked via `delegate_task`.

## Skills Mapping

| Cursor Agent | Hermes Skill | Description |
|--------------|--------------|-------------|
| director | `skills/director-carusel/` | Orchestrates the pipeline |
| carusel-researcher | `skills/carusel-researcher/` | Research via Tavily/Brave |
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
cd karuselka
hermes skills add skills/director-carusel/
hermes skills add skills/carusel-researcher/
hermes skills add skills/carusel-copywriter/
# ... etc
```

## Usage

### Via delegate_task

```python
delegate_task(
    goal="Create Instagram carousel on topic X",
    skills=["director-carusel"],
    context="Topic, platform, reference, etc.",
    toolsets=["web", "file"]
)
```

### Via slash commands

```
/carousel-new --topic "AI marketing" --platform instagram --reference "@user"
/carousel-publish --session-id path/to/session
```

## Service Integrations

### Research
- **Tavily MCP**: Primary research via `mcp_tavily_remote_tavily_research()`
- **Brave Search**: Alternative via `mcp_tavily_remote_tavily_search()`

### Image Generation
- **Kie.ai**: Via `scripts/image_gen.py` with `IMAGE_GEN_PROVIDER=kie`
- **OpenRouter**: Via `scripts/image_gen.py` with `IMAGE_GEN_PROVIDER=openrouter`
- **fal.ai**: Via `scripts/image_gen.py` with `IMAGE_GEN_PROVIDER=fal`
- **Local**: Via `scripts/image_gen.py` with `IMAGE_GEN_PROVIDER=local`

### Video Generation
- **Seedance 1.5 Pro (ByteDance)**: Via `scripts/seedance_video_gen.py` — cheapest option on Kie.ai ($0.0175/s, 720p, no audio)
- **Grok Video**: Via `scripts/grok_video_gen.py` (requires separate GROK_API_KEY)
- **fal.ai**: Via `scripts/video_gen.py` with `VIDEO_GEN_PROVIDER=fal`

### Upload Storage
- **Kie.ai**: Via `scripts/upload_carousel_assets.py` with `UPLOAD_STORAGE=kie`
- **S3**: Via `scripts/upload_carousel_assets.py` with `UPLOAD_STORAGE=s3`
- **Local**: Via `scripts/upload_carousel_assets.py` with `UPLOAD_STORAGE=local`

### Platform Publish
- **Instagram**: Via `skills/carusel-publish/` with Instagram MCP
- **Meta Ads**: Via `skills/carusel-publish/` with Meta Ads API
- **Facebook**: Via `skills/carusel-publish/` with Facebook API
- **LinkedIn**: Via `skills/carusel-publish/` with LinkedIn API

## Platform-Specific Formats

| Platform | Aspect Ratio | Dimensions |
|----------|--------------|------------|
| Instagram | 1:1 or 4:5 | 1080×1080 or 1080×1350 |
| Meta Ads | 1:1, 4:5, or 9:16 | 1080×1080, 1080×1350, or 1080×1920 |
| Facebook | 1:1 | 1080×1080 |
| LinkedIn | 1:1 or 16:9 | 1080×1080 or 1200×627 |

## Environment Variables

See `.env.example` for full configuration.

Key variables:
- `TAVILY_API_KEY`: Research (required)
- `BRAVE_API_KEY`: Alternative research (optional)
- `IMAGE_GEN_PROVIDER`: kie, openrouter, fal, or local
- `VIDEO_GEN_PROVIDER`: grok or fal
- `UPLOAD_STORAGE`: kie, s3, or local
- `SESSION_ROOT`: Session storage path