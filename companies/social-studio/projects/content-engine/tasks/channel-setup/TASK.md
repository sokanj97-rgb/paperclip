---
name: Channel setup — access, profiles, publishing mode
assignee: social-media-manager
project: content-engine
---

Get the channels ready and work out how we'll publish and measure.

1. **Access.** Check for `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID` and `TIKTOK_ACCESS_TOKEN`. Test a read call for each (profile info, recent media). Record the working publishing mode per platform (API / scheduler / manual hand-off) in the `community-guide` document.
2. If access is missing, write the board **one** short, step-by-step request covering both platforms:
   - Instagram: switch to a Professional (business/creator) account, link it to a Facebook Page, create a Meta app with Instagram publishing and insights permissions, and add the token and account ID as company secrets.
   - TikTok: create a TikTok for Developers app with Content Posting and Display (video list) scopes, connect the account and add the token. Note that posts stay private until TikTok audits the app, so manual hand-off is used until then.
   Until access exists, use manual hand-off mode. Never block production on it.
3. **Profile audit** (both platforms): bio (who we help + result + CTA), profile photo, link in bio, IG highlights (Services, Results, Process, FAQ) and pinned posts. Propose changes in the first weekly approval packet via the Creative Director.
4. Write the first version of `community-guide`: reply tone, top 10 FAQ answers from the brand book, comment-keyword CTA responses and lead-routing rules.
5. Create the `metrics-log` table header (see `social-publishing`). If the accounts already have posts, backfill the last 30 posts' metrics so the baseline doesn't start from zero.
