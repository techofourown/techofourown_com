# Documentation

This repository uses a lightweight documentation structure focused on RFCs, ADRs,
and a curated boundary between repo-only docs and the public site.

## Structure

```
docs/
├── administration/  # Operational guides and maintainer workflows
│   ├── hosting-cloudflare-pages.md  # Site hosting + deployment
│   └── publishing-site-content.md   # How to publish content to the Astro site
├── rfcs/            # Pre-decisional exploration and proposals
└── decisions/       # Architecture Decision Records (ADRs)
```

## When to use what

- **Administration (`administration/`)** — operational guides for recurring tasks (e.g., uploading
  media, configuring services). Step-by-step, practical, focused on what works. These docs stay
  repo-only unless explicitly adapted for the public site.
- **RFCs (`rfcs/`)** — explore ideas or proposals before deciding; capture options, trade-offs, and
  open questions.
- **ADRs (`decisions/`)** — record a decision that was made, with context, rationale, consequences,
  and links to any originating RFC.
- **Public library** — curated content adapted into `src/content/decisions/` and `src/content/rfcs/`.
  Repo docs do not automatically become public pages.

## Flow

```
Problem or Idea
    ↓
RFC (exploration) → Discussion → Decision
    ↓                              ↓
Implementation               ADR (record)
```

## Conventions

- **Numbering + slugs**: `RFC-0001-descriptive-slug.md` and `ADR-0001-descriptive-slug.md`
  (zero-padded, short hyphenated slug).
- **Status**: RFCs use `Draft | Discussion | Accepted | Rejected | Withdrawn`; ADRs use
  `Proposed | Accepted | Deprecated | Superseded` (with backlinks).
- **Cross-links**: ADRs link to source RFCs/issues and any supersedes/superseded-by records; RFCs
  link to related ADRs when promoted.
- **Change control**: create/update RFCs and ADRs via PRs. Keep them concise; prefer follow-up ADRs
  to massive edits.
- **Publishing boundary**: maintainer docs remain in `docs/administration/` and repo-only reference
  material stays repo-only until someone intentionally adapts it for the site.
