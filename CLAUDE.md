# insta-automation

Instagram post automation. Generates a text image locally (Pillow) and publishes it to Instagram via the
Graph API. Account: **@memes_on_ai** (MEDIA_CREATOR).

## Architecture

- `generate_post.py` — Pillow, renders wrapped text onto a 1080x1080 JPEG.
- `post_to_instagram.py` — Instagram Graph API: creates a media container, then publishes it.
- Secrets in `.env` (gitignored). Template in `.env.example`.
- Roadmap: Phase 2 adds MoviePy for animated text video, posted as a Reel.

## Meta/Instagram API setup

This project uses **Instagram API with Instagram Login** (a.k.a. Business Login for Instagram) — chosen
because it does not require linking a Facebook Page. Permissions: `instagram_business_basic`,
`instagram_business_content_publish`.

- Personal-use apps (posting only to accounts you own) do **not** need Meta App Review — Standard Access
  is enough.
- Before the dashboard's "Generate access token" step will work, you must add your IG account as an
  **Instagram Tester** under App roles → Roles, then accept the invite from the Instagram app (Settings →
  Apps and websites → Tester invites). Skipping this causes an "Insufficient Developer Role" error.

## Critical gotchas

1. **Host is `graph.instagram.com`, not `graph.facebook.com`.** This project uses the Instagram Login
   flow, which has its own host — different from the older Facebook-Login flow most example code online
   assumes.
2. **IG_USER_ID must be the canonical ID, not the ID shown in the dashboard.** `GET /me` on
   graph.instagram.com returns two different ID fields (`user_id` and `id`). The dashboard displays the
   `user_id`-style value, but graph.instagram.com treats `id` as canonical (verified empirically: looking
   up either ID always reports back the same `id` value). **Use `id` as IG_USER_ID.** Current value:
   `36885696844409943`.
3. **Images must be JPEG** — max 8MB, aspect ratio 4:5 to 1.91:1, width 320–1440px, sRGB. (PNG worked once
   in testing — Instagram silently converted it — but that's undocumented behavior; don't rely on it.)
4. **`image_url`/`video_url` must be publicly reachable.** Instagram's servers fetch it themselves; there
   is no direct binary upload for images. (Video is the exception — it supports direct local upload via a
   separate resumable-upload endpoint at `rupload.facebook.com`.) We use a public GitHub repo +
   `raw.githubusercontent.com` as the public host.
5. **The source file can be deleted right after `media_publish` succeeds.** Meta ingests a copy at
   container-creation time; it doesn't keep re-fetching from the original URL. Containers expire if not
   published within 24h of creation.
6. **This machine has two GitHub SSH identities.** Bare `git@github.com` resolves to the *work* account
   (`saichandu-juluri`). This repo belongs to the *personal* account (`julurisaichandu`) — always use the
   `github-personal` SSH host alias (`~/.ssh/config`) for git remote operations here, e.g.
   `git@github-personal:julurisaichandu/insta-automation.git`.

## Instagram Content Publishing limits

- **50 published posts per rolling 24-hour period** — images, videos, Reels, and carousels all share this
  one quota (a carousel counts as 1 post regardless of item count; max 10 items/carousel). Check live
  usage: `GET /{IG_USER_ID}/content_publishing_limit?fields=quota_usage,config`.
- Caption: 2200 characters max, 30 hashtags max, 20 mentions max.
- Reels: MOV/MP4, max 300MB, 3s–15min, H264/HEVC + AAC audio, 9:16 recommended.
- Stories: MOV/MP4, max 100MB, 3s–60s, 9:16 recommended.
- **The real ceiling is lower than 50/day.** Instagram's spam/bot detection profiles posting behavior
  independent of the API quota — posting near 50/day, on exact cron intervals, with repetitive caption
  structure, risks a shadowban or action-block even while technically within the documented limit.
  Realistic safe cadence: **1–3 posts/day**, with randomized timing.

## Secrets

- `IG_USER_ID`, `IG_ACCESS_TOKEN` live in `.env` only — never commit, never paste into a chat/AI session.
- Token is long-lived (60 days). Exchange a short-lived token via
  `GET graph.instagram.com/access_token?grant_type=ig_exchange_token` (needs app secret). Refresh a
  long-lived one before it expires via
  `GET graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token` (no app secret needed).
- API version pinned to `v25.0` in both scripts.

## Roadmap

- [x] Phase 1: static image post (Pillow + Graph API) — working. First live post:
      https://www.instagram.com/p/Dav5eP0oKPf/
- [ ] Phase 2: animated text video via MoviePy, posted as a Reel (direct local upload, no public hosting
      needed for video).
- [ ] Automate via GitHub Actions cron; move secrets to GitHub Actions encrypted secrets.
- [ ] Decide the content source for "context" (manual input vs LLM-generated vs feed-driven).
