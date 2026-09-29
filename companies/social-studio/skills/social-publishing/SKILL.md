---
name: social-publishing
description: Publish approved posts to Instagram and TikTok via official APIs (or a manual hand-off fallback), pull post metrics, and log them in the metrics log. Use for daily publishing and metrics collection.
---

# Social Publishing

**Hard rule:** publish only posts that belong to a board-approved weekly packet, in the publish window (morning, midday or evening) of their approved slot. If there's any doubt, don't publish. Ask the Creative Director.

## 1. Access modes (detect once, record in the `community-guide` document)

| Mode | When | What you do |
| --- | --- | --- |
| **API** | Tokens present (see below) | Publish and read metrics directly |
| **Scheduler** | The owner uses a scheduling tool the team can reach | Schedule through it and read its analytics |
| **Manual hand-off** | No access | At slot time, post a "Ready to post" comment on the post issue mentioning the board, with the asset attached, captions to copy and a 3-step checklist. Ask the owner to paste the live link back. Keep this under 2 minutes of owner effort per post. |

Always prefer API mode. If it isn't configured, raise it in the Channel Setup issue once, not on every heartbeat.

## 2. Instagram (Graph API; business or creator account linked to a Facebook Page)

Env: `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID`. Media must be at a publicly reachable URL when you create the container.

- **Reel:** `POST /{ig-user-id}/media` with `media_type=REELS`, `video_url`, `caption`, optional `cover_url` and `share_to_feed=true`. Poll `GET /{container-id}?fields=status_code` until `FINISHED`, then `POST /{ig-user-id}/media_publish` with `creation_id`.
- **Carousel:** create one child container per slide (`is_carousel_item=true`), then a parent container with `media_type=CAROUSEL` and `children=<ids>`, then publish.
- **Story:** `media_type=STORIES` with `image_url` or `video_url`.
- **Metrics:** `GET /{media-id}/insights?metric=reach,views,likes,comments,shares,saved,total_interactions` (Reels also have watch-time metrics). Account-level: follower count and profile activity.
- API versions, limits and metric names change. If a call errors, check the current Meta documentation and record what changed in `community-guide`.

## 3. TikTok (Content Posting API + Display API)

Env: `TIKTOK_ACCESS_TOKEN`.

- **Publish:** Content Posting API `POST /v2/post/publish/video/init/` (direct post) with the video source and post info (title/caption, privacy level, comment settings). Photo posts use the content init endpoint with `media_type=PHOTO`. Poll the publish status endpoint until done.
- **Unaudited apps can only post privately.** If posts land as private, fall back to manual hand-off and tell the board the app needs TikTok's audit.
- Alternatively, use the inbox/draft upload flow so the owner taps "post" in the app (about 30 seconds of effort) with the caption pre-filled.
- **Metrics:** Display API `POST /v2/video/query/` or `/v2/video/list/` with fields `view_count,like_count,comment_count,share_count`. Note: TikTok's API doesn't expose everything the app shows (e.g. saves, watch time). Ask the board for a monthly screenshot of TikTok Studio analytics to fill the gaps.
- Mark AI-generated content with TikTok's AI-generated content setting when it applies.

## 4. Publishing checklist (per post)

1. Confirm the post issue has an approved verdict and slot from the Creative Director.
2. Re-check the asset spec and that the caption matches the platform.
3. Publish (or hand off). Verify it's live and public by reading back the permalink.
4. Comment the permalink(s) on the post issue, with a timestamp.
5. Within the first hour: reply to early comments and pin the best one.
6. Share it to IG Stories with a "new post" sticker.

## 5. Metrics log

The `metrics-log` document has one row per post per platform. Fill it in at 24h, 72h and 7d:

```
| id | date | platform | format | pillar | hook type | tag | views | reach | likes | comments | shares | saves | follows | profile visits | link clicks | DMs/leads | avg watch % | notes |
```

- Use the hypothesis tag from the brief exactly, so the learning loop can group results.
- Record leads (DMs asking about services, audit requests) against the post that triggered them. This is the metric that matters most.
- Missing a metric? Leave it blank. Never estimate or invent numbers.

## 6. When things go wrong

- **Publish failed:** retry once. If it fails again, switch to manual hand-off for that post and log the error on the issue.
- **Post underperforms badly in the first hours:** do not delete it (deleting hurts reach and loses data). Log it and let the learning loop handle it.
- **Mistake in a live post** (typo, wrong fact): factual errors get corrected in the caption or pinned comment right away and flagged to the Creative Director. Only the board can decide to delete a post.
- **Negative pile-on or sensitive comment thread:** stop replying and escalate to the board with a summary.
