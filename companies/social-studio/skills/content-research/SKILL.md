---
name: content-research
description: Systematically study top-performing Instagram and TikTok content, find outliers, tear them down into reusable patterns, and maintain the swipe file. Use for the weekly research sweep, the monthly deep study, or whenever a brief needs evidence.
---

# Content Research

The goal is **pattern extraction, not imitation**. You are looking for posts that did far better than normal *for the account that posted them*, then working out why, in enough detail that we can apply the mechanism to our own topics.

## 1. What counts as "top material"

Raw view counts mislead because big accounts get big numbers for mediocre posts. Use **outliers**:

- **Outlier score** = post engagement ÷ that account's median engagement over its last 20–30 posts. Engagement = likes + comments×3 + shares×4 + saves×4 where available; otherwise views.
- **Study:** outlier score ≥ 3× (strong) or ≥ 2× (worth a look).
- A small account (5k followers) with a 10× outlier teaches more than a 2M account's average post.

## 2. Sources, in priority order

Use whichever are available. Note in the swipe file which source each entry came from.

1. **Instagram Business Discovery (Graph API).** If `INSTAGRAM_ACCESS_TOKEN` and `INSTAGRAM_BUSINESS_ACCOUNT_ID` are set, pull public business/creator accounts' recent media with like and comment counts:
   `GET https://graph.facebook.com/v21.0/{ig-user-id}?fields=business_discovery.username(<handle>){followers_count,media_count,media.limit(30){caption,like_count,comments_count,media_type,media_product_type,permalink,timestamp}}`
   Compute outlier scores yourself. (API versions and field names change; check the current Meta docs if a call fails.)
2. **Meta Ad Library** (public web): competitor ads that have run for 30+ days are almost certainly profitable. Study their hooks and offers.
3. **TikTok Creative Center** (public web): trending hashtags, songs, creators and top ads by industry and region.
4. **Web search** for recent breakdowns of viral posts in the niche, and for the accounts in the watchlist.
5. **Board swipe drops**: links the owner pastes as comments on the Content OS issue. Always process these first.
6. **Our own winners** from the `metrics-log`. These are the most relevant data we have.
7. Optional: video-analysis or virality-prediction tools, if connected. Treat their output as one input, not a verdict.

If a platform page is behind a login wall and no API is available, don't guess what's in it. Record the link and move on, or ask the board for a swipe drop.

## 3. The watchlist

Keep a `## Watchlist` section at the top of the `swipe-file` document with 25–40 handles in three rings:

- **Direct niche (~50%)**: web designers, agencies, copywriters, hosting and dev creators who sell to small businesses.
- **Audience-adjacent (~30%)**: creators our buyers already follow: small-business growth, marketing, local-business owners, founders.
- **Craft (~20%)**: best-in-class short-form accounts in any niche, studied for hooks, editing and storytelling.

Review the watchlist monthly: drop accounts that never produce outliers and add accounts that appear repeatedly in research.

## 4. Teardown template (one per studied post)

Append each teardown to the `swipe-file` document:

```
### <short name> — @handle — <platform> — <date posted>
Link: <permalink>          Source: <graph-api | ad-library | creative-center | web | board | ours>
Numbers: <views/likes/comments/shares/saves> · account median <x> · outlier <n>×
Format: <talking head | text-on-screen | screen recording | carousel | before/after | green-screen | ...>  Length: <s or slides>
Hook (verbatim first line / first frame): "..."
Hook mechanism: <curiosity gap | negative callout | bold claim | specific number | pattern interrupt | "you're doing X wrong" | before/after reveal | relatable pain | ...>
Structure: <beat-by-beat: 0-2s ..., 2-8s ..., payoff at ..., CTA>
Retention devices: <open loop, list countdown, visual change every Ns, reveal held to end, ...>
Why it spread: <save-worthy reference? shareable identity/opinion? comment-bait question? controversy?>
CTA: <what and how>
Transferable pattern: <one sentence we can reuse for web design / hosting / copy>
Tags: hook:<type> format:<type> pillar:<closest pillar> emotion:<type>
```

The **transferable pattern** line is required and is the whole point of the teardown. If you can't write it, the post isn't useful to us.

## 5. Weekly sweep (Mon, about 60–90 minutes of effort)

1. Process board swipe drops.
2. Pull recent posts (last 14 days) from at least 15 watchlist accounts. Find outliers ≥ 2×.
3. Check TikTok Creative Center and Meta Ad Library for the niche.
4. Write at least 10 new teardowns, at least 3 of them from outside the direct niche.
5. Cluster the week's teardowns: which hook mechanisms, formats and topics repeat? Write a 5-line "What's working this week" summary at the top of the swipe file.
6. Feed candidate patterns into the `playbook` as **hypotheses**, not rules. Rules come only from our own results (see `performance-learning`).

## 6. Monthly deep study (1st of month)

1. Pick the 3 accounts in our niche that grew fastest last month. For each, study the 10 most recent posts and the 5 all-time top posts, and write an account-level teardown: positioning, pillar mix, cadence, recurring series, visual identity, CTA strategy and what we should adopt.
2. Re-read the whole swipe file and merge duplicate patterns. Archive entries older than 90 days that never turned into a hypothesis.
3. Review the watchlist (section 3).
4. Summarize the month in the learning report: what patterns are rising or fading, and what we'll try next month.

## 7. Guardrails

- Never copy captions, scripts, footage, audio or visuals. Record them only for analysis, with a link back to the original.
- Never scrape in ways that break platform terms. Use official APIs, public pages and board-provided links.
- Never engage with watchlist accounts from the business account as part of research (no likes or follows) unless the playbook says to.
