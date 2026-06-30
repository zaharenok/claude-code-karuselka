#!/usr/bin/env python3
"""
FrameForge MCP Server
Provides MCP tools for social media carousel creation via Hermes agents.
"""

import json
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import sys

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP server not available. Install with: pip install mcp")
    sys.exit(1)

# Import FrameForge modules
# from image_gen import ImageGenerator
# from slice_grid import slice_grid

# Initialize MCP server
server = Server("frameforge")

@server.list_tools()
async def list_tools() -> List[Tool]:
    """List available FrameForge tools."""
    return [
        Tool(
            name="create_carousel",
            description=(
                "Create a new social media carousel (9 slides, 3×3 grid) "
                "through the FrameForge agent pipeline. "
                "Supports: instagram, meta-ads, facebook, linkedin"
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Carousel topic (e.g., 'AI marketing tips')"
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["instagram", "meta-ads", "facebook", "linkedin"],
                        "description": "Target platform"
                    },
                    "reference": {
                        "type": "string",
                        "description": "Reference account (e.g., '@neilpatel')"
                    },
                    "cta": {
                        "type": "string",
                        "description": "Call-to-action (e.g., 'Download guide')"
                    },
                    "audience": {
                        "type": "string",
                        "description": "Target audience (e.g., 'B2B founders')"
                    },
                    "research_service": {
                        "type": "string",
                        "enum": ["tavily", "brave"],
                        "default": "tavily",
                        "description": "Research service to use"
                    },
                    "image_provider": {
                        "type": "string",
                        "enum": ["kie", "openrouter", "fal", "local"],
                        "default": "kie",
                        "description": "Image generation provider"
                    },
                    "dry_run": {
                        "type": "boolean",
                        "default": False,
                        "description": "Skip image/video generation, text only"
                    }
                },
                "required": ["topic", "platform"]
            }
        ),
        Tool(
            name="publish_carousel",
            description=(
                "Publish a ready carousel session to the target platform. "
                "Requires platform API credentials configured."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID (timestamp-based or path)"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="get_carousel_status",
            description=(
                "Get the status of a carousel creation session. "
                "Returns current step and completion status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID (timestamp-based or path)"
                    }
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="list_carousel_sessions",
            description=(
                "List all carousel creation sessions. "
                "Returns session IDs, topics, platforms, and completion status."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "default": 10,
                        "description": "Maximum number of sessions to return"
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["instagram", "meta-ads", "facebook", "linkedin"],
                        "description": "Filter by platform"
                    }
                }
            }
        ),
        Tool(
            name="get_carousel_assets",
            description=(
                "Get uploaded asset URLs for a carousel session. "
                "Returns URLs for all 9 slides and video (if generated)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "Session ID (timestamp-based or path)"
                    }
                },
                "required": ["session_id"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""

    if name == "create_carousel":
        return await create_carousel_tool(**arguments)
    elif name == "publish_carousel":
        return await publish_carousel_tool(**arguments)
    elif name == "get_carousel_status":
        return await get_carousel_status_tool(**arguments)
    elif name == "list_carousel_sessions":
        return await list_carousel_sessions_tool(**arguments)
    elif name == "get_carousel_assets":
        return await get_carousel_assets_tool(**arguments)
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def create_carousel_tool(
    topic: str,
    platform: str,
    reference: Optional[str] = None,
    cta: Optional[str] = None,
    audience: Optional[str] = None,
    research_service: str = "tavily",
    image_provider: str = "kie",
    dry_run: bool = False
) -> List[TextContent]:
    """Create a new carousel session."""

    # Check if running in Hermes environment
    try:
        import os
        session_root = Path(os.getenv("FRAMEFORGE_SESSION_ROOT", "~/.hermes/frameforge/sessions"))
        session_root = session_root.expanduser()

        # Create session directory
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        session_path = session_root / timestamp
        session_path.mkdir(parents=True, exist_ok=True)

        # Write brief
        brief_content = f"""# Carousel Brief

## Topic
{topic}

## Platform
{platform}

## Reference Account
{reference or 'Not specified'}

## Target Audience
{audience or 'Not specified'}

## CTA
{cta or 'Not specified'}

## Configuration
- Research Service: {research_service}
- Image Provider: {image_provider}
- Dry Run: {dry_run}

## Created
{datetime.now().isoformat()}
"""
        (session_path / "00-brief.md").write_text(brief_content)

        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "created",
                "session_id": timestamp,
                "session_path": str(session_path),
                "message": f"Carousel session created. Session ID: {timestamp}"
            }, indent=2)
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
        )]


async def publish_carousel_tool(session_id: str) -> List[TextContent]:
    """Publish a carousel session."""

    try:
        import os
        session_root = Path(os.getenv("FRAMEFORGE_SESSION_ROOT", "~/.hermes/frameforge/sessions"))
        session_root = session_root.expanduser()

        # Find session
        session_path = session_root / session_id
        if not session_path.exists():
            # Try to find by timestamp
            session_path = next(session_root.glob(f"*{session_id}*"), None)
            if not session_path:
                raise ValueError(f"Session not found: {session_id}")

        # Check if session is ready to publish
        upload_json = session_path / "10-upload.json"
        if not upload_json.exists():
            raise ValueError(f"Session not ready to publish. Upload file missing.")

        # Read upload URLs
        with open(upload_json) as f:
            upload_data = json.load(f)

        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "ready_to_publish",
                "session_id": session_id,
                "assets": upload_data,
                "message": "Session ready to publish. Use platform-specific publish API."
            }, indent=2)
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
        )]


async def get_carousel_status_tool(session_id: str) -> List[TextContent]:
    """Get carousel session status."""

    try:
        import os
        session_root = Path(os.getenv("FRAMEFORGE_SESSION_ROOT", "~/.hermes/frameforge/sessions"))
        session_root = session_root.expanduser()

        # Find session
        session_path = session_root / session_id
        if not session_path.exists():
            session_path = next(session_root.glob(f"*{session_id}*"), None)
            if not session_path:
                raise ValueError(f"Session not found: {session_id}")

        # Check completion status
        steps = [
            ("01-research.md", "research"),
            ("02-copy.md", "copy"),
            ("03-design.md", "design"),
            ("04-prompts.md", "prompts"),
            ("05-master.png", "master_image"),
            ("06-slices/slide-01.png", "slices"),
            ("07-motion.md", "motion"),
            ("08-anim-01.mp4", "video"),
            ("09-qa.md", "qa"),
            ("10-upload.json", "upload"),
            ("11-publish.md", "publish")
        ]

        completed_steps = []
        for filename, step_name in steps:
            if (session_path / filename).exists():
                completed_steps.append(step_name)

        status = {
            "session_id": session_id,
            "completed_steps": completed_steps,
            "total_steps": len(steps),
            "progress": len(completed_steps) / len(steps) * 100,
            "status": "completed" if len(completed_steps) == len(steps) else "in_progress"
        }

        return [TextContent(
            type="text",
            text=json.dumps(status, indent=2)
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
        )]


async def list_carousel_sessions_tool(
    limit: int = 10,
    platform: Optional[str] = None
) -> List[TextContent]:
    """List carousel sessions."""

    try:
        import os
        session_root = Path(os.getenv("FRAMEFORGE_SESSION_ROOT", "~/.hermes/frameforge/sessions"))
        session_root = session_root.expanduser()

        if not session_root.exists():
            return [TextContent(
                type="text",
                text=json.dumps({"sessions": []}, indent=2)
            )]

        # List sessions
        sessions = []
        for session_path in sorted(session_root.iterdir(), reverse=True)[:limit]:
            if not session_path.is_dir():
                continue

            # Read brief
            brief_path = session_path / "00-brief.md"
            if not brief_path.exists():
                continue

            with open(brief_path) as f:
                brief_content = f.read()

            # Parse platform from brief
            session_platform = None
            for line in brief_content.split("\n"):
                if line.startswith("## Platform"):
                    session_platform = line.split("## Platform")[-1].strip()
                    break

            # Filter by platform
            if platform and session_platform != platform:
                continue

            # Check completion
            steps = [
                "01-research.md", "02-copy.md", "03-design.md", "04-prompts.md",
                "05-master.png", "11-publish.md"
            ]
            completed = sum(1 for step in steps if (session_path / step).exists())

            sessions.append({
                "session_id": session_path.name,
                "platform": session_platform,
                "completed_steps": completed,
                "total_steps": len(steps),
                "status": "completed" if completed == len(steps) else "in_progress"
            })

        return [TextContent(
            type="text",
            text=json.dumps({"sessions": sessions}, indent=2)
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
        )]


async def get_carousel_assets_tool(session_id: str) -> List[TextContent]:
    """Get carousel session asset URLs."""

    try:
        import os
        session_root = Path(os.getenv("FRAMEFORGE_SESSION_ROOT", "~/.hermes/frameforge/sessions"))
        session_root = session_root.expanduser()

        # Find session
        session_path = session_root / session_id
        if not session_path.exists():
            session_path = next(session_root.glob(f"*{session_id}*"), None)
            if not session_path:
                raise ValueError(f"Session not found: {session_id}")

        # Read upload URLs
        upload_json = session_path / "10-upload.json"
        if not upload_json.exists():
            raise ValueError(f"Assets not uploaded yet. Session ID: {session_id}")

        with open(upload_json) as f:
            upload_data = json.load(f)

        return [TextContent(
            type="text",
            text=json.dumps({
                "session_id": session_id,
                "assets": upload_data
            }, indent=2)
        )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "error",
                "error": str(e)
            }, indent=2)
        )]


async def main():
    """Start MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())