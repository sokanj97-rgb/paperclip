---
name: content-production
description: Turn a creative brief into finished, platform-native Instagram and TikTok posts — short-form video scripts and edits, carousels, stories, captions, covers and keywords. Use whenever producing or revising a post.
---

# Content Production

A brief is done when the post can be published as-is: finished asset, captions, cover, keywords and alt text, all attached to the issue.

## 1. Before you make anything

1. Read the brief, the `brand-book` (voice, colors, fonts, do/don't) and the playbook rules it cites.
2. Pick or improve the hook. Write **5 more hook variants** and choose the strongest. The hook decides most of the post's result, so spend real effort here.
3. Write the whole script or slide copy first. Edit it for fewer words, more specifics and one idea.

## 2. Hook craft

A hook needs to do three things in under 2 seconds: **stop** (visual change or bold text), **target** (the viewer knows it's for them) and **promise** (a reason to keep watching).

Formulas that work in this niche (tag each post with the one you used):

- **Negative callout**: "If your website still has this, you're losing clients."
- **Specific result**: "This one headline change doubled a plumber's calls."
- **Before/after reveal**: show the ugly "before" at frame one and the promise of the "after".
- **Roast / teardown**: "Rating small-business websites (brutally honest)."
- **Myth-bust**: "Stop putting sliders on your homepage."
- **Mistake list**: "3 copy mistakes killing your contact form."
- **Question they're already asking**: "Why does nobody fill out your contact form?"
- **Contrarian**: "You don't need a new website. You need new words."

On-screen hook text: at most ~8 words, readable in 1 second, and consistent with the spoken line.

## 3. Short-form video (Reels + TikTok)

**Spec:** 9:16, 1080×1920, 30fps, ≤ 60s by default (15–35s is typical for tips; teardowns can run longer if retention holds). Captions burned in. Keep text out of the UI zones: top ~250px, bottom ~350px, right ~120px.

**Structure:**
```
0–2s    Hook: visual + on-screen text + spoken line all land together
2–5s    Stakes: why it matters to them (lost leads, wasted money)
5–Ns    Payoff: the value, one point per beat, visual change every 2–4s
last 3s CTA: one action, stated plainly; loop back to the start where possible
```

**Formats an agent can make without filming** (prefer these by default):

- **Website scroll teardown**: record a headless-browser scroll of a (mock, permitted or our own) site at 1080×1920, then overlay annotations and captions. This suits the niche perfectly.
- **Before/after**: two renders of a page (old vs. redesigned), split screen or wipe transition.
- **Kinetic text / talking-text**: bold animated text over a brand background or B-roll, with a TTS or owner voiceover.
- **Screen-recorded process**: time-lapse of a build in a site builder or code, with captions.
- **AI-generated B-roll or visuals**, if a generation tool is connected. Stay on brand, avoid uncanny realistic people, and apply the AI-content label where required.

**Formats needing the owner** (talking head, face-to-camera): write a tight script plus a shot list and put them in "Needs from owner". Owner filming is batched into one weekly ~20-minute session, so always ship a no-filming fallback too.

**Tooling suggestions:** Playwright for captures and scroll recordings, ffmpeg for editing, captions, concatenation and loudness normalization (-14 LUFS), and any connected image, video or TTS tools. Keep project files and source assets attached to the issue so revisions are cheap.

**Sound:** voiceover or on-screen text must carry the post with sound off. Use trending audio only when it's licensed for business use on that platform (use the platform's commercial music library for business accounts).

## 4. Carousels (IG carousel + TikTok photo mode)

**Spec:** 1080×1350 (4:5) for IG. Reuse the slides for TikTok photo mode, checking crop. 6–10 slides.

**Structure:**
```
Slide 1   Hook: big promise or bold claim + visual cue to swipe
Slide 2   Context or the problem (make them feel it)
Slides 3–N One point per slide: headline + 1–2 lines + visual example (screenshot, mockup, before/after)
Last-1    Summary or checklist (the "save this" slide)
Last      CTA: save, share with someone who needs it, comment keyword, or DM
```

Build slides as HTML/CSS using the brand-book fonts and colors, and render to PNG with a headless browser at exact size. Body text ≥ 28px equivalent, high contrast, consistent layout grid, and a slide counter or progress cue.

## 5. Stories (IG)

Lightweight and frequent: a poll or quiz tied to this week's topic, a behind-the-scenes shot, reshares of our new posts with a "new post" sticker, and a link sticker to the offer once a week. Stories build DM conversations, so use question stickers.

## 6. Captions

**Instagram:** first line = a second hook (it shows before "more"). Then 3–8 short lines of added value (not a transcript), a single CTA, and 3–5 specific hashtags. Include the searchable keywords naturally ("web design for small business", "website copywriting").

**TikTok:** shorter. One line of context + keywords people search for (TikTok is a search engine: "how to get more website leads") + 3–5 hashtags. Put the search keywords in on-screen text and voiceover too.

Voice: follow the brand book. By default: confident, plain-spoken, a little cheeky, zero jargon without a translation, never salesy.

## 7. Deliverables checklist (attach to the issue)

- [ ] Final asset(s) at exact spec, plus a cover frame or thumbnail
- [ ] Script or slide copy (text)
- [ ] IG caption, TikTok caption
- [ ] Keywords, 3–5 hashtags per platform, alt text
- [ ] Hypothesis tag copied from the brief (plus the actual hook type used)
- [ ] Sources for any stat or claim; permission noted for any real business shown
- [ ] "Needs from owner" section (if any) + fallback version
- [ ] Self-score using the `quality-gate` rubric (hook ≥ 4 before hand-off)
