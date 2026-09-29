---
name: quality-gate
description: Score social posts against a strict 10-point creative rubric, return actionable revision notes, and assemble the weekly board approval packet. Use when reviewing drafts or preparing content for owner approval.
---

# Quality Gate

The bar is "would this stop a busy small-business owner mid-scroll and make them trust us more?" Anything that doesn't clear it gets revised or killed. Posting weak content isn't neutral: it trains the algorithm and the audience that we're skippable.

## 1. Rubric (score each 1–5)

| # | Dimension | 5 looks like |
| --- | --- | --- |
| 1 | **Hook** | Stops the scroll in < 2s; clear who it's for and what they get |
| 2 | **One idea** | A single, sharp takeaway; nothing that dilutes it |
| 3 | **Value density** | Viewer learns or feels something they'd save or send to someone |
| 4 | **Specificity and proof** | Concrete numbers, examples and visuals, not generic advice |
| 5 | **Retention craft** | Pacing, visual changes, open loops; no dead seconds or dead slides |
| 6 | **Visual craft** | Legible on a phone, on brand, safe zones respected, polished |
| 7 | **Platform-native** | Feels made for this platform; right length, sound, text, no watermarks |
| 8 | **Brand voice** | Sounds like the brand book, not like generic marketing |
| 9 | **CTA fit** | One clear action that matches the post's intent |
| 10 | **Originality** | Uses a proven *pattern* but is clearly ours; not a clone of a swipe-file post |

**Pass:** total ≥ 40/50, no dimension below 3, **Hook ≥ 4**, and every compliance check below passes.

## 2. Compliance checks (any fail = automatic revise)

- [ ] Every fact, stat and result is sourced or verified in the brand book
- [ ] No invented clients, testimonials, reviews or screenshots
- [ ] No guarantees or misleading claims (rankings, income, "overnight" results)
- [ ] Real businesses shown only with permission or clearly anonymized
- [ ] Music and footage are licensed for business use on the platform
- [ ] AI-generated realistic media is labeled where the platform requires it
- [ ] Nothing that contradicts the brand book's do/don't list

## 3. Revision notes

Notes must be specific and actionable. Name the timestamp or slide, what's wrong and what to do instead.

- Bad: "Hook could be stronger."
- Good: "0–2s: hook text is 14 words, and the visual doesn't change until 3s. Cut to 'Your contact form is scaring people off' and open on the red-highlighted form."

A maximum of 2 revision rounds per post. After that, kill the post, record why in the `playbook` (under retired ideas or lessons), and pull a backup idea from the calendar.

Post the scorecard as a comment on the post issue:

```
Quality gate — round <n>
Hook 4 · One idea 5 · Value 4 · Specific 4 · Retention 4 · Visual 4 · Native 5 · Voice 4 · CTA 4 · Original 4 = 42/50
Compliance: pass
Verdict: approved-internal | revise | kill
Notes: <numbered, actionable>
```

## 4. Weekly approval packet (one `request_board_approval` per week)

Keep it scannable in 5–10 minutes. Link every post issue in `issueIds`.

```
Week of <date> — <n> posts ready (<n> Reels/TikToks, <n> carousels, <n> stories plan)

Last week in one line: <e.g. "Teardown Reels 2.4× baseline; offer post flopped — details in learning report">

| # | Slot | Platform | Format | Hook | Score | Link |
|---|------|----------|--------|------|-------|------|
| 1 | Mon 12:00 | IG+TT | Reel | "Your contact form is scaring people off" | 44 | <issue link> |
...

Needs from you (optional — fallbacks are ready):
- Film 3 clips (~15 min): scripts on posts #2, #5
- Confirm: can we name <client> in post #4?

Proposed change (at most one): <strategy change + evidence>

Reply "approve all", or list post numbers to cut or change.
```

When the approval resolves: approved posts go to the Social Media Manager with their slots, and posts with requested changes go back into revision with the owner's notes quoted. If the owner cuts a post, log the reason in the `playbook` because it's a taste signal about the brand.
