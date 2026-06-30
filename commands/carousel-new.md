---
name: carousel-new
description: Create new social media carousel via Karuselka pipeline
version: 1.0.0
author: zaharenok
---

# /carousel-new

Creates a new social media carousel (9 slides, 3×3 grid) through the agent pipeline.

## Usage

```
/carousel-new --topic "AI marketing tips" --platform instagram --reference "@neilpatel" --cta "Download guide"
```

## Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--topic` | Yes | Carousel topic | `--topic "AI automation"` |
| `--platform` | Yes | Platform (instagram, meta-ads, facebook, linkedin) | `--platform instagram` |
| `--reference` | No | Reference account | `--reference "@garyvee"` |
| `--cta` | No | Call-to-action | `--cta "Book free audit"` |
| `--audience` | No | Target audience | `--audience "B2B founders"` |
| `--research-service` | No | Research service (tavily, brave) | `--research-service tavily` |
| `--image-provider` | No | Image gen provider (kie, openrouter, fal, local) | `--image-provider kie` |

## Options

| Option | Description |
|--------|-------------|
| `--auto-publish` | Publish after QA (requires platform API) |
| `--dry-run` | Skip image/video generation, text only |
| `--skip-upload` | Skip asset upload |
| `--session-id` | Use existing session path |

## Platform Formats

### Instagram
- Grid: 3×3
- Aspect ratio: 1:1 or 4:5
- Dimensions: 1080×1080 or 1080×1350 per slide
- Video: Loop 5s for slide-01

### Meta Ads
- Grid: 3×3
- Aspect ratio: 1:1, 4:5, or 9:16
- Dimensions: 1080×1080, 1080×1350, or 1080×1920 per slide
- Video: Optional for slide-01

### Facebook
- Grid: 3×3
- Aspect ratio: 1:1
- Dimensions: 1080×1080 per slide
- Video: Optional

### LinkedIn
- Grid: 3×3
- Aspect ratio: 1:1 or 16:9
- Dimensions: 1080×1080 or 1200×627 per slide
- Video: Not recommended

## Research Services

### Tavily (primary)
```bash
--research-service tavily
```
- Web research, competitor analysis, trend detection
- Requires: `TAVILY_API_KEY` in `.env`

### Brave Search (alternative)
```bash
--research-service brave
```
- Privacy-focused web search
- Requires: `BRAVE_API_KEY` in `.env`

## Image Generation Providers

### Kie.ai (recommended)
```bash
--image-provider kie
```
- Fast, high-quality generation
- Requires: `KIE_API_KEY` in `.env`
- Get started with: https://kie.ai?ref=80779f6a33a1f5311277ef1c44c0f665

### OpenRouter
```bash
--image-provider openrouter
```
- Access to Flux, Stable Diffusion, and more
- Requires: `OPENROUTER_API_KEY` in `.env`

### fal.ai
```bash
--image-provider fal
```
- Fast inference
- Requires: `FAL_API_KEY` in `.env`

### Local
```bash
--image-provider local
```
- Ollama with supported image models
- Requires: `ollama serve` running
- Model: `LOCAL_MODEL` in `.env`

## Pipeline

1. **Init**: Create session at `~/.hermes/karuselka/sessions/{timestamp}/`
2. **Research**: Delegate `carusel-researcher` → research via Tavily/Brave
3. **Copy**: Delegate `carusel-copywriter` → text for 9 slides + caption
4. **Design**: Delegate `carusel-designer` → visual system
5. **Image Prompt**: Delegate `carusel-image-prompter` → image gen prompts
6. **Generate**: Generate master image via `scripts/image_gen.py`
7. **Slice**: Slice master image into 9 slides via `scripts/slice_grid.py`
8. **Motion**: Create animation scenario via `carusel-motion-director`
9. **Animate**: Generate video for slide-01 via `scripts/video_gen.py`
10. **QA**: Check design, bleed, aspect ratio via `carusel-design-guardian`
11. **Upload**: Upload assets to storage via `scripts/upload_carousel_assets.py`
12. **Publish**: Publish via MCP (if `--auto-publish`)

## Examples

### Instagram carousel
```bash
/carousel-new --topic "AI automation tools" --platform instagram --reference "@neilpatel"
```

### Meta Ads carousel
```bash
/carousel-new --topic "Facebook ads strategy" --platform meta-ads --reference "@garyvee" --cta "Book audit"
```

### LinkedIn carousel (dry run)
```bash
/carousel-new --topic "LinkedIn growth" --platform linkedin --reference "@justinwelsh" --dry-run
```

### With Brave Search and fal.ai
```bash
/carousel-new --topic "AI SEO tips" --platform instagram --research-service brave --image-provider fal
```

## Output Files

Session created at `~/.hermes/karuselka/sessions/{timestamp}/`:

```
├── 00-brief.md          # Brief
├── 01-research.md       # Research
├── 02-copy.md           # Copy
├── 03-design.md         # Design
├── 04-prompts.md        # Prompts
├── 05-master.png        # Master image
├── 06-slices/           # 9 slides
│   ├── slide-01.png
│   ├── slide-02.png
│   └── ...
├── 07-motion.md         # Motion scenario
├── 08-anim-01.mp4       # Video slide-01
├── 09-qa.md             # QA report
├── 10-upload.json       # Asset URLs
├── 11-publish.md        # Publish result
└── fragments/           # Summary fragments
```

## Environment Variables

```bash
# Research
TAVILY_API_KEY=tvly-...
BRAVE_API_KEY=...

# Image Generation
IMAGE_GEN_PROVIDER=kie
KIE_API_KEY=...
OPENROUTER_API_KEY=...
FAL_API_KEY=...

# Storage
UPLOAD_STORAGE=kie
S3_BUCKET=...

# Platform APIs
INSTAGRAM_MCP_ENDPOINT=http://localhost:3000
META_ADS_ACCOUNT_ID=...

# Session Storage
SESSION_ROOT=~/.hermes/karuselka/sessions
```

## After Creation

To publish:
```bash
/carousel-publish --session-id ~/.hermes/karuselka/sessions/{timestamp}/
```