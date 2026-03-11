# Publishing site content

Status: current  
Audience: maintainers

## Overview
The public site is an Astro site with content collections defined in
`src/content.config.ts`.

Use Astro pages for high-structure marketing surfaces such as `/` and `/ourbox`.
Use content entries for repeatable public material such as build guides, learn
pages, philosophy essays, journal entries, and curated library entries.

Do not auto-publish the whole `docs/` tree. The public library is curated.

## Add a learn entry
1. Create a Markdown file in `src/content/learn/`.
2. Add frontmatter:
   - `title`
   - `description`
   - `summary` (optional but recommended)
   - `draft`
   - `order` or `publishedAt`
   - `runtime` (optional)
   - `videoUrl` when a video exists
   - `noindex` and `referrer` for non-indexed walkthroughs
3. Write the body in Markdown.
4. Run `npm run check && npm run build`.
5. Verify the page at `/learn/<slug>`.

## Add a build entry
1. Create a Markdown file in `src/content/build/`.
2. Add frontmatter:
   - `title`
   - `description`
   - `summary` (optional)
   - `draft`
   - `order` or `publishedAt`
   - `difficulty`
   - `estimatedTime` (optional)
   - `videoUrl` when a video exists
   - `noindex` and `referrer` for non-indexed walkthroughs
3. Run `npm run check && npm run build`.
4. Verify the page at `/build/<slug>`.

## Add a journal entry
1. Create a Markdown file in `src/content/journal/`.
2. Include `title`, `description`, `summary` (optional), `draft`, `order`
   (optional), and `publishedAt`.
3. Run `npm run check && npm run build`.
4. Verify the entry at `/journal/<slug>` and in `/journal`.

## Add a philosophy entry
1. Create a Markdown file in `src/content/philosophy/`.
2. Include `title`, `description`, `summary` (optional), `draft`, `order`
   (optional), and `publishedAt`.
3. Run `npm run check && npm run build`.
4. Verify it appears in `/why`.

## Publish a public ADR or RFC
1. Start from the repository source material in `docs/decisions/` or `docs/rfcs/`.
2. Adapt it into a public-facing Markdown entry under:
   - `src/content/decisions/` for ADRs
   - `src/content/rfcs/` for public RFCs
3. Keep the actual decision, rationale, tradeoffs, and consequences.
4. Remove maintainer-only framing, operational clutter, and repo-internal assumptions.
5. Link back to GitHub as source material, not as the primary reading surface.
6. Run `npm run check && npm run build`.
7. Verify `/library`, `/library/decisions`, and `/library/rfcs`.

## What stays repo-only
These materials remain in the repository and should not be auto-published:
- `docs/administration/`
- `docs/reference/`
- operational playbooks
- maintainer workflow notes
- any internal or provisional doc that is not ready for the public library

## Deployment check
After content changes:
```bash
npm run check
npm run build
```

For a manual preview deploy:
```bash
export CLOUDFLARE_API_TOKEN=...
export CLOUDFLARE_ACCOUNT_ID=...

npx wrangler pages deploy dist --project-name web-techofourown --branch <branch-name>
```
