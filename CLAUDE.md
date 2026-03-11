# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the public-facing website for Tech of Our Own (techofourown.com), a stakeholder-led company building non-extractive consumer technology. The site is now an Astro-based static site that builds to `dist/`, while some legacy `.html` pages remain as passthrough files during the migration.

**Key pages:**
- `src/pages/index.astro` - Main landing page describing Tech of Our Own's mission, vision, and governance model
- `public/ourbox.html` - Temporary legacy passthrough for the OurBox page during migration
- `public/matchbox_demo.html` - Temporary legacy passthrough for the Matchbox demo page during migration

## Architecture

### Site Structure
This is a static Astro site with no client-side JavaScript. Astro pages live under `src/pages/`, shared styling lives in `src/styles/`, and raw passthrough assets live in `public/`. Some legacy HTML pages still carry inline CSS while they await migration. The design uses:
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
```

**Required elements:**
- **Type:** `feat`, `fix`, `perf`, `refactor`, `docs`, `chore`, `test`, `build`, `ci`, `style`, `revert`
- **Subject:** Max 100 characters, no trailing period, lowercase type
- **Body:** REQUIRED - must explain what changed and why (blank line after subject)
- **Line length:** Max 100 characters per line (header, body, footer)

### Single Authorship Principle
This repository enforces **single authorship** - each commit has ONE author who takes full responsibility. The git hooks will REJECT commits that contain:
- Email addresses anywhere in commit messages (privacy + single authorship)
- "Co-Authored-By" trailers of any kind
- Any external attribution patterns (Generated with, Thanks to, Assisted by, etc.)
- Tool/entity mentions suggesting shared authorship (Claude, ChatGPT, Copilot, AI, etc.)

**Why:** Collaboration happens in PRs/issues, not commit messages. Git metadata already records authorship. Attribution dilutes responsibility.

**When committing work assisted by Claude Code:** You (the human) write the commit and sign it yourself. Do **not** add Co-Authored-By trailers; the hooks enforce single authorship.

### Git Hooks
Active hooks in `.git/hooks/`:
- `commit-msg` - Validates conventional commits format, 100-char limits, email ban, attribution ban using commitlint and gitlint
- `pre-push` - Auto-rebases if remote advanced (e.g., semantic-release), ensures seed tag exists, blocks emails
- `post-checkout` and `post-commit` - Additional automation

**Note:** These hooks reference `/srv/praxes/tools/git-commit-standards.md` for help, which may not exist in all environments.

## Development Workflow

### Making Changes
```bash
# Edit Astro pages in src/pages/ and shared styles in src/styles/
# Legacy passthrough .html pages live in public/ during the migration

# Run the Astro dev server locally
npm install
npm run dev

# Commit with proper format
git commit -m "$(cat <<'EOF'
docs: update governance section

Revised the governance model description to clarify user and worker representation on the board.
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
The site deploys automatically via Cloudflare Pages. GitHub Actions runs `npm ci` and `npm run build`, then publishes `dist/` to the custom domain `techofourown.com`. Media remains first-party on `https://media.techofourown.com` (Cloudflare R2 + CDN).

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
