"""Render slides + edge-tts narration into one MP4 (with chapters and transcript).

Usage: python build_video.py <out_dir>
"""
import asyncio
import subprocess
import sys
import textwrap
from pathlib import Path

import edge_tts
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from slides_content import SLIDES

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
VOICE, RATE = "en-US-AriaNeural", "+8%"
W, H = 1920, 1080
F = "C:/Windows/Fonts/"
TITLE = ImageFont.truetype(F + "segoeuib.ttf", 50)
BODY = ImageFont.truetype(F + "segoeui.ttf", 31)
SMALL = ImageFont.truetype(F + "segoeui.ttf", 24)
CODE = ImageFont.truetype(F + "consola.ttf", 25)
COLORS = {"Intro": (52, 73, 94), "Assignment 2": (31, 97, 141), "Assignment 3": (120, 66, 18),
          "Viva drill": (30, 110, 70)}


def fit(img, box_w, box_h):
    im = Image.open(img).convert("RGB")
    im.thumbnail((box_w, box_h), Image.LANCZOS)
    return im


def render(i, s):
    img = Image.new("RGB", (W, H), (250, 250, 247))
    d = ImageDraw.Draw(img)
    col = COLORS[s["section"]]
    d.rectangle([0, 0, W, 120], fill=col)
    d.text((50, 30), s["title"], font=TITLE, fill="white")
    d.text((W - 470, H - 40), f"{s['section']} · slide {i + 1}/{len(SLIDES)}", font=SMALL, fill=(120, 120, 120))
    imgs = [s[k] for k in ("image", "image2") if s.get(k)]
    text_w = 1060 if imgs else 1800
    wrap = 62 if imgs else 105
    y = 160
    if s.get("code"):
        lines = s["code"]
        box_h = 34 * len(lines) + 30
        d.rounded_rectangle([40, y - 10, 40 + text_w + 20, y + box_h], 12, fill=(36, 39, 46))
        for ln in lines:
            d.text((60, y + 5), ln[:wrap + 18], font=CODE, fill=(220, 230, 240))
            y += 34
        y += 45
    for b in s["bullets"]:
        sub = b.startswith("  ")
        parts = textwrap.wrap(b.strip(), wrap - (4 if sub else 0)) or [""]
        x = 90 if sub else 55
        if not sub:
            d.ellipse([x, y + 14, x + 12, y + 26], fill=col)
        for k, part in enumerate(parts):
            d.text((x + 28, y), part, font=BODY, fill=(35, 35, 35))
            y += 42
        y += 8
    if imgs:
        n = len(imgs)
        box_h = (H - 200) // n - 10
        yy = 150
        for p in imgs:
            im = fit(p, 780, box_h)
            img.paste(im, (W - 40 - im.width, yy))
            yy += im.height + 15
    path = OUT / f"slide_{i:02d}.png"
    img.save(path)
    return path


async def tts(text, path):
    await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(path))


def duration(path):
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "Duration:" in line:
            h, m, sec = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(sec)
    raise RuntimeError(path)


async def main():
    segs, chapters, transcript, t = [], [], [], 0.0
    last_section = None
    for i, s in enumerate(SLIDES):
        png = render(i, s)
        mp3 = OUT / f"audio_{i:02d}.mp3"
        if not mp3.exists():
            await tts(s["narration"], mp3)
        seg = OUT / f"seg_{i:02d}.mp4"
        subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-framerate", "2", "-i", str(png),
                        "-i", str(mp3), "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                        "-r", "2", "-c:a", "aac", "-b:a", "128k", "-af", "apad=pad_dur=0.8",
                        "-shortest", str(seg)], check=True)
        dur = duration(seg)
        if s["section"] != last_section:
            chapters.append((t, s["section"]))
            last_section = s["section"]
        mm, ss = divmod(int(t), 60)
        transcript.append(f"[{mm:02d}:{ss:02d}] {s['title']}\n{s['narration']}\n")
        print(f"{i + 1:2d}/{len(SLIDES)} {dur:6.1f}s  {s['title']}")
        segs.append(seg)
        t += dur
    lst = OUT / "concat.txt"
    lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs))
    final = OUT / "GenAI_A2_A3_Viva_Walkthrough.mp4"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(final)], check=True)
    (OUT / "transcript.txt").write_text("\n".join(transcript), encoding="utf-8")
    with open(OUT / "chapters.txt", "w", encoding="utf-8") as f:
        f.write(f"Total {int(t // 60)} min {int(t % 60)} s\n")
        for start, name in chapters:
            f.write(f"{int(start // 60):02d}:{int(start % 60):02d}  {name}\n")
        for i, s in enumerate(SLIDES):
            pass
    print("TOTAL", round(t / 60, 1), "min ->", final)


asyncio.run(main())
