#!/usr/bin/env node
// Render an Instagram carousel (also usable as TikTok photo mode) from a JSON spec.
// Each slide is laid out in HTML/CSS with the brand font (Montserrat by default) and
// screenshotted in headless Chromium at exactly 1080x1350 (4:5).
//
// Requirements: Node 18+ and Playwright with Chromium
//   npm i -g playwright && npx playwright install chromium   (or a local install)
//
// Usage: node render_carousel.mjs slides.json out_dir/
//   (optional) CHROMIUM_PATH=/path/to/chrome to use an existing browser
//
// slides.json:
// {
//   "brand": { "bg": "#FFFFFF", "ink": "#111111", "accent": "#168C40", "handle": "@yourbrand" },
//   "slides": [
//     { "kind": "hook",    "title": "3 copy mistakes killing your contact form", "body": "Swipe →" },
//     { "kind": "point",   "title": "1. Your button says \"Submit\"", "body": "Say what they get: \"Get my free quote\"", "image": "optional/path.png" },
//     { "kind": "summary", "title": "Quick checklist", "items": ["Specific button", "3 fields max", "Say when you'll reply"] },
//     { "kind": "cta",     "title": "Want us to check yours?", "body": "Comment AUDIT and we'll send a free teardown" }
//   ]
// }
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";

// Montserrat ExtraBold (SIL Open Font License), pinned to a commit and cached on
// first use. BRAND_FONT=/path/to/font.ttf overrides it with the brand's own font.
const FONT_URL =
  "https://raw.githubusercontent.com/JulietaUla/Montserrat/555facfb2a18c72c3c0380f0d9c0f060453a9058/fonts/ttf/Montserrat-ExtraBold.ttf";
const fontCache = path.join(os.homedir(), ".cache", "social-studio", "fonts", "Montserrat-ExtraBold.ttf");
async function loadFontBytes() {
  if (process.env.BRAND_FONT) return fs.readFileSync(process.env.BRAND_FONT);
  if (!fs.existsSync(fontCache)) {
    const res = await fetch(FONT_URL);
    if (!res.ok) throw new Error(`Font download failed: HTTP ${res.status}`);
    fs.mkdirSync(path.dirname(fontCache), { recursive: true });
    fs.writeFileSync(fontCache, Buffer.from(await res.arrayBuffer()));
  }
  return fs.readFileSync(fontCache);
}
// Embedded as a data URL: pages loaded via setContent cannot fetch file:// fonts.
const fontUrl = `data:font/ttf;base64,${(await loadFontBytes()).toString("base64")}`;

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  console.error("Playwright is not installed. Run: npm i -g playwright && npx playwright install chromium");
  process.exit(2);
}

const [specPath, outDir] = process.argv.slice(2);
if (!specPath || !outDir) {
  console.error("Usage: node render_carousel.mjs slides.json out_dir/");
  process.exit(2);
}
const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
const brand = { bg: "#FFFFFF", ink: "#111111", accent: "#168C40", handle: "", ...spec.brand };
fs.mkdirSync(outDir, { recursive: true });

const esc = (s = "") => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

function slideHtml(slide, index, total) {
  const img = slide.image
    ? `<img class="shot" src="${pathToFileURL(path.resolve(path.dirname(specPath), slide.image)).href}">`
    : "";
  const items = (slide.items || []).map((i) => `<li>${esc(i)}</li>`).join("");
  const isHook = slide.kind === "hook";
  const isCta = slide.kind === "cta";
  return `<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face { font-family: Brand; src: url("${fontUrl}"); font-weight: 800; }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 1080px; height: 1350px; }
  body { font-family: Brand, system-ui, sans-serif; background: ${isCta ? brand.ink : brand.bg};
         color: ${isCta ? brand.bg : brand.ink}; padding: 96px 88px; display: flex; flex-direction: column; }
  .count { font-size: 30px; letter-spacing: 2px; opacity: .55; }
  .main { flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 44px; }
  h1 { font-size: ${isHook ? 104 : 76}px; line-height: 1.08; letter-spacing: -1.5px; }
  h1 em { font-style: normal; color: ${brand.accent}; }
  p { font-size: 44px; line-height: 1.3; opacity: .85; }
  ul { list-style: none; display: flex; flex-direction: column; gap: 26px; }
  li { font-size: 46px; padding-left: 64px; position: relative; }
  li::before { content: "✓"; position: absolute; left: 0; color: ${brand.accent}; }
  .shot { width: 100%; max-height: 560px; object-fit: cover; border-radius: 28px; }
  .foot { display: flex; justify-content: space-between; font-size: 30px; opacity: .6; }
  .swipe { color: ${brand.accent}; opacity: 1; }
  </style></head><body>
  <div class="count">${index + 1}/${total}</div>
  <div class="main">
    <h1>${esc(slide.title).replace(/\*(.+?)\*/g, "<em>$1</em>")}</h1>
    ${img}
    ${slide.body ? `<p>${esc(slide.body)}</p>` : ""}
    ${items ? `<ul>${items}</ul>` : ""}
  </div>
  <div class="foot"><span>${esc(brand.handle)}</span>${index < total - 1 ? '<span class="swipe">Swipe →</span>' : ""}</div>
  </body></html>`;
}

// CHROMIUM_PATH lets you point at an existing Chrome/Chromium instead of Playwright's download.
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
const files = [];
for (const [i, slide] of spec.slides.entries()) {
  await page.setContent(slideHtml(slide, i, spec.slides.length), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  if (!(await page.evaluate(() => document.fonts.check('800 40px Brand')))) {
    console.error("Brand font failed to load; refusing to render with a fallback font.");
    process.exit(1);
  }
  // Fail loudly if any text overflows the slide instead of silently clipping it.
  const overflow = await page.evaluate(() => document.body.scrollHeight > 1350 || document.body.scrollWidth > 1080);
  if (overflow) {
    console.error(`Slide ${i + 1} overflows 1080x1350 — shorten the copy.`);
    process.exitCode = 1;
  }
  const file = path.join(outDir, `slide_${String(i + 1).padStart(2, "0")}.png`);
  await page.screenshot({ path: file });
  files.push(file);
}
await browser.close();
console.log(JSON.stringify({ slides: files }, null, 2));
