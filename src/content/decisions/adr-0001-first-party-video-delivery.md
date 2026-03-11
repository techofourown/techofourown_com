---
title: "ADR-0001: First-party video delivery through Cloudflare R2 and CDN"
description: "Why Tech of Our Own uses Cloudflare R2 and Cloudflare's edge for public first-party video delivery."
summary: "A public version of the decision to keep canonical video delivery first-party while accepting Cloudflare as the current storage and edge layer."
draft: false
order: 1
publishedAt: 2026-02-04
status: "accepted"
---

Tech of Our Own publishes public videos such as walkthroughs, build logs, and educational material. We want a canonical first-party option so people can watch without loading an ad-tech video platform, but that channel still has to survive ordinary abuse and traffic spikes.

## Decision

Use Cloudflare for both layers of first-party public video delivery:

1. **Cloudflare R2** stores the video assets.
2. **Cloudflare's edge network** delivers those assets globally with caching and DDoS resistance.

This is the architecture for public, non-sensitive media. It is not the architecture for private communications or high-risk content.

## Why this was the right initial choice

The deciding constraint was availability.

A first-party media channel that is easy to knock offline does not meaningfully serve the mission. Public walkthroughs and educational material need to stay reachable even when they attract unwanted attention or traffic spikes.

Cloudflare was the pragmatic launch choice because it let us keep storage and delivery in one place, reduce operational complexity, and get to a first-party viewing experience quickly.

We also wanted to avoid embedding third-party players or ad-tech analytics into the canonical viewing path. Viewers should be able to watch from our own infrastructure without being routed through an engagement engine.

## Tradeoffs we accepted

This decision does introduce real tradeoffs.

- Cloudflare becomes a critical dependency for first-party video delivery.
- Cloudflare can observe normal request metadata needed to deliver content.
- Some users may experience friction from Cloudflare security posture, especially with hardened privacy setups.
- Cloudflare may set security-related cookies as part of edge protection.

Those tradeoffs were accepted because the primary goal for this channel is resilient, public delivery, not anonymity against a sophisticated adversary.

## Guardrails

The decision comes with guardrails.

- The first-party viewing experience should stay free of ad-tech tracking.
- Public videos should still be mirrored elsewhere so Cloudflare is not the only access path.
- Media stays in standard formats and in local archives so future migration remains plausible.
- If the threat model changes, this decision should be revisited rather than treated as permanent doctrine.

## Consequences

The result is a first-party media pipeline that is easier to operate, more resilient to disruption, and aligned with the goal of giving people a way to watch without platform surveillance.

The cost is centralization around Cloudflare for this specific delivery path. That tradeoff is acceptable for now, but it remains a live decision rather than sacred architecture.

## Source material

This public entry is adapted from the repository ADR:

- [ADR-0001 in the repository](https://github.com/techofourown/web-techofourown/blob/main/docs/decisions/ADR-0001-use-cloudflare-r2-and-cdn-for-first-party-video-delivery.md)
