# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the public-facing website for Tech of Our Own (techofourown.com), a stakeholder-led company building non-extractive consumer technology. The site consists of static HTML pages with inline CSS, no build process required.

**Key pages:**
- `index.html` - Main landing page describing Tech of Our Own's mission, vision, and governance model
- `ourbox.html` - Product page for OurBox, the flagship local-first home server appliance
- `CNAME` - DNS configuration for GitHub Pages deployment to techofourown.com

## Architecture

### Site Structure
This is a simple static website with no frameworks, no bundlers, and no JavaScript. All styling is inline CSS within `<style>` tags in each HTML file. The design uses:
- CSS custom properties for theming (color scheme, shadows, spacing)
- Responsive grid layouts with `auto-fit` for cards and sections
- Modern CSS features (clamp, radial-gradient, backdrop-filter)
- Mobile-first responsive design with media queries

### Documentation System
The `docs/` directory organizes documentation by purpose:

**Administration (`docs/administration/`)** - Operational guides
- Step-by-step procedures for recurring tasks (e.g., uploading media to R2)
- Practical and focused on what works

**RFCs (`docs/rfcs/`)** - Pre-decisional exploration
- Draft proposals, trade-off analysis, open questions
- Status: Draft | Discussion | Accepted | Rejected | Withdrawn
- Use for exploring ideas before committing to decisions

**ADRs (`docs/decisions/`)** - Architecture Decision Records
- Post-decisional documentation of what was decided and why
- Status: Proposed | Accepted | Deprecated | Superseded
- Link back to originating RFCs when applicable
- Example: ADR-0001 documents Cloudflare R2/CDN decision for video delivery

**Naming convention:** Both use zero-padded numbers with descriptive slugs:
- `RFC-0001-descriptive-slug.md`
- `ADR-0001-descriptive-slug.md`

Templates for both formats exist in `docs/rfcs/0000-template.md` and `docs/decisions/0000-template.md`.

## Commit Standards

This repository enforces strict commit message standards via git hooks. All commits MUST follow these rules:

### Conventional Commits Format
```
<type>: <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Required elements:**
- **Type:** `feat`, `fix`, `perf`, `refactor`, `docs`, `chore`, `test`, `build`, `ci`, `style`, `revert`
- **Subject:** Max 100 characters, no trailing period, lowercase type
- **Body:** REQUIRED - must explain what changed and why (blank line after subject)
- **Line length:** Max 100 characters per line (header, body, footer)

### Single Authorship Principle
This repository enforces **single authorship** - each commit has ONE author who takes full responsibility. The git hooks will REJECT commits that contain:
- Email addresses anywhere in commit messages (privacy + single authorship)
- "Co-Authored-By" trailers (except for Claude Code's standardized trailer)
- Any external attribution patterns (Generated with, Thanks to, Assisted by, etc.)
- Tool/entity mentions suggesting shared authorship (Claude, ChatGPT, Copilot, AI, etc.)

**Why:** Collaboration happens in PRs/issues, not commit messages. Git metadata already records authorship. Attribution dilutes responsibility.

**When committing work assisted by Claude Code:** You (the human) are the sole author. The standard Claude co-authorship trailer is required by Claude Code's commit process, but YOU are still the single responsible author.

### Git Hooks
Active hooks in `.git/hooks/`:
- `commit-msg` - Validates conventional commits format, 100-char limits, email ban, attribution ban using commitlint and gitlint
- `pre-push` - Auto-rebases if remote advanced (e.g., semantic-release), ensures seed tag exists, blocks emails
- `post-checkout` and `post-commit` - Additional automation

**Note:** These hooks reference `/srv/praxes/tools/git-commit-standards.md` for help, which may not exist in all environments.

## Development Workflow

### Making Changes
```bash
# Edit HTML files directly - no build step needed
# CSS is inline in each HTML file

# Test locally by opening files in browser
open index.html  # macOS
xdg-open index.html  # Linux

# Commit with proper format
git commit -m "$(cat <<'EOF'
docs: update governance section

Revised the governance model description to clarify user and worker representation on the board.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push (hooks will auto-rebase if needed)
git push github main
```

### Working with Documentation
```bash
# Create a new RFC to explore an idea
cp docs/rfcs/0000-template.md docs/rfcs/RFC-0002-your-topic.md
# Edit, set status to "Draft", submit PR

# After decision, create ADR
cp docs/decisions/0000-template.md docs/decisions/ADR-0002-your-decision.md
# Document decision, link to RFC, set status to "Accepted"
```

### Deployment
The site deploys automatically via GitHub Pages to techofourown.com. No manual deployment steps required - just push to main.

## Project Values and Constraints

When working on this site, keep these organizational principles in mind:

**Non-negotiables:**
- No subscriptions or recurring fees for consumer features
- Local-first architecture (though this is just a marketing site)
- No user data collection or behavioral tracking
- Open source always
- User and worker governance representation

**Content focus:**
- Mission-driven messaging about ownership, privacy, and autonomy
- Transparent governance model (co-op structure with user/worker stewards)
- OurBox as flagship product (local-first home server)
- Build-in-public ethos with GitHub integration

**Design principles:**
- Clean, accessible, modern aesthetic
- No JavaScript for core functionality
- Fast loading, low complexity
- Works without external dependencies (except fonts)

## Related Repositories

This is part of the Tech of Our Own organization:
- `org-techofourown` - Organization governance docs, constitution, values
- `pf-ourbox` - OurBox product family documentation and specs

Links to these are embedded throughout the website content.
