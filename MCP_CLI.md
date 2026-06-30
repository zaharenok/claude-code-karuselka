# FrameForge MCP & CLI

## MCP Server

FrameForge provides an MCP server for integration with Hermes Agent and other MCP-compatible agents.

### Installation

```bash
# Install MCP server dependencies
pip install -r mcp_requirements.txt

# Add MCP server to Hermes config
# Edit ~/.hermes/config.yaml:
```

```yaml
mcp_servers:
  frameforge:
    command: python
    args: ["/path/to/frameforge/mcp_server.py"]
    env:
      FRAMEFORGE_SESSION_ROOT: "~/.hermes/frameforge/sessions"
```

### MCP Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_carousel` | Create new carousel session | topic, platform, reference, cta, audience, research_service, image_provider, dry_run |
| `publish_carousel` | Publish ready carousel | session_id |
| `get_carousel_status` | Get session status | session_id |
| `list_carousel_sessions` | List all sessions | limit, platform |
| `get_carousel_assets` | Get asset URLs | session_id |

### MCP Usage Example

```python
# In Hermes Agent session
# Create carousel
mcp_frameforge_create_carousel(
    topic="AI marketing tips",
    platform="instagram",
    reference="@neilpatel",
    image_provider="kie"
)

# Get status
mcp_frameforge_get_carousel_status(session_id="20250115-143022")

# List sessions
mcp_frameforge_list_carousel_sessions(limit=10)

# Get assets
mcp_frameforge_get_carousel_assets(session_id="20250115-143022")

# Publish
mcp_frameforge_publish_carousel(session_id="20250115-143022")
```

## CLI

FrameForge provides a command-line interface for manual carousel creation and management.

### Installation

```bash
# Install CLI
pip install -e .

# Or run directly
python frameforge.py --help
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `create` | Create new carousel session |
| `status` | Get carousel session status |
| `list` | List all carousel sessions |
| `assets` | Get carousel asset URLs |
| `publish` | Publish carousel session |

### CLI Usage Examples

```bash
# Create new carousel
frameforge create --topic "AI marketing tips" --platform instagram

# Create with reference and CTA
frameforge create \
  --topic "Facebook ads strategy" \
  --platform meta-ads \
  --reference "@garyvee" \
  --cta "Book free audit"

# Create dry run (text only)
frameforge create --topic "AI SEO tips" --platform instagram --dry-run

# Get session status
frameforge status --session-id 20250115-143022

# List all sessions
frameforge list --limit 10

# List Instagram sessions only
frameforge list --platform instagram --limit 10

# Get asset URLs
frameforge assets --session-id 20250115-143022

# Publish carousel
frameforge publish --session-id 20250115-143022
```

### CLI Command Reference

#### create

Create a new carousel session.

```bash
frameforge create --topic TOPIC --platform PLATFORM [OPTIONS]
```

**Required:**
- `--topic`: Carousel topic
- `--platform`: Target platform (instagram, meta-ads, facebook, linkedin)

**Optional:**
- `--reference`: Reference account (e.g., @neilpatel)
- `--cta`: Call-to-action
- `--audience`: Target audience
- `--research-service`: Research service (tavily, brave)
- `--image-provider`: Image generation provider (kie, openrouter, fal, local)
- `--video-provider`: Video generation provider (seedance, grok, fal)
- `--dry-run`: Skip image/video generation, text only
- `--auto-publish`: Publish after QA

#### status

Get carousel session status.

```bash
frameforge status --session-id SESSION_ID
```

Shows completion status of all pipeline steps.

#### list

List carousel sessions.

```bash
frameforge list [OPTIONS]
```

**Optional:**
- `--limit`: Maximum sessions to show (default: 10)

#### assets

Get carousel asset URLs.

```bash
frameforge assets --session-id SESSION_ID
```

Shows URLs for all 9 slides and video (if generated).

#### publish

Publish carousel session.

```bash
frameforge publish --session-id SESSION_ID
```

Triggers platform-specific publish via MCP or API.

## Environment Variables

Both MCP server and CLI use these environment variables:

```bash
# Session storage
FRAMEFORGE_SESSION_ROOT=~/.hermes/frameforge/sessions

# Research services
TAVILY_API_KEY=tvly-...
BRAVE_API_KEY=...

# Image generation
IMAGE_GEN_PROVIDER=kie
KIE_API_KEY=...
OPENROUTER_API_KEY=...
FAL_API_KEY=...

# Video generation
VIDEO_GEN_PROVIDER=seedance
GROK_VIDEO_API_KEY=...

# Upload storage
UPLOAD_STORAGE=kie
S3_BUCKET=...
S3_REGION=us-east-1
```

## Integration Examples

### Hermes Agent Integration

Add to Hermes config:

```yaml
mcp_servers:
  frameforge:
    command: python
    args: ["/path/to/frameforge/mcp_server.py"]
    env:
      FRAMEFORGE_SESSION_ROOT: "~/.hermes/frameforge/sessions"
      KIE_API_KEY: "${KIE_API_KEY}"
```

Use in agent sessions:

```python
# Create carousel
mcp_frameforge_create_carousel(
    topic="AI marketing automation",
    platform="instagram",
    reference="@neilpatel"
)
```

### Standalone CLI Usage

For manual carousel creation or automation scripts:

```bash
# Create and track
SESSION_ID=$(frameforge create --topic "X" --platform instagram --dry-run | grep "Session ID" | cut -d: -f2 | xargs)

# Monitor progress
while true; do
  frameforge status --session-id $SESSION_ID
  sleep 10
done

# Get assets when done
frameforge assets --session-id $SESSION_ID
```

### Cron Job Integration

Schedule carousel creation:

```bash
# Daily carousel creation at 10 AM
0 10 * * * cd /path/to/frameforge && frameforge create --topic "Daily tip" --platform instagram --auto-publish >> /var/log/frameforge.log 2>&1
```

## Troubleshooting

### MCP Server Not Starting

Check Python dependencies:
```bash
pip install -r mcp_requirements.txt
```

Check Hermes config:
```bash
hermes config get mcp_servers.frameforge
```

### CLI Not Found

Install in development mode:
```bash
pip install -e .
```

Or run directly:
```bash
python /path/to/frameforge/frameforge.py --help
```

### Session Not Found

Use full session ID or timestamp:
```bash
# Use full timestamp
frameforge status --session-id 20250115-143022

# Or partial match
frameforge status --session-id 143022
```

## Next Steps

- See [README.md](README.md) for full FrameForge documentation
- See [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for roadmap
- See [AGENT-PIPELINE.md](AGENT-PIPELINE.md) for pipeline details