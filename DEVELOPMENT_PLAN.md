# Development Plan for Karuselka

## Immediate Tasks

### 1. Documentation overhaul
- [ ] Write primary README.md in English
- [ ] Create README_RU.md for Russian users
- [ ] Update HERMES_AGENTS.md with expanded services
- [ ] Update SLASH_COMMANDS.md with new platform options

### 3. Expand service integrations
- [ ] Add Brave Search as alternative/complement to Tavily
- [ ] Add fal.ai as image generation option
- [ ] Update skills/carusel-researcher/SKILL.md with Brave Search
- [ ] Update scripts/image_gen.py with fal.ai support
- [ ] Update .env.example with new service configs

### 4. Platform expansion
- [ ] Add support for Meta Ads carousels
- [ ] Add support for Facebook carousels
- [ ] Add support for LinkedIn carousels
- [ ] Update skill metadata with platform tags
- [ ] Create platform-specific templates

### 5. Referral integration
- [ ] Add Kie.ai referral link organically in README
- [ ] Add referral note in documentation where Kie is mentioned
- [ ] Keep it non-intrusive, helpful

### 6. Complete remaining skills
- [ ] carusel-image-prompter/SKILL.md
- [ ] carusel-slice/SKILL.md
- [ ] carusel-motion-director/SKILL.md
- [ ] carusel-animate/SKILL.md
- [ ] carusel-design-guardian/SKILL.md
- [ ] carusel-upload/SKILL.md
- [ ] carusel-publish/SKILL.md
- [ ] carusel-fixic/SKILL.md

### 7. Complete scripts
- [ ] upload_carousel_assets.py
- [ ] video_gen.py (Grok Video + fal.ai video)
- [ ] publish_preflight.py
- [ ] brave_search_client.py (optional, can use Tavily-MCP)

## Medium-term Tasks

### 8. Testing and validation
- [ ] Test full pipeline with Tavily
- [ ] Test full pipeline with Brave Search
- [ ] Test image gen with Kie.ai
- [ ] Test image gen with fal.ai
- [ ] Test image gen with local Ollama
- [ ] Test Instagram publish via MCP
- [ ] Test Meta Ads carousel export

### 9. Platform-specific formats
- [ ] Instagram: 1080×1080 or 1080×1350
- [ ] Meta Ads: 1080×1080, 1080×1350, 1080×1920
- [ ] Facebook: 1080×1080
- [ ] LinkedIn: 1080×1080, 1200×627
- [ ] Update design specs per platform

### 10. Advanced features
- [ ] Multi-language support
- [ ] Template library (shared/carousel-prompt-library.md already exists)
- [ ] Brand kit system (colors, fonts, logo)
- [ ] A/B testing copy variants
- [ ] Analytics integration (CTR, save rate, engagement)

## Long-term Tasks

### 11. Performance optimization
- [ ] Parallelize independent steps
- [ ] Cache frequently used assets
- [ ] Optimize image generation prompts

### 12. CLI improvements
- [ ] Interactive mode for parameter input
- [ ] Progress bars for long-running tasks
- [ ] Better error messages and recovery

### 13. Documentation
- [ ] API documentation for skills
- [ ] Integration guide for Hermes
- [ ] Troubleshooting guide
- [ ] Video tutorial (maybe)

## Priority

### High (Now)
- 1. Rename and rebrand
- 2. Documentation overhaul
- 3. Expand service integrations
- 4. Platform expansion
- 5. Referral integration

### Medium (This week)
- 6. Complete remaining skills
- 7. Complete scripts

### Low (Future)
- 8-13: Testing, advanced features, optimization