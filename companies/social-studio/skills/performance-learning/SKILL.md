---
name: performance-learning
description: Turn post metrics into learning — baseline scoring, winner/loser classification, hypothesis testing, and playbook updates — so each week's content is better than the last. Use for the weekly performance review and when checking what the data says before planning.
---

# Performance Learning

This loop is what makes the team improve without human coaching. Research produces **hypotheses**. Only our own results turn a hypothesis into a **rule**.

## 1. What we optimize, in priority order

1. **Qualified leads**: DMs about services, audit requests, link clicks to booking.
2. **Follows per 1,000 views**: are the right people subscribing?
3. **Shares + saves per 1,000 views**: was it valuable enough to keep or send?
4. **Retention**: average watch % and completion for video; swipe-through for carousels.
5. **Reach/views**: distribution. Necessary, but a vanity metric on its own.

A post with modest views and 3 real leads beats a viral post with none. Keep this ordering when the numbers disagree.

## 2. Baseline and scoring (weekly, Sun)

1. Using the `metrics-log`, compute our **trailing 30-day median** for each metric, per platform and format (Reels ≠ carousels ≠ TikTok).
2. For each post that reached 7 days, compute a **performance index**:
   `index = 0.35·(leads vs median) + 0.25·(follows/1k vs median) + 0.25·((shares+saves)/1k vs median) + 0.15·(views vs median)`
   Each term is a ratio to the median, capped at 5×. If leads are zero for everyone, drop that term and renormalize.
3. Classify: **winner** ≥ 1.5, **average** 0.67–1.5, **loser** ≤ 0.67.
4. For the first ~4 weeks (under 20 posts), baselines are noisy. Say so in reports and lean on the research hypotheses.

## 3. Updating the playbook

The `playbook` document has three sections. Update them every week:

```
## Rules (proven on our account)
- <pattern> — evidence: <n> wins / <n> tries, avg index <x> — posts: <ids> — since <date>

## Hypotheses (being tested)
- <pattern> — source: <swipe-file entries or our data> — tries so far: <n> — status: testing

## Retired
- <pattern> — why: <n> losses / <n> tries, or owner cut — date
```

Promotion and retirement:

- **Promote** a hypothesis to a rule after ≥ 3 tries with ≥ 2 winners and an average index ≥ 1.3.
- **Retire** after ≥ 3 tries with no winner and an average index < 0.8.
- **Demote** a rule back to a hypothesis if its last 4 uses average < 1.0. Audiences and algorithms shift.
- Change **one variable at a time** when testing (same hook type with a different topic, or the same topic with a different format). Otherwise we can't tell what caused the result.

## 4. Remix winners

- Every winner gets a follow-up within 2 weeks: same structure on a new topic, or a part 2 if comments ask for it.
- A strong winner (index ≥ 2.5) gets a cross-format remix (Reel → carousel or vice versa), and a re-post with a new hook after 45–60 days.
- Mine comments on winners for next topics. Questions in comments are free research.

## 5. Weekly learning report (comment on the Content OS issue)

```
Learning report — week of <date>
Posts scored: <n>   Winners: <list with index>   Losers: <list with index>
Leads this week: <n> (source posts: ...)   Followers: <+n>
What worked: <2–3 bullets, each with evidence>
What didn't: <1–2 bullets with evidence>
Playbook changes: promoted <...>, retired <...>, new hypotheses <...>
Next week: <the 70/20/10 plan in one line each>
```

Keep it short and evidence-first. If a conclusion rests on one post, call it a signal, not a finding.

## 6. Guardrails

- Never invent or estimate missing metrics. Blank means unknown.
- Don't chase a single viral outlier. Look for patterns across posts.
- Be suspicious of spikes from outside our audience (e.g. viral with other designers but zero leads). Note them, but don't optimize for them.
