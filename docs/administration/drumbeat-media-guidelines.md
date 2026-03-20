# Drumbeat media guidelines

Status: current  
Audience: maintainers

## Drumbeat media roles

### `coverImage`

Used on the detail page itself.

House intent:

- can be square, landscape, or portrait
- should look good when shown large on the entry page
- is not assumed to be safe as a thumbnail
- is not assumed to be safe as a share image

### `cardImage`

Used on `/` and `/drumbeat/`.

House intent:

- must be composed for a thumbnail slot
- should be safe in both a `4 / 3` and `16 / 10` frame
- if it is text-forward, screenshot-like, or OG-like, it must use `cardImageFit: contain`
- if it is art/photo and crop-safe, it should use `cardImageFit: cover`

### `shareImage`

Used for `og:image` and `twitter:image`.

House standard:

- target ratio: `1.91:1`
- house working size: `1200 × 630`
- all critical text and logos must stay inside a padded safe area
- do not use a screenshot with tiny UI text as a share image

## House aspect-ratio rules

### Preferred `cardImage` ratios

- ideal: `4:3` or `16:10`
- acceptable for `cover`: roughly `1.2` to `1.6`
- acceptable for `contain`: roughly `1.4` to `2.0`
- discouraged: portrait-only assets for thumbnail use

### Preferred `shareImage` ratio

- required house target: `1.91:1`

### Preferred `coverImage` ratios

- flexible
- choose what serves the detail page best

## Hard content rules

- Never ship a published Drumbeat entry without `cardImage`.
- Never ship a published Drumbeat entry without `shareImage`.
- Never reuse a GitHub-generated OG card as a `cover` thumbnail.
- Never reuse a title card as a `cover` thumbnail.
- If the image contains meaningful text near the edges, it is a `contain` thumbnail case or it needs a dedicated card asset.
- If the source image is portrait and the feed thumbnail matters, create a dedicated landscape `cardImage`.

## Practical creation rules

### Text post

Create:

- `coverImage`: the detail-page title card, usually `1600 × 900`
- `cardImage`: either a safer `1600 × 1000` or `1200 × 900` version, or reuse the title card with `cardImageFit: contain`
- `shareImage`: a dedicated `1200 × 630` social image

### Art / illustration post

Create:

- `coverImage`: original artwork
- `cardImage`: reuse artwork if crop-safe, otherwise export a thumbnail variant
- `shareImage`: dedicated `1200 × 630` share crop or padded adaptation

### Screenshot / GitHub preview / UI card post

Create:

- `coverImage`: the full screenshot if it serves the detail page
- `cardImage`: usually the same file with `cardImageFit: contain`, unless you make a dedicated thumbnail
- `shareImage`: a dedicated `1200 × 630` graphic, not the raw screenshot
