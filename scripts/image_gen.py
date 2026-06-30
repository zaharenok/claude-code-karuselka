#!/usr/bin/env python3
"""
Image generation for Karuselka carousel.
Supports Kie.ai, OpenRouter, and local models (Ollama).
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    """Multi-provider image generator."""

    def __init__(self):
        self.provider = os.getenv("IMAGE_GEN_PROVIDER", "kie")
        self.session_root = Path(os.getenv("SESSION_ROOT", "~/.hermes/karuselka/sessions/current"))
        self.session_root = self.session_root.expanduser()

    def generate_master_image(self, prompt: str, style_config: dict) -> Path:
        """
        Generate master image (3:4 @ 4K) for 3×3 grid.

        Args:
            prompt: Image generation prompt
            style_config: Dict with colors, typography, style constraints

        Returns:
            Path to generated master image
        """
        full_prompt = self._build_full_prompt(prompt, style_config)

        if self.provider == "kie":
            return self._generate_via_kie(full_prompt)
        elif self.provider == "openrouter":
            return self._generate_via_openrouter(full_prompt)
        elif self.provider == "local":
            return self._generate_locally(full_prompt)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _build_full_prompt(self, prompt: str, style_config: dict) -> str:
        """Build full prompt with style constraints."""
        colors = style_config.get("colors", {})
        fonts = style_config.get("typography", {})

        full = f"""
{prompt}

## Style Constraints
- Minimalist aesthetic, flat design
- NO gradients, NO drop shadows, NO blur effects
- High contrast ratio (WCAG AA 4.5:1)

## Color Palette
- Background: {colors.get('background', '#FFFFFF')}
- Text: {colors.get('text', '#1A1A1A')}
- Secondary: {colors.get('secondary', '#007AFF')}
- Accent: {colors.get('accent', '#FFD600')}

## Typography
- Headlines: Bold, {fonts.get('headline_size', '48px')}
- Body: Regular, {fonts.get('body_size', '24px')}
- Line height: 1.3

## Composition
- 3×3 grid layout (360×480 px cells)
- Master format: 3:4 aspect ratio (1080×1440 px)
- Center-aligned or left-aligned based on slide function
"""
        return full.strip()

    def _generate_via_kie(self, prompt: str) -> Path:
        """Generate via Kie.ai API."""
        api_key = os.getenv("KIE_API_KEY")
        if not api_key:
            raise ValueError("KIE_API_KEY not set")

        url = "https://api.kie.ai/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": "1080x1440",
            "model": "flux-pro-v1.1"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # Download image
        image_url = data["data"][0]["url"]
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()

        output_path = self.session_root / "05-master.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image_response.content)

        return output_path

    def _generate_via_openrouter(self, prompt: str) -> Path:
        """Generate via OpenRouter (Flux)."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not set")

        url = "https://openrouter.ai/api/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/zaharenok/claude-code-karuselka",
            "X-Title": "Claude Code Karuselka"
        }
        payload = {
            "prompt": prompt,
            "n": 1,
            "size": "1080x1440",
            "model": "flux-pro-v1.1"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()

        # Download image
        image_url = data["data"][0]["url"]
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()

        output_path = self.session_root / "05-master.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image_response.content)

        return output_path

    def _generate_locally(self, prompt: str) -> Path:
        """Generate via local Ollama model."""
        # Requires ollama serve running with image generation model
        model = os.getenv("LOCAL_MODEL", "gemma2:latest")

        try:
            # Use automatic1111 or similar local API
            url = "http://localhost:7860/sdapi/v1/txt2img"
            payload = {
                "prompt": prompt,
                "width": 1080,
                "height": 1440,
                "steps": 30,
                "cfg_scale": 7.5
            }

            response = requests.post(url, json=payload, timeout=180)
            response.raise_for_status()
            data = response.json()

            # Decode base64 image
            import base64
            image_data = base64.b64decode(data["images"][0])

            output_path = self.session_root / "05-master.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(image_data)

            return output_path

        except Exception as e:
            raise RuntimeError(
                f"Local generation failed. Ensure ollama serve or Automatic1111 is running. Error: {e}"
            )


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate master image for carousel")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--style-config", required=True, help="Path to style config JSON")
    parser.add_argument("--session-root", help="Override SESSION_ROOT")

    args = parser.parse_args()

    if args.session_root:
        os.environ["SESSION_ROOT"] = args.session_root

    generator = ImageGenerator()

    with open(args.style_config) as f:
        style_config = json.load(f)

    master_path = generator.generate_master_image(args.prompt, style_config)
    print(f"Master image generated: {master_path}")


if __name__ == "__main__":
    main()