# Local setup brief: Social Studio on this machine

**For:** Claude Code running on the owner's computer.
**How to use:** open Claude Code in any folder and say: *"Read `companies/social-studio/LOCAL-SETUP.md` from github.com/sokanj97-rgb/paperclip (branch `claude/nifty-pasteur-3tqprs`) and carry it out."* If the repo is already cloned, point it at the local file instead.

---

## Your job

Set up this machine so the **Social Studio** agent team (Creative Director + Social Media Manager) runs in Paperclip on the owner's **Claude subscription** and produces videos and carousels at the reference-post quality. Install what's missing, verify each step with the listed check, and finish with the report in section 9.

## Ground rules

- **Never set `ANTHROPIC_API_KEY`**, and remove it if you find it (section 3). If it's set, agent runs bill as API usage instead of the subscription.
- **Stop and ask the owner** at each 🙋 step. Those need a browser sign-in or a decision only they can make. Tell them exactly what to click or type, then wait.
- Don't publish anything to Instagram/TikTok, spend Higgsfield credits beyond the check in section 4, or commit secrets.
- Don't run Paperclip as root/Administrator: its embedded Postgres refuses to start as root.
- **Windows:** do everything inside **WSL2 (Ubuntu)**. The scripts and embedded database expect a POSIX shell. If WSL isn't installed, 🙋 ask the owner to run `wsl --install` in an admin PowerShell and reboot.
- Prefer the OS package manager: Homebrew on macOS, apt on Ubuntu/WSL. Skip anything already installed at a good version.

## 1. Inventory (report before installing)

Run these and show the owner a table of found / missing / version:

```bash
uname -a; git --version; node --version; pnpm --version; claude --version
ffmpeg -hide_banner -version | head -1
ffmpeg -hide_banner -encoders 2>/dev/null | grep -c libx264
ffmpeg -hide_banner -filters 2>/dev/null | grep -cE " (loudnorm|ebur128) "
python3 --version; python3 -c "import PIL; print('Pillow', PIL.__version__)"
npm root -g; ls "$(npm root -g)" | grep -x playwright
claude mcp list
env | grep -i ANTHROPIC_API_KEY
```

## 2. Install dependencies

| Dependency | Version | macOS | Ubuntu / WSL2 | Check |
| --- | --- | --- | --- | --- |
| Git | any recent | `brew install git` | `sudo apt install -y git` | `git --version` |
| Node.js | **≥ 20** (22 LTS recommended) | `brew install node@22` | NodeSource 22.x or `nvm install 22` | `node --version` |
| pnpm | **9.15.4** (repo pins it) | `corepack enable && corepack prepare pnpm@9.15.4 --activate` | same | `pnpm --version` |
| Claude Code CLI | latest | native installer from code.claude.com/docs (skip if `claude` works) | same | `claude --version` |
| ffmpeg | with **libx264**, **loudnorm**, **ebur128** | `brew install ffmpeg` | `sudo apt install -y ffmpeg` | both inventory greps print ≥ 1 |
| Python 3 + Pillow | Python ≥ 3.9 | `brew install pillow` (Homebrew Python) | `sudo apt install -y python3 python3-pil` | `python3 -c "import PIL"` |
| Playwright + Chromium | latest | `npm i -g playwright && npx playwright install chromium` | `npm i -g playwright && npx playwright install --with-deps chromium` | `ls "$(npm root -g)/playwright"` |

Notes:
- Pillow must import in the **same `python3` the agents will run**, i.e. the first `python3` on PATH. If pip says "externally-managed-environment", use the OS package above rather than `--break-system-packages`.
- Playwright must be installed **globally**. The carousel script falls back to `npm root -g` because Paperclip runs it from a folder with no `node_modules`.
- The video and carousel scripts download the Montserrat font once to `~/.cache/social-studio/fonts/` (from raw.githubusercontent.com). Make sure that host isn't blocked.

## 3. Claude subscription (not API)

1. Find and remove any `ANTHROPIC_API_KEY`: check `env`, `~/.zshrc`, `~/.bashrc`, `~/.profile`, `~/.zprofile`, and any `.env` in the Paperclip folder. 🙋 Show the owner each line before deleting it.
2. Confirm Claude Code is signed in to the subscription: `claude -p "reply with the single word ok"`. If it asks for login, 🙋 have the owner run `claude`, type `/login` and pick their Claude.ai (Pro/Max) account.
3. Recommend **Max**: the team runs about 25 agent sessions a week, which can hit Pro's limits.

## 4. Higgsfield (AI video)

1. Add the MCP server at user scope so Paperclip's headless agents inherit it:
   ```bash
   claude mcp add --scope user --transport http higgsfield https://mcp.higgsfield.ai/mcp
   ```
   Confirm this URL on Higgsfield's help page ("How to connect Higgsfield to Claude"). If it differs, use theirs.
2. 🙋 The owner runs `claude`, types `/mcp`, selects **higgsfield**, and completes the browser sign-in. Agents can't do this themselves.
3. Verify (free call):
   ```bash
   claude -p "Call the Higgsfield balance tool and report credits and plan." --allowedTools "mcp__higgsfield__balance"
   ```
   Report the plan and credits. Starter works; draft mode needs Plus or higher. The team's default budget is 150 credits/week.
4. If Higgsfield isn't wanted, skip this section. The team falls back to no-AI formats (website teardowns, before/after, carousels).

## 5. Get Paperclip (the fork, with the Social Studio package)

```bash
git clone https://github.com/sokanj97-rgb/paperclip.git ~/paperclip   # 🙋 if private, owner signs in: `gh auth login` or SSH
cd ~/paperclip && git checkout claude/nifty-pasteur-3tqprs
pnpm install
```

Use this fork, not upstream `npx paperclipai`. The fork's CLI keeps skill scripts on import, and the package lives here.

## 6. Production toolchain smoke test (before importing)

Run in a scratch folder. **Every step must pass.**

```bash
S=~/paperclip/companies/social-studio/skills/content-production/scripts
mkdir -p ~/social-studio-smoke && cd ~/social-studio-smoke
ffmpeg -v error -y -f lavfi -i testsrc2=s=720x1280:d=6 -f lavfi -i sine=d=6 -shortest -pix_fmt yuv420p raw.mp4
echo '{"segments":[{"start":0,"end":6,"lines":[{"text":"Smoke test","size":84}]}]}' > captions.json
python3 $S/finish_video.py raw.mp4 captions.json out/
python3 $S/qa_video.py out/final.mp4 --max-shot 10 --out out/qa/        # must print "result": "PASS"
cat > slides.json <<'EOF'
{"brand":{"handle":"@test"},"slides":[{"kind":"hook","title":"Smoke *test*"},{"kind":"cta","title":"Done"}]}
EOF
node $S/render_carousel.mjs slides.json slides/                           # must write slide_01.png, slide_02.png
```

Open `out/cover.jpg`, `out/qa/qa-sheet.jpg` and `slides/slide_01.png`, and confirm the captions use the bold Montserrat font in white pills and the slide shows the heading. Fix anything that fails before continuing.

## 7. Start Paperclip and import the team

1. Start it and leave it running (a separate terminal or background):
   ```bash
   cd ~/paperclip && pnpm dev
   ```
   It auto-onboards on first run. The first start can take 30–60s. Check `curl -s http://localhost:3100/api/health`. If port 3100 is taken, use the port it prints.
2. 🙋 Confirm with the owner before importing. Once imported, the agents start their starter tasks (brand intake questionnaire, research baseline, channel setup) and the weekly routines go live (America/New_York).
3. Import with the fork's CLI:
   ```bash
   cd ~/paperclip && pnpm paperclipai company import ./companies/social-studio --dry-run   # review the preview
   pnpm paperclipai company import ./companies/social-studio --yes
   ```
   Use `pnpm paperclipai company import --help` if it asks for an API base or target.
4. Verify in the board UI (`http://localhost:3100`):
   - 2 agents, both **Claude Code (local)**: Creative Director on `opus`, Social Media Manager on `sonnet`
   - Each agent's page shows **"Claude is logged in via claude.ai"** (the subscription is working). If it says API key, go back to section 3.
   - 6 routines, 3 starter tasks, and the 5 Social Studio skills (plus Paperclip's built-in ones). The **content-production** skill's files include `scripts/finish_video.py`, `scripts/qa_video.py`, `scripts/render_carousel.mjs` and `references/ai-video-recipe.md`.

## 8. Optional: Instagram / TikTok access

Not required: without it the team uses manual hand-off (you tap post). If the owner wants API publishing, the Social Media Manager's **Channel Setup** task walks them through it and adds `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_BUSINESS_ACCOUNT_ID` and `TIKTOK_ACCESS_TOKEN` as company secrets. Never paste tokens into files or chat logs.

## 9. Final report to the owner

Reply with:

1. A dependency table (name, version, how installed).
2. A pass/fail line for each of: subscription sign-in, `ANTHROPIC_API_KEY` absent, Higgsfield connected + credits, smoke test (video QA PASS + carousel rendered), Paperclip running (URL), import (agents/routines/tasks/skills counts), agents showing claude.ai sign-in.
3. Anything skipped or still needing the owner, as a short checklist.
4. The next step: *"Open the Brand intake task in Paperclip and answer the Creative Director's questionnaire."*
