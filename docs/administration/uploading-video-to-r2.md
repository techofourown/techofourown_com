# Uploading Video to Cloudflare R2

How to upload video files to the `too-media` R2 bucket for first-party delivery via
`media.techofourown.com`.

See [ADR-0001](../decisions/ADR-0001-use-cloudflare-r2-and-cdn-for-first-party-video-delivery.md) for
the architectural decision behind this setup.

## Prerequisites

- **rclone** installed (`apt install rclone`)
- **R2 API credentials** (S3-compatible): Access Key ID, Secret Access Key, Account ID
- **R2 bucket** (`too-media`) with:
  - Custom domain connected (`media.techofourown.com`)
  - Public Development URL enabled

R2 API credentials are created in the Cloudflare dashboard under R2 → Manage R2 API Tokens. These are
separate from Cloudflare API tokens used for DNS or Terraform.

## Configure rclone

Create an rclone remote named `too-media`:

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

Uploading a 747 MB video to the `videos/` directory:

```bash
rclone copyto \
  woodbox_demo_parts_procurement_v1.mp4 \
  too-media:too-media/videos/woodbox_demo_parts_procurement_v1.mp4 \
  --s3-upload-concurrency 16 \
  --s3-chunk-size 64M \
  --progress \
  --header "Content-Type: video/mp4" \
  --header "Content-Disposition: inline; filename=\"woodbox_demo_parts_procurement_v1.mp4\"" \
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
curl -I https://media.techofourown.com/videos/woodbox_demo_parts_procurement_v1.mp4
```

Expected response:

```
HTTP/2 200
content-type: video/mp4
content-disposition: inline; filename="woodbox_demo_parts_procurement_v1.mp4"
cache-control: public, max-age=31536000, immutable
```

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
