# AI video recipe (Higgsfield)

The exact method behind the reference test post (`references/test-post-food-tracker/` at the package root). Follow it step by step. Deviate only when the playbook has evidence something else works better.

## 0. Requirements

- The **Higgsfield MCP server** is connected to the Claude Code install that runs this agent. The tools you need are `generate_video`, `models_explore`, `jobs_wait` and `balance`. If they're missing, you can't make AI footage: say so in the Channel Setup issue and use a no-AI format (section 6).
- `ffmpeg` and `python3` with Pillow, for `scripts/finish_video.py` and `scripts/qa_video.py`.

## 1. Check the budget first

1. Call `balance`. Compare it against the weekly credit budget in the `brand-book`, defaulting to 150 credits/week if none is set.
2. Preflight every generation with `get_cost: true`. **Cap: 60 credits per post for first cuts** (two attempts of the default). Spending more needs the Creative Director's note on the brief.
3. If the balance won't cover the week's briefs, tell the Creative Director before producing so they can cut or re-format posts. Never let a routine run the account dry.

## 2. Model defaults

| Use | Model and settings | Cost (Sept 2026) |
| --- | --- | --- |
| **First cut** (default for every AI video) | `kling3_0`, `mode: "std"`, `duration` ≤ 15, `aspect_ratio: "9:16"`, `sound: "on"` | about 30 credits for 15s |
| Longer than 15s | `seedance_2_5`, `mode: "t2v"`, duration 4–30, 720p | preflight (about 105 for 15s) |
| **Approved hero re-render** (sharper faces/text) | `kling3_0` `mode: "pro"`, or `seedance_2_5` at `resolution: "1080p"` | preflight (about 180 for Seedance 15s 1080p) |

Seedance `draft` mode needs a Plus plan or higher. Don't use it on Starter. Prices and models change: when a call fails or a price looks off, run `models_explore` with `action: "get"` to check.

## 3. Prompt template (proven)

```
Vertical 9:16 smartphone-style lifestyle video, natural UGC look, <setting>, <lighting>, <color grade>.
<ONE consistent character: age, hair, clothing — repeated so every shot matches>.
<N> quick shots, handheld with gentle motion:
Shot 1 (0-3s): <hook visual — motion or a reveal at frame one>.
Shot 2 (3-7s): <...>.
Shot 3 (7-11s): <...>.
Shot 4 (11-15s): <payoff / resolution>.
Audio: <music mood>, <ambience>, <1–2 specific sound effects on key moments>. No speech, no dialogue, no voiceover.
No on-screen captions, no readable text, no logos, no watermarks.
```

Rules:
- **Shots of 3–4 seconds** that match the caption beats. The QA check fails any shot over 5 seconds.
- **Never ask the model for words.** Screens show "clean minimal interface, no readable text". All text is added in post.
- **No generated speech.** Voiceover comes from the owner or a TTS tool. Lip-sync artifacts kill trust.
- Describe the hook moment concretely: motion at frame one beats a static establishing shot.
- Real products, apps or client sites never come from generation. Composite the real screen recording or screenshot in post, or use a screen-recording format instead.

## 4. Generate, wait, download

1. `generate_video` with the settings above. Save the job id on the issue.
2. `jobs_wait` until it finishes. A 15s Kling clip takes about 3–6 minutes. Poll roughly every 15 seconds rather than hammering the API.
3. Download the `result_url` with `curl -fL -o raw.mp4 <url>`. If your network blocks the CDN, do the finishing steps inside Higgsfield's `sandbox_exec`: it has ffmpeg and Pillow, and its output can be uploaded back through `media_upload`.

## 5. Finish and QA (mandatory, never skip)

```bash
python3 scripts/finish_video.py raw.mp4 captions.json out/    # captions snapped to cuts, 1080x1920, -14 LUFS, cover
python3 scripts/qa_video.py out/final.mp4 --out out/qa/       # must print "result": "PASS"
```

Then **open `out/qa/qa-sheet.jpg` and look at it.** Check hands (finger count, grip), faces (eyes, teeth), phone screens (no garbled text) and the product. If any frame has a visible artifact, regenerate once with a prompt fix (e.g. "hands out of frame", "phone screen facing away"). If the second attempt also fails, switch to a no-AI format.

Attach `final.mp4`, `cover.jpg`, `finish-report.json`, `qa-report.json` and `qa-sheet.jpg` to the post issue.

## 6. No-AI formats (fallback, and often better for this niche)

- **Website scroll teardown:** record with Playwright at 1080×1920 (`recordVideo`), cut to 3–4s beats, then run it through `finish_video.py`.
- **Before/after:** two screenshots with a wipe or split. Build the frames, encode with ffmpeg, then finish.
- **Carousel:** `scripts/render_carousel.mjs` (see SKILL.md section 4).
