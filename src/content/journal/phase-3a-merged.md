---
title: "Phase 3A merged"
description: "Astro replaced repo-root publishing as the site build layer while Cloudflare Pages and first-party media stayed in place."
summary: "The site now builds through Astro, publishes `dist` to Cloudflare Pages, and keeps media on the existing first-party R2/CDN path."
draft: false
order: 1
publishedAt: 2026-03-11
---

Phase 3A was the publishing-machine replacement.

The public site is no longer "repo root HTML goes straight to production." It is now an Astro site that builds static output into `dist`, which Cloudflare Pages publishes.

## What changed

- Astro is now the build layer for the public site.
- The homepage and OurBox page are real Astro routes.
- Shared layout, navigation, footer, and theme rules now live in source instead of being copied between pages.
- Deploys publish built output instead of raw repo-root files.

## What did not change

A few important things stayed exactly where they belong.

- Cloudflare Pages is still the public host.
- `media.techofourown.com` still serves video from the existing first-party R2/CDN path.
- The site remains static-first and script-free under the current CSP.
- GitHub remains the source of truth for code, docs, and public history.

## Why this mattered

Phase 3 is not about adding accounts, commerce, or application logic. It is about replacing the publishing machinery so the site becomes cheaper to extend without collapsing back into repeated hand-edited HTML files.

That gives the project a path to add learn pages, build guides, philosophy writing, journal entries, and curated public library material without rewriting the hosting story again.

## What comes next after Phase 3

With Phase 3 complete, the site has the publishing foundation it needs for the
next architectural phase.

That means the next work can focus on expanding the public rooms of the house
instead of fighting the build system:

- more learn pages and build guides
- more public philosophy and library material
- a broader public information architecture
- future application and service layers only when they are actually justified

The important thing is that hosting, media delivery, and publishing now line up.
New public material is cheaper to publish, easier to review, and easier to keep
coherent.
