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
3. **Production toolchain check.** Confirm every tool in the "Required tools" table of your instructions:
   - `ffmpeg -hide_banner -filters | grep -E "loudnorm|ebur128"` and `ffmpeg -hide_banner -encoders | grep libx264`
   - `python3 -c "import PIL"`
   - `node --version` and a test render of a 2-slide carousel with `render_carousel.mjs`
   - Higgsfield: call `balance`, and record the plan and credits in `community-guide`
   - **Smoke test:** in a scratch folder, run
     `ffmpeg -f lavfi -i testsrc2=s=720x1280:d=6 -f lavfi -i sine=d=6 -shortest -pix_fmt yuv420p raw.mp4`
     then write `captions.json` as `{"segments":[{"start":0,"end":6,"lines":[{"text":"Smoke test","size":84}]}]}`,
     then `python3 <skill>/scripts/finish_video.py raw.mp4 captions.json out/`,
     then `python3 <skill>/scripts/qa_video.py out/final.mp4 --max-shot 10 --out out/qa/`, and confirm `"result": "PASS"`.
   Post the results as one comment. List anything missing as a single install checklist for the board.
4. **Profile audit** (both platforms): bio (who we help + result + CTA), profile photo, link in bio, IG highlights (Services, Results, Process, FAQ) and pinned posts. Propose changes in the first weekly approval packet via the Creative Director.
5. Write the first version of `community-guide`: reply tone, top 10 FAQ answers from the brand book, comment-keyword CTA responses and lead-routing rules.
6. Create the `metrics-log` table header (see `social-publishing`). If the accounts already have posts, backfill the last 30 posts' metrics so the baseline doesn't start from zero.
