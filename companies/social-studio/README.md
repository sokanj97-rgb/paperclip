# Social Studio

A two-agent social media team for a **web design, web hosting and copywriting** business, running **Instagram and TikTok** with about 10 minutes of owner time per week.

The team studies top-performing content, turns what it learns into posts, checks each one against a strict quality bar, publishes what you approve, and gets better every week from its own results.

## How it works

```
        ┌────────────── Study top content (swipe file) ◄──────────────┐
        ▼                                                             │
  Plan + brief ──► Produce ──► Quality gate ──► You approve ──► Publish + engage
  (Mon, CD)       (Tue, SMM)   (Thu, CD)       (1 packet/wk)   (3x daily, SMM)
                                                                      │
        ▲                                                             ▼
        └──────── Update playbook ◄──── Score vs. baseline (Sun, CD) ◄┘
```

- **Research → hypotheses.** The Creative Director finds *outlier* posts (posts that beat their own account's median by 2–3× or more) across niche, audience-adjacent and craft accounts. Each one is torn down into a reusable pattern in the `swipe-file`.
- **Results → rules.** Every post carries a hypothesis tag (hook type, format, pillar). Weekly scoring against our own baseline promotes patterns that win 2 of 3 tries into playbook **rules** and retires those that don't.
- **70/20/10.** 70% of posts use proven rules, 20% iterate on winners, 10% are experiments.
- **Leads first.** Posts are scored on leads, then follows, then shares and saves, then views.

## Org chart

| Agent | Title | Reports to | Skills |
| --- | --- | --- | --- |
| `creative-director` | Creative Director & Head of Social | — (you, the board) | content-research, quality-gate, performance-learning |
| `social-media-manager` | Social Media Manager & Content Producer | creative-director | content-production, social-publishing, performance-learning |

**Creative Director:** owns brand, strategy, research, briefs, the quality gate, the weekly approval packet and the learning playbook.

**Social Media Manager:** produces finished posts (videos, carousels, captions, covers), publishes approved content, replies to comments, routes leads to you and logs metrics.

## What you (the owner) do

1. **Once:** answer the brand intake questionnaire (pre-filled; just correct it) and, optionally, connect Instagram and TikTok API access.
2. **Weekly, about 10 minutes:** review one approval packet and reply "approve all" or list the posts to cut or change.
3. **Optional:** film a few talking-head clips from ready scripts (about 15–20 minutes, batched), and drop links to posts you like into the Content OS issue.
4. **As they come:** take leads the team routes to you.

Nothing is published without your approved packet.

## Routines

All times are in `America/New_York`. To change them, edit `.paperclip.yaml` before importing, or edit the routines in Paperclip afterwards.

| Routine | When | Agent |
| --- | --- | --- |
| Weekly strategy sprint | Mon 07:05 | Creative Director |
| Weekly production | Tue 07:10 | Social Media Manager |
| Quality gate + approval packet | Thu 07:10 | Creative Director |
| Publish, engage, log metrics | Daily 08:55 / 11:55 / 17:55 | Social Media Manager |
| Performance review + playbook | Sun 18:05 | Creative Director |
| Monthly deep study | 1st of month 06:05 | Creative Director |

Starter tasks: **Brand intake and Content OS setup**, **Content OS baseline** (first 30+ teardowns, playbook v0, 4-week calendar) and **Channel setup** (access, profile audit, community guide).

## Runs on your Claude subscription

Both agents use the `claude_local` adapter (Claude Code CLI). With no API key set, Paperclip bills their runs to your Claude Pro/Max subscription instead of API credits.

| Agent | Model | Why |
| --- | --- | --- |
| Creative Director | `opus` | Research, judgment and the quality gate; runs about 4× a week |
| Social Media Manager | `sonnet` | Production, publishing and replies; runs 3× a day, so a lighter model saves your usage limits |

`opus` and `sonnet` are Claude CLI aliases that always point to the latest model your plan includes.

Setup, on the machine that runs Paperclip:

1. Install Claude Code and run `claude login` with your Claude subscription account.
2. Make sure `ANTHROPIC_API_KEY` is **not** set in the environment Paperclip starts from, and not in the agents' env in Paperclip. If it's set, it takes priority and runs bill as API usage. Paperclip passes the server's environment through to the agents.
3. After importing, the agent's page in Paperclip should show "Claude is logged in via claude.ai" with your plan's usage windows.

Agent runs count toward your plan's usage limits. If you hit them, runs pause until the window resets. Scheduled routines coalesce, so nothing piles up.

Your Claude subscription does not pay for video/image generation (e.g. Higgsfield credits) or other paid APIs.

## Production requirements (for test-post quality)

The Social Media Manager makes every video and carousel with the scripts in `skills/content-production/scripts/`. They encode the craft floor set by the reference post in `references/test-post-food-tracker/`, and the Creative Director's quality gate rejects anything that skipped them. Install these on the machine that runs Paperclip:

| Requirement | Why | Check |
| --- | --- | --- |
| **ffmpeg** (with libx264) | Captions, 1080×1920 export, -14 LUFS loudness, cut detection, QA | `ffmpeg -version` |
| **Python 3 + Pillow** | Caption overlays, QA reports | `python3 -c "import PIL"` |
| **Node 18+ + Playwright Chromium** | Carousels, website scroll recordings | `npx playwright install chromium` |
| **Higgsfield MCP server** in Claude Code (user scope) | AI video generation (Kling 3.0 by default, about 30 credits per 15s clip) | `claude mcp list` shows higgsfield |

To add Higgsfield: run `claude mcp add --scope user --transport http higgsfield <server URL from Higgsfield's MCP docs>`, then open `claude` once and run `/mcp` to sign in. Agents run headless and can't complete a sign-in themselves. Generation spends **Higgsfield credits**, not your Claude subscription. The default budget is 150 credits/week with a 60-credit cap per post; change it in the brand book.

Without Higgsfield the team still ships, using no-AI formats: website scroll teardowns, before/afters and carousels. The **Channel Setup** task runs a toolchain check and a smoke test on day one and sends you one install checklist for anything missing.

## Integrations (all optional)

| Env input | Used for |
| --- | --- |
| `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID` | Publishing, insights and studying other business accounts via Business Discovery |
| `TIKTOK_ACCESS_TOKEN` | Publishing and video metrics. Posts stay private until TikTok audits your developer app. |

Without these, the team runs in **manual hand-off** mode: at each slot you get a ready-to-post comment (asset, caption, checklist) that takes under 2 minutes. Web research and asset creation work best with an agent runtime that has web search/fetch, a headless browser (Playwright) and ffmpeg.

## Getting started

```sh
paperclipai company import ./companies/social-studio
```

Then open the **Brand intake** task and answer the Creative Director's questionnaire.

## Guardrails built in

No copying of other creators' content, invented results, testimonials or client work, bought engagement, or unapproved posts. Leads, complaints, pricing and anything legal go to you.

## References

- [Agent Companies specification](https://agentcompanies.io/specification)
- [Paperclip](https://github.com/paperclipai/paperclip)
