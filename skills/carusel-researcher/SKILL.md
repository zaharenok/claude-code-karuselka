---
name: carusel-researcher
category: social-media
description: |
  Researches social media carousel topics via Tavily or Brave Search: audience analysis, competitor audit, angle discovery
version: 1.0.0
author: zaharenok
tags: [instagram, carousel, research, tavily, brave-search, market-analysis]
---

# Carusel Researcher

## Role

Researcher for social media carousels. Analyzes topics, audiences, competitors, trends.

## Tools

- **Tavily MCP** — primary research (web research, competitor analysis, trend detection)
- **Brave Search** — alternative research (privacy-focused web search)
- **File operations** — read/write results

## Environment Configuration

Research service is selected via command line or `.env`:

```bash
# Command line override
/carousel-new --topic "X" --research-service tavily

# Or via .env
RESEARCH_SERVICE=tavily  # or brave
```

## Input Data

Reads from `{SESSION_ROOT}/00-brief.md`:

```markdown
## Topic
How AI changes marketing

## Platform
instagram

## Reference Account
@neilpatel

## Target Audience
Marketers 25-45 years, SMB owners

## CTA
Subscribe to newsletter
```

## Process

### 1. Topic Analysis via Tavily

```python
mcp_tavily_remote_tavily_research(
    input=f"Analyze social media content trends about: {topic}",
    max_results=10
)
```

### 2. Reference Account Audit

```python
# Download last 20 carousels from reference
# Analyze formats, headlines, CTAs
# Identify patterns
```

### 3. Competitor Analysis

```python
mcp_tavily_remote_tavily_search(
    query=f"{platform} carousel {topic} examples",
    max_results=10
)
```

### 4. Alternative: Brave Search

If `RESEARCH_SERVICE=brave`:

```python
mcp_tavily_remote_tavily_search(
    query=f"{platform} carousel trends {topic}",
    max_results=15,
    search_depth="advanced"
)
```

### 5. Angles Discovery — 3-5 variants

Examples:
- "AI → Automation → ROI"
- "Tools → Tactics → Results"
- "Future → Now → Action"
- "Problem → Solution → Implementation"

## Output Data

Writes to `{SESSION_ROOT}/01-research.md`:

```markdown
# Research Report

## Platform Analysis
- Platform: Instagram
- Format: 3×3 grid, 1:1 or 4:5 aspect ratio
- Video support: Loop 5s for slide-01 recommended
- Best posting times: 10-11 AM, 7-9 PM (local time)

## Audience Analysis
- Age: 25-40 years dominate carousel consumption
- Platform: 60% mobile, 40% desktop
- Attention: 3 seconds per slide → punchy headlines critical
- Behavior: Save rate > 5% is excellent

## Topic Trends
- AI tool screenshots + annotations (high CTR)
- Before/After comparisons (38% higher save rate)
- Step-by-step frameworks (57% higher share rate)
- Data-driven charts (42% higher engagement)

## Reference Account Analysis (@neilpatel)
- Average slide: 150-200 words
- Headlines: Question-based (70%), Numbered lists (30%)
- CTA: Link in bio only (87%), DM for template (13%)
- Colors: Blue (#007AFF), White (#FFFFFF), Yellow (#FFD600)
- Posting frequency: 2-3 carousels/week

## Competitors
- @garyvee: Short slides, heavy emoji, video-first
- @hubspot: Educational, case study format
- @Buffer: Data-backed charts, minimal text

## Recommended Angles
1. **Tool → Case Study → ROI** (for SMB owners)
2. **Problem → AI Solution → Implementation** (for marketers)
3. **Trend → Tool → Tutorial** (for early adopters)
4. **Data → Insight → Action** (for data-driven audience)

## Pitfalls
- Overly technical jargon → keep it simple
- Too much text per slide → max 40 words
- Missing CTA on final slide → convert point critical
- Ignoring platform specifics → format matters
```

## Fragment Contract

Create `{SESSION_ROOT}/fragments/01-research-summary.md`:

```markdown
# Research Summary

## Done
- Analyzed 20 reference carousels
- Audited 3 competitors
- Identified 5 trend patterns
- Discovered 4 angle variations

## Issues
- Reference account posts infrequently (2/month)
- Limited carousel data for B2B audience
- Platform-specific optimization needed

## Recommendations
- Focus on B2C marketing angle (more data)
- Use broader reference pool
- Test multiple angles in A/B format
```

## Pitfalls from `shared/agent-pipeline-pitfalls.md`

- Don't copy reference structure 1:1 → adapt to brand
- Don't ignore platform-specific formats → aspect ratio matters
- Don't overload with data → 3 key insights max
- Don't forget video support → Instagram supports loop video

## Platform-Specific Notes

### Instagram
- Aspect ratio: 1:1 or 4:5
- Video: Loop 5s for slide-01 recommended
- Hashtags: 3-5 relevant tags
- Best posting: 10-11 AM, 7-9 PM

### Meta Ads
- Aspect ratio: 1:1, 4:5, or 9:16
- Video: Optional
- Compliance: Ad policies apply
- CTA: Clear, measurable action

### Facebook
- Aspect ratio: 1:1 only
- Video: Optional
- Organic posting focus
- Link preview support

### LinkedIn
- Aspect ratio: 1:1 or 16:9
- Video: Not recommended
- Professional tone required
- Document format option

## Environment Variables

```bash
# Research Service
RESEARCH_SERVICE=tavily  # or brave

# Tavily MCP
TAVILY_API_KEY=tvly-...

# Brave Search
BRAVE_API_KEY=...

# Session Storage
SESSION_ROOT=~/.hermes/karuselka/sessions/{timestamp}/
```