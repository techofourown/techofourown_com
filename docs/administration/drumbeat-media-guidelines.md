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

## Detail-page cover presentation

### `coverImagePresentation: "full"`

Use for:

- illustration
- photography
- artwork
- image posts where the image should read as a normal large editorial image

House behavior:

- rendered wide on the detail page
- house max width: `900px`
- no inner padding panel

### `coverImagePresentation: "framed"`

Use for:

- title cards
- GitHub OG cards
- screenshot-like graphics
- text-forward graphics
- UI cards
- social-preview-style graphics

House behavior:

- rendered in a padded neutral frame
- house max width: `760px`
- preserves the graphic as a graphic instead of pretending it is a photo

### Hard rules

- Never render a text-forward title card as a raw full-width detail image.
- Published text posts must use `coverImagePresentation: "framed"`.
- If the asset would look wrong as a giant poster on the entry page, it is a `framed` case.
- `cardImageFit` does not control detail-page rendering.

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
- `coverImagePresentation`: `framed`
- `cardImage`: either a safer `1600 × 1000` or `1200 × 900` version, or reuse the title card with `cardImageFit: contain`
- `shareImage`: a dedicated `1200 × 630` social image

### Art / illustration post

Create:

- `coverImage`: original artwork
- `coverImagePresentation`: usually `full`
- `cardImage`: reuse artwork if crop-safe, otherwise export a thumbnail variant
- `shareImage`: dedicated `1200 × 630` share crop or padded adaptation

### Screenshot / GitHub preview / UI card post

Create:

- `coverImage`: the full screenshot if it serves the detail page
- `coverImagePresentation`: `framed`
- `cardImage`: usually the same file with `cardImageFit: contain`, unless you make a dedicated thumbnail
- `shareImage`: a dedicated `1200 × 630` graphic, not the raw screenshot
