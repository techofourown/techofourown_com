# Uploading Video to Cloudflare R2

How to upload video files to the `too-media` R2 bucket for first-party delivery via
`media.techofourown.com`.

See [ADR-0001](../decisions/ADR-0001-use-cloudflare-r2-and-cdn-for-first-party-video-delivery.md) for
the architectural decision behind this setup.

## Credentials

All Cloudflare credentials for this workflow are stored on **centroid** at:

```
/home/johnb/cloudflare token.txt
```

The file contains:

| Key | Used for |
|-----|----------|
| `access key ID` | rclone R2 remote (`too-media`) |
| `secret access key` | rclone R2 remote (`too-media`) |
| `account id` | rclone endpoint URL |
| `s3 api` | rclone endpoint URL |
| `token value` | General Cloudflare API token (R2 scope) |
| `cache purge token` | Cloudflare Cache Purge API |
| `zone id (techofourown.com)` | Cache purge API calls |

Do not commit credential values to this repository.

## Prerequisites

- **rclone** installed (`apt install rclone`) — already configured on centroid
- **ffmpeg** installed (`apt install ffmpeg`) — for converting non-MP4 source files
- **R2 bucket** (`too-media`) with custom domain (`media.techofourown.com`) connected

## Configure rclone

The `too-media` rclone remote is already configured on centroid. On a new machine, set it up
using the credentials from centroid:

```bash
rclone config create too-media s3 \
  provider=Cloudflare \
  access_key_id=<ACCESS_KEY_ID> \
  secret_access_key=<SECRET_ACCESS_KEY> \
  endpoint=https://<ACCOUNT_ID>.r2.cloudflarestorage.com \
  acl=private
```

Verify the connection by listing buckets:

```bash
rclone lsd too-media:
```

You should see the `too-media` bucket in the output.

## Convert source video to MP4

Videos must be MP4 (H.264) before uploading. If your source file is a different format
(e.g. `.webm`, `.mov`, `.mkv`), convert it first:

```bash
ffmpeg -i <SOURCE_FILE> \
  -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p \
  <OUTPUT_FILE>.mp4
```

If the source has no audio track, add `-an` to skip audio encoding:

```bash
ffmpeg -i <SOURCE_FILE> \
  -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p \
  -an \
  <OUTPUT_FILE>.mp4
```

If the source is already H.264 MP4, no conversion is needed — upload it directly.

Verify the output before uploading:

```bash
ffprobe <OUTPUT_FILE>.mp4
```

## Upload a video

Use `rclone copyto` with HTTP metadata headers so the file plays correctly in browsers:

```bash
rclone copyto \
  <LOCAL_FILE> \
  too-media:too-media/<PATH>/<FILENAME> \
  --s3-upload-concurrency 16 \
  --s3-chunk-size 64M \
  --progress \
  --header "Content-Type: video/mp4" \
  --header "Content-Disposition: inline; filename=\"<FILENAME>\"" \
  --header "Cache-Control: public, max-age=31536000, immutable"
```

### Example

Uploading a 115 MB video to the `videos/` directory:

```bash
rclone copyto \
  democracy_ai_vision.mp4 \
  too-media:too-media/videos/democracy_ai_vision.mp4 \
  --s3-upload-concurrency 16 \
  --s3-chunk-size 64M \
  --progress \
  --header "Content-Type: video/mp4" \
  --header "Content-Disposition: inline; filename=\"democracy_ai_vision.mp4\"" \
  --header "Cache-Control: public, max-age=31536000, immutable"
```

### What the flags do

| Flag | Purpose |
|------|---------|
| `--s3-upload-concurrency 16` | Parallel chunk uploads for speed |
| `--s3-chunk-size 64M` | Chunk size for multipart upload (good for large files) |
| `--progress` | Show upload progress |
| `Content-Type: video/mp4` | Browser recognizes the file as playable video |
| `Content-Disposition: inline` | Browser plays the video instead of downloading it |
| `Cache-Control: immutable` | CDN and browsers cache aggressively (1 year) |

### Why rclone and not Wrangler

Wrangler (Cloudflare's CLI) has a 315 MB upload limit. Video files routinely exceed this.
rclone uses the S3-compatible API with multipart uploads, which has no practical size limit.

## Verify the upload

Check the file exists in the bucket:

```bash
rclone ls too-media:too-media/videos/
```

Check the file is accessible and has correct headers:

```bash
curl -I https://media.techofourown.com/videos/<FILENAME>.mp4
```

Expected response:

```
HTTP/2 200
content-type: video/mp4
content-disposition: inline; filename="<FILENAME>.mp4"
cache-control: public, max-age=31536000, immutable
```

## Replacing a video

Because videos are cached with `Cache-Control: immutable`, replacing a file in R2 is not enough
on its own — the old version may remain cached at Cloudflare edge nodes. You must also purge
the cache.

### Step 1 — Upload the replacement

Upload the new file to the **same bucket path** as the original:

```bash
rclone copyto \
  <NEW_FILE>.mp4 \
  too-media:too-media/videos/<FILENAME>.mp4 \
  --s3-upload-concurrency 16 \
  --s3-chunk-size 64M \
  --progress \
  --header "Content-Type: video/mp4" \
  --header "Content-Disposition: inline; filename=\"<FILENAME>.mp4\"" \
  --header "Cache-Control: public, max-age=31536000, immutable"
```

### Step 2 — Purge the cache

Use the cache purge token from centroid's credentials file:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/28d253589f420799fba7af3db433b470/purge_cache" \
  -H "Authorization: Bearer <CACHE_PURGE_TOKEN>" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://media.techofourown.com/videos/<FILENAME>.mp4"]}'
```

A successful response looks like:

```json
{"success": true, "errors": [], "messages": [], "result": {"id": "28d253589f420799fba7af3db433b470"}}
```

### Step 3 — Verify

```bash
curl -I https://media.techofourown.com/videos/<FILENAME>.mp4
```

Confirm `content-length` matches the new file size. The `cf-cache-status` header will show
`DYNAMIC` or `MISS` immediately after a purge, indicating the edge is serving fresh from R2.

## Bucket path conventions

Files in the `too-media` bucket are organized by type:

```
too-media/
└── videos/
    └── <filename>.mp4
```

The public URL maps directly to the bucket path:

```
https://media.techofourown.com/videos/<filename>.mp4
```

## Moving files within the bucket

If a file was uploaded to the wrong path, use `rclone moveto`:

```bash
rclone moveto \
  too-media:too-media/<OLD_PATH> \
  too-media:too-media/<NEW_PATH>
```

Note: HTTP metadata headers are set during upload and preserved during moves.

## Listing bucket contents

```bash
# List all files
rclone ls too-media:too-media/

# Show directory tree
rclone tree too-media:too-media/

# List with timestamps and sizes
rclone lsl too-media:too-media/
```
