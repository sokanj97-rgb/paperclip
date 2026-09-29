#!/usr/bin/env python3
"""Finish a raw short-form clip into a publish-ready 9:16 post.

Takes a raw video (AI-generated, screen recording, or filmed) plus a captions
JSON file and produces:
  - final.mp4   1080x1920, 30fps, H.264/AAC, captions burned in, loudness
                normalized to -14 LUFS, faststart
  - cover.jpg   a chosen frame with the hook caption on top
  - finish-report.json   detected cuts, snapped caption times, font sizes

Captions are rendered as white "pill" overlays (Pillow), placed below the top
UI safe zone, and their start/end times are snapped to real scene cuts.

Requirements: python3 + Pillow, ffmpeg on PATH (or FFMPEG=/path/to/ffmpeg).
Font: "font" in captions.json or BRAND_FONT=/path.ttf; defaults to Montserrat
ExtraBold, downloaded once to ~/.cache/social-studio/fonts/.

Usage:
  python3 finish_video.py raw.mp4 captions.json out_dir/

captions.json:
{
  "top": 300,                      # optional, px from top (keep >= 260)
  "cover_at": 8.6,                 # optional, seconds; default = middle
  "cover_segment": 0,              # optional, which caption goes on the cover
  "segments": [
    {"start": 0, "end": 3, "lines": [
      {"text": "Logging lunch", "size": 84},
      {"text": "took me 3 seconds", "size": 84}
    ]},
    {"start": 3, "end": 7, "lines": [
      {"text": "Protein goal:", "size": 72},
      {"text": "hit by lunch", "size": 72, "color": "accent"}
    ]}
  ]
}
Colors: "ink" (default), "accent", or "#RRGGBB". Break lines by hand into
natural phrases; the script shrinks a line's font if it exceeds the safe width
but never re-wraps (auto-wrap leaves orphan words).
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
MAX_TEXT_W = 860          # keeps text clear of the right-side UI buttons
MIN_TOP = 260             # top UI safe zone
SNAP_WINDOW = 0.6         # seconds; caption edges within this of a cut snap to it
COLORS = {"ink": (17, 17, 17), "accent": (22, 140, 64)}
# Montserrat ExtraBold (SIL Open Font License), pinned to a commit and cached on first use.
FONT_URL = ("https://raw.githubusercontent.com/JulietaUla/Montserrat/"
            "555facfb2a18c72c3c0380f0d9c0f060453a9058/fonts/ttf/Montserrat-ExtraBold.ttf")
FONT_CACHE = os.path.join(os.path.expanduser("~"), ".cache", "social-studio", "fonts", "Montserrat-ExtraBold.ttf")
FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def resolve_font(spec_font):
    """Brand font from the spec or BRAND_FONT, else the cached Montserrat (downloaded once)."""
    for candidate in (spec_font, os.environ.get("BRAND_FONT")):
        if candidate:
            if not os.path.isfile(candidate):
                sys.exit(f"Font not found: {candidate}")
            return candidate
    if not os.path.isfile(FONT_CACHE):
        os.makedirs(os.path.dirname(FONT_CACHE), exist_ok=True)
        tmp = FONT_CACHE + ".part"
        urllib.request.urlretrieve(FONT_URL, tmp)
        ImageFont.truetype(tmp, 20)  # raises if the download is not a valid font
        os.replace(tmp, FONT_CACHE)
    return FONT_CACHE


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def probe(path):
    err = run([FFMPEG, "-hide_banner", "-i", path]).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    if not m:
        sys.exit(f"Could not read duration of {path}")
    duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return duration, "Audio:" in err


def detect_cuts(path, threshold=0.25):
    err = run([FFMPEG, "-hide_banner", "-i", path, "-vf",
               f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"]).stderr
    return [round(float(t), 3) for t in re.findall(r"pts_time:([\d.]+)", err)]


def snap(t, cuts):
    best = min(cuts, key=lambda c: abs(c - t), default=None)
    return best if best is not None and abs(best - t) <= SNAP_WINDOW else t


def color(value):
    if not value:
        return COLORS["ink"]
    if value in COLORS:
        return COLORS[value]
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def render_overlay(lines, top, font_path, out_png):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y, used = max(top, MIN_TOP), []
    for line in lines:
        text, size = line["text"], int(line.get("size", 72))
        font = ImageFont.truetype(font_path, size)
        while draw.textlength(text, font=font) > MAX_TEXT_W and size > 24:
            size -= 2
            font = ImageFont.truetype(font_path, size)
        tw = draw.textlength(text, font=font)
        ascent, descent = font.getmetrics()
        h, px, py = ascent + descent, 32, 12
        x0 = (W - tw) / 2 - px
        draw.rounded_rectangle([x0, y, x0 + tw + 2 * px, y + h + 2 * py], radius=24,
                               fill=(255, 255, 255, 246))
        draw.text(((W - tw) / 2, y + py), text, font=font, fill=color(line.get("color")))
        used.append({"text": text, "size": size, "width": int(tw)})
        y += h + 2 * py + 8
    img.save(out_png)
    return used


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    raw, spec_path, out_dir = sys.argv[1:]
    os.makedirs(out_dir, exist_ok=True)
    spec = json.load(open(spec_path))
    font_path = resolve_font(spec.get("font"))
    duration, has_audio = probe(raw)
    cuts = detect_cuts(raw)

    segments, overlays = [], []
    for i, seg in enumerate(spec["segments"]):
        start = 0.0 if seg["start"] <= 0 else snap(float(seg["start"]), cuts)
        end = duration if seg["end"] >= duration - 0.05 else snap(float(seg["end"]), cuts)
        png = os.path.join(out_dir, f"caption_{i}.png")
        used = render_overlay(seg["lines"], spec.get("top", 300), font_path, png)
        segments.append({"start": round(start, 3), "end": round(end, 3), "lines": used})
        overlays.append(png)

    chain, last = ["[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[v0]"], "v0"
    for i, seg in enumerate(segments):
        nxt = f"v{i + 1}"
        chain.append(f"[{last}][{i + 1}:v]overlay=0:0:enable='between(t,{seg['start']},{seg['end']})'[{nxt}]")
        last = nxt

    final = os.path.join(out_dir, "final.mp4")
    cmd = [FFMPEG, "-v", "error", "-y", "-i", raw]
    for png in overlays:
        cmd += ["-i", png]
    cmd += ["-filter_complex", ";".join(chain), "-map", f"[{last}]"]
    if has_audio:
        cmd += ["-map", "0:a", "-c:a", "aac", "-b:a", "160k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11"]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-r", "30", "-movflags", "+faststart", final]
    result = run(cmd)
    if result.returncode != 0:
        sys.exit(f"ffmpeg failed:\n{result.stderr}")

    cover_at = float(spec.get("cover_at", duration / 2))
    cover_png = overlays[int(spec.get("cover_segment", 0))]
    cover = os.path.join(out_dir, "cover.jpg")
    result = run([FFMPEG, "-v", "error", "-y", "-ss", str(cover_at), "-i", raw, "-i", cover_png,
                  "-filter_complex",
                  "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[b];[b][1:v]overlay=0:0",
                  "-frames:v", "1", "-q:v", "2", cover])
    if result.returncode != 0:
        sys.exit(f"cover render failed:\n{result.stderr}")

    report = {"input": raw, "duration": round(duration, 3), "has_audio": has_audio,
              "cuts": cuts, "segments": segments, "outputs": [final, cover]}
    json.dump(report, open(os.path.join(out_dir, "finish-report.json"), "w"), indent=2)
    print(json.dumps(report, indent=2))
    if not has_audio:
        print("WARNING: no audio track; add music or voiceover before publishing.", file=sys.stderr)


if __name__ == "__main__":
    main()
