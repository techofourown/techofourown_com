# ADR-0001: Use Cloudflare R2 and Cloudflare CDN for first-party video delivery


## Date
2026-02-04

## Context

Tech of Our Own publishes public-facing videos (e.g., build logs, education, calls-to-action) that are
intended to be accessible to mainstream users.

We will continue to mirror videos on third-party platforms (e.g., YouTube) for reach. However, we
also want a canonical, first-party option on our own website so people can watch without ad-tech
surveillance, without platform engagement incentives, and without being turned into targeting data.

At the same time, availability and resilience are a prerequisite for the mission. A first-party
publishing channel that is easy to knock offline via denial-of-service (DoS/DDoS) or harassment does
not meaningfully serve users. The threat model includes adversarial actors who may attempt to disrupt
availability (including large-scale DDoS), even when the content itself is public and non-sensitive.

This ADR chooses the initial architecture for first-party video delivery:

- **Bucket layer** (object storage for video files)
- **CDN layer** (global delivery, caching, and DDoS resistance in front of those files)

Constraints and priorities:

- **Primary priority:** robustness against DoS/DDoS and common internet abuse.
- **Secondary priority:** reduce ad-tech and data-broker exposure for viewers (no embedded
  third-party video platforms; no ad-tech tracking scripts).
- **Acceptable tradeoff:** using a major third-party edge provider even if it implies (a) dependency,
  (b) metadata visibility to that provider (IP/request logs), and (c) security-related cookies.
- **Explicitly not a goal (today):** state-level confidentiality for viewers. These videos are
  public, friendly, and also mirrored elsewhere. We are not trying to make watching these videos
  anonymous against a capable state adversary.
- **Tor/VPN friction:** not prioritized for this use case. Users who prefer Tor can still access the
  software/code/docs and can choose alternate mirrors for video content if needed.

We expect to revisit this decision if the threat model changes (e.g., we begin hosting sensitive
content, user-generated content, or we observe unacceptable user friction).

## Decision

We will use **Cloudflare** for both layers of first-party video delivery:

1. **Object storage:** **Cloudflare R2** will be the bucket/origin for public video assets served
   from our website.
2. **Delivery + protection:** **Cloudflare CDN / edge network** will serve these assets globally and
   provide DDoS resistance and edge caching.

Operational guardrails (normative for this decision):

- This Cloudflare-based pipeline is for **public, non-sensitive media** intended for reach and
  education. It is not the architecture for private communications or high-risk content.
- Videos will be **mirrored** on at least one additional public platform (e.g., YouTube) so Cloudflare
  is not a single point of total failure for access to the content.
- We accept that Cloudflare may set **security-related cookies** (e.g., bot/challenge/security
  cookies) as part of operating an edge security posture. We treat this as an acceptable tradeoff
  for availability.
- We will not intentionally add ad-tech tracking to the first-party viewing experience. The purpose
  of the first-party channel is “watch without ads / ad-tech.”

## Rationale

Cloudflare is selected because it best matches the current priorities and constraints:

- **DDoS resilience is existential for reach.** A first-party channel that can be routinely knocked
  offline is not usable as an alternative to platform hosting.
- **Single-vendor simplicity for launch.** Using one provider for both bucket and CDN reduces
  integration and operations overhead and accelerates time-to-publish.
- **Cost and scale predictability for video.** Video delivery is bandwidth-heavy. Using Cloudflare
  R2 + Cloudflare edge is a pragmatic choice for controlling delivery cost and avoiding “viral
  success = financial failure” dynamics.
- **This content is not a confidentiality surface.** These are public videos, mirrored elsewhere.
  We are offering an ad-free/no-ad-tech option, not a high-anonymity channel.
- **Dependency count is not the decisive factor.** If Cloudflare is the front door for delivery,
  the availability chain already depends on Cloudflare. Adding R2 does not meaningfully change the
  “single provider outage or policy issue impacts availability” reality for this specific media
  pipeline.
- **Exit is plausible.** We believe we can preserve credible exit by keeping media in standard
  formats and maintaining mirrors elsewhere. If the threat model changes or Cloudflare becomes
  misaligned with our values, we can reassess and migrate.

## Consequences

### Positive

- **High availability and abuse resistance** for first-party media delivery (better resilience to
  opportunistic and targeted DoS/DDoS).
- **Faster time-to-launch** with a lower operational burden than stitching multiple vendors together.
- **A practical “watch without ads/ad-tech” option** that does not require viewers to load a
  third-party video platform player.
- **Better tolerance of traffic spikes** typical of public media releases.

### Negative

- **Centralization and dependency risk:** Cloudflare becomes a critical dependency for first-party
  video delivery at both storage and edge layers.
- **Viewer metadata visibility:** Cloudflare will necessarily observe request metadata (e.g., IP
  address, user agent) to deliver content.
- **User friction risk:** Cloudflare’s security posture can create access friction for some users,
  especially Tor/VPN users or users with strict privacy/browser hardening.
- **Cookie optics:** Cloudflare may set security/bot-related cookies. Some privacy tools and users
  may interpret any third-party-set cookie as “tracking,” even when it is security-related rather
  than ad-tech profiling.
- **Policy drift risk:** Future pricing, product changes, or policy decisions by Cloudflare could
  make this architecture less aligned with TOOO’s values or less viable operationally.

### Mitigation

- **Mirrors as an availability backstop:** Maintain at least one public mirror (e.g., YouTube) for
  videos so Cloudflare is not a single point of total access failure.
- **Keep the content portable:** Use standard video formats and keep a canonical local archive of
  uploaded media so migration is feasible if needed.
- **Keep the first-party experience clean:** Avoid embedding third-party ad-tech analytics and avoid
  third-party platform players in the canonical page.
- **Avoid unnecessary friction by default:** Do not run “maximum friction” modes continuously.
  Escalate protections only if/when active abuse requires it.
- **Reassessment trigger:** If we begin publishing sensitive content, if Tor access becomes a
  priority, if Cloudflare introduces ad-tech-like behaviors, or if user friction/cookie behavior
  becomes unacceptable, open a follow-up RFC to evaluate alternatives.

## Notes

- Cloudflare cookie behavior is **feature- and configuration-dependent**, not “video-page only.”
  Security/bot features may issue cookies on any proxied request. We accept this today for the media
  delivery channel, and we will revisit if it materially harms user trust or access.

## References

- Tech of Our Own values and governance (org-level):
  - https://github.com/techofourown/org-techofourown/blob/main/docs/policies/founding/VALUES.md
  - https://github.com/techofourown/org-techofourown/blob/main/docs/policies/founding/CONSTITUTION.md
  - https://github.com/techofourown/org-techofourown/blob/main/docs/ethos/Signs_and_Ancestrals.md
  - https://github.com/techofourown/org-techofourown/blob/main/docs/decisions/ADR-0006-adopt-cc-by-4-0-public-documents-and-educational-media.md

- Cloudflare product references (for bucket + CDN concepts):
  - Cloudflare R2 (object storage): https://www.cloudflare.com/developer-platform/products/r2/
  - Cloudflare DDoS protection overview: https://www.cloudflare.com/ddos/
  - Cloudflare “Under Attack Mode” (challenge mode): https://developers.cloudflare.com/fundamentals/reference/under-attack-mode/
  - Cloudflare cookies (security/bot cookies): https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/
  - Tor/Cloudflare discussion (access friction context):
    - Tor Project: https://blog.torproject.org/trouble-cloudflare/
    - Cloudflare: https://blog.cloudflare.com/the-trouble-with-tor/
