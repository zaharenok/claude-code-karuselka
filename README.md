# Karuselka

Agent system for creating social media carousels: research, copy, design, image/video generation, QA, upload, and publish.

Supported platforms: Instagram, Meta Ads, Facebook, LinkedIn.

## Quick Start

```bash
git clone https://github.com/zaharenok/claude-code-karuselka.git
cd claude-code-karuselka
pip install -r scripts/requirements.txt
cp .env.example .env  # Add your API keys
```

Create a carousel:
```bash
/carousel-new --topic "AI marketing tips" --platform instagram --reference "@neilpatel"
```

Publish:
```bash
/carousel-publish --session-id ~/.hermes/karuselka/sessions/{timestamp}/
```

## Features
## Features
- **Multi-platform**: Instagram, Meta Ads, Facebook, LinkedIn
- **Full pipeline**: Research → Copy → Design → Image/Video generation → QA → Upload → Publish
- **Research integration**: Tavily MCP, Brave Search
- **Image generation**: Kie.ai, OpenRouter, fal.ai, local models
- **Video generation**: Seedance 1.5 Pro (ByteDance), Grok Video, fal.ai
- **Storage**: Kie.ai, S3, local
- **Hermes integration**: Slash commands, delegate_task orchestration, MCP server
- **CLI**: Command-line interface for manual carousel creation

## Architecture

Karuselka uses Hermes Agent orchestration with specialized subagents:

| Agent | Role | Tools |
|-------|------|-------|
| researcher | Market research, competitor analysis | Tavily MCP, Brave Search |
| copywriter | 9-slide copy + caption + CTA | — |
| designer | Visual system 3×3 grid | — |
| image-prompter | Image generation prompts | — |
| slice | Master image generation + slicing | Kie.ai / OpenRouter / fal.ai / local |
| motion-director | Animation scenario | — |
| animate | Loop video for slide-01 | Grok Video / fal.ai |
| design-guardian | QA: design, bleed, aspect ratio | — |
| upload | Asset upload to HTTPS storage | Kie.ai / S3 / local |
| publish | Publish via MCP | Instagram / Meta Ads / Facebook / LinkedIn |
| fixic | Incident resolution | — |

## Pipeline

```
research → copy → design → image-prompt → generate → slice → motion → animate → QA → upload → publish → fixic
```

Full details in [AGENT-PIPELINE.md](AGENT-PIPELINE.md).

## Supported Services

### Research
- **Tavily MCP**: Web research, competitor analysis, trend detection
- **Brave Search**: Alternative web search with privacy focus

### Image Generation
- **Kie.ai**: Fast image generation (get started with [referral link](https://kie.ai?ref=80779f6a33a1f5311277ef1c44c0f665))
- **OpenRouter**: Access to Flux, Stable Diffusion, and more
- **fal.ai**: Fast inference for image models
- **Local**: Ollama with supported image models

### Video Generation
- **Seedance 1.5 Pro (ByteDance)**: Cheapest option on Kie.ai ($0.0175/s, 720p, 5s loop, no audio) — recommended
- **Grok Video**: Loop video for first slide (requires separate API key)
- **fal.ai**: Alternative video generation

### Upload Storage
- **Kie.ai**: Integrated CDN
- **S3**: AWS S3 or compatible
- **Local**: File system storage

### Publishing
- **Instagram**: Via MCP or Make automation
- **Meta Ads**: Carousel ad creation
- **Facebook**: Organic posts
- **LinkedIn**: Professional posts

## Installation

### Prerequisites
- Python 3.10+
- Claude Code CLI (optional, for native mode)
- Hermes Agent with delegate_task support
- API keys for chosen services

### Setup

1. Clone repository:
```bash
git clone https://github.com/zaharenok/karuselka.git
cd karuselka
```

2. Install Python dependencies:
```bash
pip install -r scripts/requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Install Hermes skills (optional, if not using slash commands):
```bash
hermes skills add skills/director-carusel/
hermes skills add skills/carusel-researcher/
# ... add other skills as needed
```

## Usage

### Create carousel

```bash
/carousel-new --topic "AI marketing tips" --platform instagram --reference "@neilpatel"
```

Parameters:
- `--topic`: Carousel topic (required)
- `--platform`: Platform (instagram, meta-ads, facebook, linkedin)
- `--reference`: Reference account (optional)
- `--cta`: Call-to-action (optional)
- `--audience`: Target audience (optional)
- `--auto-publish`: Publish after QA (optional)
- `--dry-run`: Skip image generation (optional)

### Publish carousel

```bash
/carousel-publish --session-id ~/.hermes/karuselka/sessions/{timestamp}/
```

### Platform-specific options

**Instagram**: Standard 3×3 grid, 1080×1350 (default) or 1080×1080 per slide, video: Seedance 1.5 Pro (5s loop)

**Meta Ads**: Aspect ratios 1080×1350 (default) or 1080×1080, 1080×1920, video: Seedance 1.5 Pro (5s loop, optional)

**Facebook**: 1080×1080 square format, video: Seedance 1.5 Pro (5s loop, optional)

**LinkedIn**: 1080×1080 or 1200×627 (landscape), video: Not recommended

## Session Structure

```
~/.hermes/karuselka/sessions/{timestamp}/
├── 00-brief.md          # Initial brief
├── 01-research.md       # Research report
├── 02-copy.md           # Copy for 9 slides + caption
├── 03-design.md         # Visual system
├── 04-prompts.md        # Image generation prompts
├── 05-master.png        # Master image
├── 06-slices/           # 9 sliced slides
├── 07-motion.md         # Animation scenario
├── 08-anim-01.mp4       # Animated slide-01
├── 09-qa.md             # QA report
├── 10-upload.json       # Uploaded asset URLs
├── 11-publish.md        # Publish result
└── pipeline-fix-queue.md # Incident queue
```

## Configuration

### Research services
```bash
# Tavily MCP (primary)
TAVILY_API_KEY=tvly-...

# Brave Search (alternative)
BRAVE_API_KEY=...
```

### Image generation
```bash
IMAGE_GEN_PROVIDER=kie  # kie, openrouter, fal, local

# Kie.ai (recommended, fast)
KIE_API_KEY=...

# OpenRouter (access to many models)
OPENROUTER_API_KEY=...

# fal.ai (fast inference)
FAL_API_KEY=...

# Local (Ollama)
LOCAL_MODEL=gemma2:latest
```

### Storage
```bash
UPLOAD_STORAGE=kie  # kie, s3, local

# S3 config
S3_BUCKET=your-bucket
S3_REGION=us-east-1
S3_ACCESS_KEY=...
S3_SECRET_KEY=...
```

### Video generation
```bash
VIDEO_GEN_PROVIDER=seedance  # seedance, grok, fal

# Seedance 1.5 Pro (recommended, cheapest on Kie.ai)
# Uses same KIE_API_KEY as image generation
# Cost: $0.0175/s, 720p, 5s loop, no audio

# Grok Video (requires separate API key)
# GROK_API_KEY=...  # Not used with seedance
# GROK_VIDEO_API_KEY=...

# fal.ai (alternative)
# FAL_API_KEY=...
```

### Publishing
```bash
# Instagram MCP
INSTAGRAM_MCP_ENDPOINT=http://localhost:3000
INSTAGRAM_ACCESS_TOKEN=...

# Meta Ads
META_ADS_ACCOUNT_ID=...
META_ADS_ACCESS_TOKEN=...
```

## MCP Server & CLI

Karuselka provides MCP server and CLI for integration:

### MCP Server

Integrate with Hermes Agent and other MCP-compatible agents:

```bash
# Install MCP dependencies
pip install -r mcp_requirements.txt

# Add to Hermes config (~/.hermes/config.yaml)
mcp_servers:
  karuselka:
    command: python
    args: ["/path/to/karuselka/mcp_server.py"]
```

Full documentation: [MCP_CLI.md](MCP_CLI.md)

### CLI

Command-line interface for manual carousel creation:

```bash
# Make executable
chmod +x karuselka.py

# Create carousel
./karuselka.py create --topic "AI marketing" --platform instagram

# Get status
./karuselka.py status --session-id 20250115-143022

# List sessions
./karuselka.py list
```

Full documentation: [MCP_CLI.md](MCP_CLI.md)

## Development

See [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for roadmap.

## Contributing

Contributions welcome! Please read [HERMES_AGENTS.md](HERMES_AGENTS.md) for skill development guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Original [Karuselka](https://github.com/Horosheff/Karuselka) for Cursor
- Hermes Agent framework
- Tavily for research API
- Kie.ai for image generation (get started with [referral link](https://kie.ai?ref=80779f6a33a1f5311277ef1c44c0f665))