# Changelog

## [Unreleased]

### Added
- MCP server with 5 tools for agent integration
- CLI with 5 commands for manual carousel creation
- **Seedance 1.5 Pro (ByteDance)** video generation support — cheapest option on Kie.ai ($0.0175/s, 720p, 5s loop, no audio)

### Changed
- Rebrand from FrameForge back to Karuselka
- Default aspect ratio changed to 4:5 for Instagram and Meta Ads (was 1:1)
- `VIDEO_GEN_PROVIDER` default from `grok` to `seedance`
- Platform aspect ratios:
  - Instagram: 4:5 (default) or 1:1
  - Meta Ads: 4:5 (default) or 1:1, 9:16
  - Facebook: 1:1
  - LinkedIn: 1:1 or 16:9
- Video support specified as Seedance 1.5 Pro, 5s loop
- Session storage: `~/.hermes/karuselka/sessions` (was `~/.hermes/frameforge/sessions`)
- Environment variable: `KARUSELKA_SESSION_ROOT` (was `FRAMEFORGE_SESSION_ROOT`)

### Removed
- `GROK_API_KEY` requirement (not needed with seedance)

## [0.1.0] - 2025-01-15

### Added
- Initial release as Karuselka
- Multi-platform support: Instagram, Meta Ads, Facebook, LinkedIn
- Research services: Tavily MCP, Brave Search
- Image generation: Kie.ai, OpenRouter, fal.ai, local
- Video generation: Grok Video, fal.ai
- Upload storage: Kie.ai, S3, local
- Hermes agent integration via delegate_task
- Slash commands: /carousel-new, /carousel-publish
- Kie.ai referral integration