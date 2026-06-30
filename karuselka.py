#!/usr/bin/env python3
"""
Karuselka CLI
Command-line interface for social media carousel creation.
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

try:
    from image_gen import ImageGenerator
    from slice_grid import slice_grid
except ImportError:
    print("Warning: Some modules not available. Install dependencies with: pip install -r scripts/requirements.txt")


class KaruselkaCLI:
    """Karuselka CLI handler."""

    def __init__(self):
        self.session_root = Path(os.getenv("KARUSELKA_SESSION_ROOT", "~/.hermes/karuselka/sessions"))
        self.session_root = self.session_root.expanduser()

    def create_carousel(self, args):
        """Create a new carousel session."""
        # Create session directory
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        session_path = self.session_root / timestamp
        session_path.mkdir(parents=True, exist_ok=True)

        # Write brief
        brief_content = f"""# Carousel Brief

## Topic
{args.topic}

## Platform
{args.platform}

## Reference Account
{args.reference or 'Not specified'}

## Target Audience
{args.audience or 'Not specified'}

## CTA
{args.cta or 'Not specified'}

## Configuration
- Research Service: {args.research_service}
- Image Provider: {args.image_provider}
- Video Provider: {args.video_provider}
- Dry Run: {args.dry_run}
- Auto Publish: {args.auto_publish}

## Created
{datetime.now().isoformat()}
"""
        (session_path / "00-brief.md").write_text(brief_content)

        print(f"✓ Carousel session created")
        print(f"  Session ID: {timestamp}")
        print(f"  Session Path: {session_path}")
        print(f"  Topic: {args.topic}")
        print(f"  Platform: {args.platform}")

        if args.dry_run:
            print(f"\n📝 Dry run mode: text generation only (skips image/video)")

        return timestamp

    def get_status(self, args):
        """Get carousel session status."""
        # Find session
        session_path = self.session_root / args.session_id
        if not session_path.exists():
            # Try to find by timestamp
            session_path = next(self.session_root.glob(f"*{args.session_id}*"), None)
            if not session_path:
                print(f"❌ Session not found: {args.session_id}")
                return

        # Check completion status
        steps = [
            ("01-research.md", "Research", "🔍"),
            ("02-copy.md", "Copywriting", "✍️"),
            ("03-design.md", "Design", "🎨"),
            ("04-prompts.md", "Image Prompts", "📝"),
            ("05-master.png", "Master Image", "🖼️"),
            ("06-slices/slide-01.png", "Slices (9 slides)", "✂️"),
            ("07-motion.md", "Motion Scenario", "🎬"),
            ("08-anim-01.mp4", "Video Generation", "🎥"),
            ("09-qa.md", "QA Checks", "✅"),
            ("10-upload.json", "Asset Upload", "☁️"),
            ("11-publish.md", "Publish", "🚀")
        ]

        completed_steps = []
        print(f"📊 Carousel Status: {args.session_id}")
        print()

        for filename, step_name, emoji in steps:
            if (session_path / filename).exists():
                completed_steps.append(step_name)
                print(f"  {emoji} {step_name}: ✓")
            else:
                print(f"  {emoji} {step_name}: ○")

        print()
        progress = len(completed_steps) / len(steps) * 100
        print(f"Progress: {len(completed_steps)}/{len(steps)} steps ({progress:.0f}%)")

        if len(completed_steps) == len(steps):
            print(f"Status: ✅ Completed")
        else:
            print(f"Status: 🔄 In Progress")

        # Show next step
        if len(completed_steps) < len(steps):
            next_step = steps[len(completed_steps)]
            print(f"Next: {next_step[1]} ({next_step[2]})")

    def list_sessions(self, args):
        """List carousel sessions."""
        if not self.session_root.exists():
            print("No sessions found.")
            return

        # List sessions
        sessions = []
        for session_path in sorted(self.session_root.iterdir(), reverse=True)[:args.limit]:
            if not session_path.is_dir():
                continue

            # Read brief
            brief_path = session_path / "00-brief.md"
            if not brief_path.exists():
                continue

            with open(brief_path) as f:
                brief_content = f.read()

            # Parse topic and platform from brief
            topic = "Unknown"
            platform = "Unknown"
            for line in brief_content.split("\n"):
                if line.startswith("## Topic"):
                    topic = line.split("## Topic")[-1].strip()
                elif line.startswith("## Platform"):
                    platform = line.split("## Platform")[-1].strip()

            # Check completion
            steps = [
                "01-research.md", "02-copy.md", "03-design.md", "04-prompts.md",
                "05-master.png", "11-publish.md"
            ]
            completed = sum(1 for step in steps if (session_path / step).exists())

            sessions.append({
                "id": session_path.name,
                "topic": topic,
                "platform": platform,
                "completed": completed,
                "total": len(steps),
                "status": "✅" if completed == len(steps) else "🔄"
            })

        if not sessions:
            print("No sessions found.")
            return

        print(f"📋 Carousel Sessions (last {len(sessions)})\n")
        print(f"{'ID':<20} {'Platform':<12} {'Topic':<30} {'Status':<4}")
        print("-" * 80)

        for session in sessions:
            print(f"{session['id']:<20} {session['platform']:<12} {session['topic'][:30]:<30} {session['status']:<4}")

        print()
        print(f"Total: {len(sessions)} session(s)")

    def get_assets(self, args):
        """Get carousel session asset URLs."""
        # Find session
        session_path = self.session_root / args.session_id
        if not session_path.exists():
            # Try to find by timestamp
            session_path = next(self.session_root.glob(f"*{args.session_id}*"), None)
            if not session_path:
                print(f"❌ Session not found: {args.session_id}")
                return

        # Read upload URLs
        upload_json = session_path / "10-upload.json"
        if not upload_json.exists():
            print(f"❌ Assets not uploaded yet. Session ID: {args.session_id}")
            return

        with open(upload_json) as f:
            upload_data = json.load(f)

        print(f"📦 Asset URLs: {args.session_id}\n")

        if "slides" in upload_data:
            print("Slides:")
            for i, url in enumerate(upload_data["slides"], 1):
                print(f"  Slide {i:02d}: {url}")

        if "video" in upload_data:
            print(f"\nVideo:\n  {upload_data['video']}")

        if "upload_timestamp" in upload_data:
            print(f"\nUploaded: {upload_data['upload_timestamp']}")

    def publish(self, args):
        """Publish a carousel session."""
        # Find session
        session_path = self.session_root / args.session_id
        if not session_path.exists():
            # Try to find by timestamp
            session_path = next(self.session_root.glob(f"*{args.session_id}*"), None)
            if not session_path:
                print(f"❌ Session not found: {args.session_id}")
                return

        # Check if session is ready to publish
        upload_json = session_path / "10-upload.json"
        if not upload_json.exists():
            print(f"❌ Session not ready to publish. Upload file missing.")
            print(f"   Run 'karuselka generate' first.")
            return

        # Read upload URLs
        with open(upload_json) as f:
            upload_data = json.load(f)

        print(f"🚀 Publishing carousel: {args.session_id}")
        print(f"\nAssets to publish:")

        if "slides" in upload_data:
            print(f"  Slides: {len(upload_data['slides'])}")
        if "video" in upload_data:
            print(f"  Video: 1")

        print(f"\nNote: Platform-specific publish API required.")
        print(f"  Configure platform API credentials in .env")

        # Check if publish already happened
        publish_md = session_path / "11-publish.md"
        if publish_md.exists():
            print(f"\n⚠️  Carousel already published on:")
            with open(publish_md) as f:
                print(f.read())
        else:
            print(f"\nTo publish, use platform-specific MCP or API integration.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Karuselka - Social Media Carousel CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create new carousel
  karuselka create --topic "AI marketing tips" --platform instagram

  # Create with reference and CTA
  karuselka create --topic "Facebook ads" --platform meta-ads --reference "@garyvee" --cta "Book audit"

  # Get session status
  karuselka status --session-id 20250115-143022

  # List all sessions
  karuselka list --limit 10

  # Get asset URLs
  karuselka assets --session-id 20250115-143022

  # Publish carousel
  karuselka publish --session-id 20250115-143022
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create new carousel session")
    create_parser.add_argument("--topic", required=True, help="Carousel topic")
    create_parser.add_argument("--platform", required=True, choices=["instagram", "meta-ads", "facebook", "linkedin"], help="Target platform")
    create_parser.add_argument("--reference", help="Reference account (e.g., @neilpatel)")
    create_parser.add_argument("--cta", help="Call-to-action")
    create_parser.add_argument("--audience", help="Target audience")
    create_parser.add_argument("--research-service", choices=["tavily", "brave"], default="tavily", help="Research service")
    create_parser.add_argument("--image-provider", choices=["kie", "openrouter", "fal", "local"], default="kie", help="Image generation provider")
    create_parser.add_argument("--video-provider", choices=["seedance", "grok", "fal"], default="seedance", help="Video generation provider")
    create_parser.add_argument("--dry-run", action="store_true", help="Skip image/video generation, text only")
    create_parser.add_argument("--auto-publish", action="store_true", help="Publish after QA")

    # Status command
    status_parser = subparsers.add_parser("status", help="Get carousel session status")
    status_parser.add_argument("--session-id", required=True, help="Session ID")

    # List command
    list_parser = subparsers.add_parser("list", help="List carousel sessions")
    list_parser.add_argument("--limit", type=int, default=10, help="Maximum sessions to show")

    # Assets command
    assets_parser = subparsers.add_parser("assets", help="Get carousel asset URLs")
    assets_parser.add_argument("--session-id", required=True, help="Session ID")

    # Publish command
    publish_parser = subparsers.add_parser("publish", help="Publish carousel session")
    publish_parser.add_argument("--session-id", required=True, help="Session ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = KaruselkaCLI()

    if args.command == "create":
        cli.create_carousel(args)
    elif args.command == "status":
        cli.get_status(args)
    elif args.command == "list":
        cli.list_sessions(args)
    elif args.command == "assets":
        cli.get_assets(args)
    elif args.command == "publish":
        cli.publish(args)


if __name__ == "__main__":
    main()