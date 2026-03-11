# Hosting on Cloudflare Pages

Status: current  
Audience: maintainers

## Overview
- **App:** Astro source in `src/` with static passthrough files in `public/`.
- **Host:** Cloudflare Pages project `web-techofourown`.
- **Media:** `media.techofourown.com` served from Cloudflare R2 + CDN (see `uploading-video-to-r2.md`).
- **Domains:** `techofourown.com` (apex) and `www.techofourown.com` CNAME to the Pages project, proxied in Cloudflare DNS.
- **Source of truth:** GitHub repo `techofourown/web-techofourown`.
- **Build output:** `dist/`

## Deployment
### Automated (default)
- Workflow: `.github/workflows/cloudflare-pages.yml`
- Trigger: push to `main`
- Publish command: `npx wrangler pages deploy dist --project-name web-techofourown --branch main`
- Build steps: `npm ci`, `npm run check`, then `npm run build`
- Required repo secrets:
  - `CLOUDFLARE_API_TOKEN` — token with **Pages:Edit** on account `3c20efc51551c69eba728cdb54093b6b`
  - `CLOUDFLARE_ACCOUNT_ID` — set to `3c20efc51551c69eba728cdb54093b6b`
- Output: publishes `dist/` to Cloudflare Pages production from `main` only.

### Manual (fallback)
```
npm run check
npm run build

export CLOUDFLARE_API_TOKEN=...   # Pages:Edit scope
export CLOUDFLARE_ACCOUNT_ID=3c20efc51551c69eba728cdb54093b6b
npx wrangler pages deploy dist --project-name web-techofourown --branch main
```

### Manual preview deploys
- Non-`main` branch previews are manual for now.
- Use `npx wrangler pages deploy dist --project-name web-techofourown --branch <branch-name>` after `npm run build`.

## DNS
- `techofourown.com` → CNAME `web-techofourown.pages.dev` (proxied)
- `www.techofourown.com` → CNAME `web-techofourown.pages.dev` (proxied)
- `media.techofourown.com` unchanged (R2/CDN); do not modify during site deploys.
- GitHub Pages is disabled for this repository; Cloudflare Pages is the only intended publisher.

## Route compatibility during Phase 3
- Legacy `.html` routes remain reachable during migration because the files are copied through from `public/`.
- Cloudflare Pages may canonicalize those routes to extensionless paths with a `308` redirect in practice.
- Treat the legacy `.html` files as a compatibility layer, not as a guarantee of byte-for-byte legacy URL behavior.
- When replacing a legacy page with an Astro route, add an explicit redirect and test fragment preservation in a browser.

## Verification checklist (post-deploy)
- `curl -I https://techofourown.com/` returns 200 with CSP/Permissions-Policy/XFO headers.
- Key pages load: `/`, `/ourbox.html`, `/matchbox_demo.html`, `/woodbox_demo_parts_procurement.html`.
- Videos stream from `https://media.techofourown.com/...`.
- Build output contains `_headers` and `_redirects` copied through from `public/`.

## Rollback
- Redeploy a known-good commit via the workflow or `wrangler pages deploy`.
- If hosting path must revert, re-point DNS back to prior origin (not expected now that Pages is primary).
