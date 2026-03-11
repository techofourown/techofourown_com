# Hosting on Cloudflare Pages

Status: current  
Audience: maintainers

## Overview
- **App:** static HTML/CSS in repo root (no build step).
- **Host:** Cloudflare Pages project `web-techofourown`.
- **Media:** `media.techofourown.com` served from Cloudflare R2 + CDN (see `uploading-video-to-r2.md`).
- **Domains:** `techofourown.com` (apex) and `www.techofourown.com` CNAME to the Pages project, proxied in Cloudflare DNS.
- **Source of truth:** GitHub repo `techofourown/web-techofourown`.

## Deployment
### Automated (default)
- Workflow: `.github/workflows/cloudflare-pages.yml`
- Trigger: push to `main`
- Action: `cloudflare/pages-action@v1`
- Required repo secrets:
  - `CLOUDFLARE_API_TOKEN` — token with **Pages:Edit** on account `3c20efc51551c69eba728cdb54093b6b`
  - `CLOUDFLARE_ACCOUNT_ID` — set to `3c20efc51551c69eba728cdb54093b6b`
- Output: publishes the repo root to Cloudflare Pages production; previews come from the Pages `*.pages.dev` URL per commit.

### Manual (fallback)
```
export CLOUDFLARE_API_TOKEN=...   # Pages:Edit scope
export CLOUDFLARE_ACCOUNT_ID=3c20efc51551c69eba728cdb54093b6b
wrangler pages deploy . --project-name web-techofourown --branch main
```

## DNS
- `techofourown.com` → CNAME `web-techofourown.pages.dev` (proxied)
- `www.techofourown.com` → CNAME `web-techofourown.pages.dev` (proxied)
- `media.techofourown.com` unchanged (R2/CDN); do not modify during site deploys.
- GitHub Pages A/AAAA records removed; GitHub Pages should stay disabled in repo settings.

## Verification checklist (post-deploy)
- `curl -I https://techofourown.com/` returns 200 with CSP/Permissions-Policy/XFO headers.
- Key pages load: `/`, `/ourbox.html`, `/matchbox_demo.html`, `/woodbox_demo_parts_procurement.html`.
- Videos stream from `https://media.techofourown.com/...`.

## Rollback
- Redeploy a known-good commit via the workflow or `wrangler pages deploy`.
- If hosting path must revert, re-point DNS back to prior origin (not expected now that Pages is primary).
