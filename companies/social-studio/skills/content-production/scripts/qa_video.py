#!/usr/bin/env python3
"""Automated craft checks for a finished short-form video.

Checks the file against the team's craft floor (the reference test post):
  - 1080x1920, ~30fps, H.264 video
  - duration within the brief's range (default 5-60s)
  - audio track present, integrated loudness -14 LUFS +/- 1.5
  - no single shot longer than --max-shot seconds (default 5) -> visual change
    at least every few seconds
Also writes qa-sheet.jpg: a contact sheet of the opening frame plus the middle
of every shot, for the mandatory visual check (hands, faces, screens, text).

Requirements: ffmpeg on PATH (or FFMPEG=/path/to/ffmpeg), python3.

Usage:
  python3 qa_video.py final.mp4 [--min 5] [--max 60] [--max-shot 5] [--out qa/]
Exit code 0 = PASS, 1 = FAIL. Attach qa-report.json and qa-sheet.jpg to the issue.
"""
import argparse
import json
import os
import re
import subprocess
import sys

FFMPEG = os.environ.get("FFMPEG", "ffmpeg")


def stderr_of(args):
    return subprocess.run(args, capture_output=True, text=True).stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--min", type=float, default=5)
    ap.add_argument("--max", type=float, default=60)
    ap.add_argument("--max-shot", type=float, default=5)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.dirname(os.path.abspath(a.video))
    os.makedirs(out, exist_ok=True)

    info = stderr_of([FFMPEG, "-hide_banner", "-i", a.video])
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info)
    duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)) if m else 0
    v = re.search(r"Video: (\w+).*?, (\d+)x(\d+).*?, ([\d.]+) fps", info)
    codec, width, height, fps = (v.group(1), int(v.group(2)), int(v.group(3)), float(v.group(4))) if v else (None, 0, 0, 0)
    has_audio = "Audio:" in info

    loudness = None
    if has_audio:
        lm = re.findall(r"I:\s+(-?[\d.]+) LUFS", stderr_of(
            [FFMPEG, "-hide_banner", "-i", a.video, "-af", "ebur128", "-vn", "-f", "null", "-"]))
        loudness = float(lm[-1]) if lm else None

    cuts = [round(float(t), 3) for t in re.findall(r"pts_time:([\d.]+)", stderr_of(
        [FFMPEG, "-hide_banner", "-i", a.video, "-vf", "select='gt(scene,0.25)',showinfo", "-an", "-f", "null", "-"]))]
    bounds = [0.0] + cuts + [duration]
    shots = [round(bounds[i + 1] - bounds[i], 2) for i in range(len(bounds) - 1)]

    checks = {
        "resolution_1080x1920": (width, height) == (1080, 1920),
        "fps_about_30": abs(fps - 30) < 1,
        "codec_h264": codec == "h264",
        "duration_in_range": a.min <= duration <= a.max,
        "audio_present": has_audio,
        "loudness_-14_lufs": loudness is not None and abs(loudness + 14) <= 1.5,
        "visual_change_every_few_seconds": max(shots) <= a.max_shot if shots else False,
    }

    sample_times = [0.5] + [round((bounds[i] + bounds[i + 1]) / 2, 2) for i in range(len(bounds) - 1)]
    frames = []
    for i, t in enumerate(sample_times):
        f = os.path.join(out, f"qa_frame_{i}.png")
        subprocess.run([FFMPEG, "-v", "error", "-y", "-ss", str(t), "-i", a.video, "-frames:v", "1",
                        "-vf", "scale=360:-1", f])
        frames.append(f)
    sheet = os.path.join(out, "qa-sheet.jpg")
    inputs = sum([["-i", f] for f in frames], [])
    n = len(frames)
    layout = "|".join(f"{'+'.join(['w0'] * i) or '0'}_0" for i in range(n))
    subprocess.run([FFMPEG, "-v", "error", "-y", *inputs, "-filter_complex",
                    f"{''.join(f'[{i}]' for i in range(n))}xstack=inputs={n}:layout={layout}" if n > 1 else "null",
                    "-q:v", "3", sheet])

    report = {
        "video": a.video, "duration": round(duration, 2), "resolution": f"{width}x{height}",
        "fps": fps, "codec": codec, "loudness_lufs": loudness, "cuts": cuts, "shot_lengths": shots,
        "checks": checks, "result": "PASS" if all(checks.values()) else "FAIL",
        "qa_sheet": sheet, "sampled_at": sample_times,
        "manual_review_required": "Open qa-sheet.jpg and check hands, faces, phone screens and any "
                                  "text for AI artifacts before hand-off.",
    }
    json.dump(report, open(os.path.join(out, "qa-report.json"), "w"), indent=2)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
