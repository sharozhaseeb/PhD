"""Slow walkthrough video: handout (highlighted) -> code -> results, with natural TTS.

Usage: python build_video2.py slides_a2.py out_dir "Video title"
       add --check to only render slides (no audio / video), to verify every handout phrase and code start.
"""
import asyncio
import re
import runpy
import subprocess
import sys
from pathlib import Path

import edge_tts
import fitz
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

HERE = Path(__file__).parent
G = Path(r"C:/Users/pc/study/PhD/courses/first sem/genai")
PREFIX = {"DG/": HERE / "diagrams", "A2F/": G / "assignment-2/colab_run/outputs/figures",
          "A3F/": G / "assignment-3/output/Group3_Assignment3/figures"}
SRC = {"A2NB": HERE / "ref/A2_notebook_cells.txt",
       "A3NB": HERE / "ref/A3_notebook_cells.txt",
       "A3SRC": G / "assignment-3/output/Group3_Assignment3/source/train_group3.py",
       "A3PRE": G / "assignment-3/output/Group3_Assignment3/source/track3_preflight.py",
       "A3COL": G / "assignment-3/output/Group3_Assignment3/source/collect_results.py",
       "A3FIG": G / "assignment-3/output/Group3_Assignment3/source/make_figures.py",
       "A3REC": G / "assignment-3/output/Group3_Assignment3/source/run_recovery.py",
       "A2OUT": HERE / "ref/A2_notebook_outputs.txt",
       "A3OUT": HERE / "ref/A3_notebook_outputs.txt"}
SRC_LABEL = {"A2NB": "26L-9005_A2.ipynb", "A3NB": "Group3_Colab_Executed.ipynb", "A3SRC": "source/train_group3.py",
             "A3PRE": "source/track3_preflight.py", "A3COL": "source/collect_results.py",
             "A3FIG": "source/make_figures.py", "A3REC": "source/run_recovery.py",
             "A2OUT": "26L-9005_A2.ipynb · saved output", "A3OUT": "Group3_Colab_Executed.ipynb · saved output"}

VOICE, RATE = "en-US-AvaMultilingualNeural", "-6%"
W, H = 1920, 1080
FD = "C:/Windows/Fonts/"
f = lambda name, size: ImageFont.truetype(FD + name, size)
TITLE, BODY, BODY_BIG, SMALL, LABEL = f("segoeuib.ttf", 46), f("segoeui.ttf", 30), f("segoeui.ttf", 36), f("segoeui.ttf", 22), f("segoeuib.ttf", 24)
MATH = lambda size: ImageFont.truetype(FD + "cambria.ttc", size, index=1)
BG, INK, MUTED = (250, 249, 245), (33, 33, 33), (120, 120, 120)
KIND_COLOR = {"handout": (176, 96, 0), "code": (40, 90, 160), "figure": (30, 120, 80), "text": (90, 70, 140), "output": (20, 110, 120)}
KIND_LABEL = {"handout": "HANDOUT", "code": "OUR CODE", "figure": "RESULTS", "text": "IDEA", "output": "COLAB OUTPUT"}


def wrap_px(text, font, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if font.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    return lines + ([cur] if cur else [])


FALLBACK = set("∇⊙⌊⌋∂∘⊗")


def text_fb(d, xy, text, font, fill=INK):
    """Draw text, switching to Cambria Math for symbols Segoe UI lacks."""
    x, y = xy
    run = ""
    for ch in text + "\0":
        if ch == "\0" or ch in FALLBACK:
            if run:
                d.text((x, y), run, font=font, fill=fill)
                x += font.getlength(run)
                run = ""
            if ch != "\0":
                mf = MATH(font.size)
                d.text((x, y + font.size * 0.22), ch, font=mf, fill=fill)
                x += mf.getlength(ch)
        else:
            run += ch


def draw_bullets(d, bullets, x, y, width, font, color, gap=14):
    lh = int(font.size * 1.35)
    for b in bullets:
        sub = b.startswith("  ")
        xx = x + (34 if sub else 0)
        if not sub:
            d.ellipse([xx, y + lh // 2 - 6, xx + 12, y + lh // 2 + 6], fill=color)
        else:
            d.text((xx - 4, y), "–", font=font, fill=MUTED)
        for line in wrap_px(b.strip(), font, width - (xx - x) - 30):
            text_fb(d, (xx + 28, y), line, font)
            y += lh
        y += gap
    return y


def resolve(p):
    for k, v in PREFIX.items():
        if p.startswith(k):
            return v / p[len(k):]
    return Path(p)


# ---------------------------------------------------------------- handout crop with highlights
_docs = {}


def handout_image(pdf, page, phrases, box_w, box_h):
    doc = _docs.setdefault(pdf, fitz.open(HERE / "ref" / pdf))
    pg = doc[page - 1]
    rects = []
    for ph in phrases:
        found = pg.search_for(ph)
        if not found:
            raise ValueError(f"phrase not found on {pdf} p{page}: {ph!r}")
        rects += found
    u = fitz.Rect(rects[0])
    for r in rects[1:]:
        u |= r
    pr = pg.rect
    # text lines on the page; highlight the whole line that holds each phrase
    tl = [fitz.Rect(l["bbox"]) for b in pg.get_text("dict")["blocks"] if b.get("type") == 0 for l in b["lines"]]
    rects = [max((L for L in tl if L.intersects(r)), key=lambda L: (L & r).get_area(), default=r) | r for r in rects]
    u = fitz.Rect(rects[0])
    for r in rects[1:]:
        u |= r
    want_h = min(max(u.height + 200, 320), pr.height)
    cy = (u.y0 + u.y1) / 2
    y0 = max(0, min(cy - want_h / 2, pr.height - want_h))
    y1 = y0 + want_h
    # snap so no text line is cut in half
    for L in tl:
        if L.y0 < y0 < L.y1:
            y0 = L.y0 - 4
        if L.y0 < y1 < L.y1:
            y1 = L.y1 + 4
    clip = fitz.Rect(30, max(0, y0), pr.width - 30, min(pr.height, y1))
    zoom = min(box_w / clip.width, box_h / clip.height) * 1.0
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for r in rects:
        x0, yy0 = (r.x0 - clip.x0) * zoom, (r.y0 - clip.y0) * zoom
        x1, yy1 = (r.x1 - clip.x0) * zoom, (r.y1 - clip.y0) * zoom
        od.rectangle([x0 - 4, yy0 - 3, x1 + 4, yy1 + 3], fill=(255, 220, 0, 90), outline=(230, 120, 0, 255), width=3)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    return im, f"{'Assignment 2' if pdf.startswith('A2') else 'Assignment 3'} handout · page {page}"


# ---------------------------------------------------------------- code with syntax colours
STYLE = get_style_by_name("monokai")
_code_cache = {}


def tok_color(tt):
    while tt is not None:
        st = STYLE.style_for_token(tt)
        if st["color"]:
            return "#" + st["color"]
        tt = tt.parent
    return "#f8f8f2"


def output_image(src, start, n, box_w, box_h, hl=()):
    lines = _code_cache.setdefault(src, SRC[src].read_text(encoding="utf-8").splitlines())
    hits = [i for i, l in enumerate(lines) if start in l]
    if len(hits) != 1:
        raise ValueError(f"output start {start!r} in {src}: {len(hits)} matches")
    i0 = hits[0]
    cell = next((re.search(r"CELL (\d+)", lines[j]).group(1) for j in range(i0, -1, -1) if lines[j].startswith("# ===== CELL")), "?")
    raw = []
    for l in lines[i0:i0 + min(n, 30)]:
        if l.startswith("# ===== CELL") and raw:
            break
        if not l.startswith("# ===== CELL"):
            raw.append(l)
    label = f"{SRC_LABEL[src]} · cell {cell}"
    size = 22
    fnt = f("consola.ttf", size)
    cw = fnt.getlength("M")
    per = int((box_w - 60) // cw)
    rows = []   # (text, highlighted)
    for l in raw:
        on = any(h in l for h in hl)
        for k in range(0, max(len(l), 1), per):
            rows.append((l[k:k + per], on))
    lh = int(size * 1.4)
    maxrows = (box_h - 80) // lh
    if len(rows) > maxrows:
        rows = rows[:maxrows - 1] + [("…", False)]
    im = Image.new("RGB", (box_w, min(box_h, lh * len(rows) + 90)), (18, 24, 28))
    d = ImageDraw.Draw(im)
    d.text((24, 14), label, font=LABEL, fill=(120, 220, 220))
    y = 60
    for txt, on in rows:
        if on:
            d.rectangle([14, y - 3, box_w - 14, y + lh - 3], fill=(70, 62, 20))
        d.text((30, y), txt, font=fnt, fill=(255, 236, 140) if on else (215, 225, 225))
        y += lh
    return im, label


def code_image(src, start, n, box_w, box_h, hl=()):
    lines = _code_cache.setdefault(src, SRC[src].read_text(encoding="utf-8").splitlines())
    hits = [i for i, l in enumerate(lines) if start in l]
    if len(hits) != 1:
        raise ValueError(f"code start {start!r} in {src}: {len(hits)} matches")
    i0 = hits[0]
    n = min(n, 24)
    snippet = lines[i0:i0 + n]
    for k, l in enumerate(snippet):
        if k > 0 and l.startswith("# ===== CELL"):
            snippet = snippet[:k]
            break
    while snippet and not snippet[-1].strip():
        snippet.pop()
    snippet = [l for l in snippet]
    label = SRC_LABEL[src]
    if src.endswith("NB"):
        cell = next((re.search(r"CELL (\d+)", lines[j]).group(1) for j in range(i0, -1, -1) if lines[j].startswith("# ===== CELL")), "?")
        label += f" · cell {cell}"
        first = i0 - max(j for j in range(i0 + 1) if lines[j].startswith("# ===== CELL"))
    else:
        first = i0 + 1
        label += f" · line {first}"
    longest = max(len(l) for l in snippet)
    size = 26
    while size > 16:
        fnt = f("consola.ttf", size)
        if fnt.getlength("M" * (longest + 6)) <= box_w - 40 and size * 1.45 * len(snippet) <= box_h - 80:
            break
        size -= 1
    fnt = f("consola.ttf", size)
    lh = int(size * 1.45)
    im = Image.new("RGB", (box_w, min(box_h, lh * len(snippet) + 90)), (39, 40, 34))
    d = ImageDraw.Draw(im)
    for k, l in enumerate(snippet):
        if any(h in l for h in hl):
            d.rectangle([10, 60 + k * lh - 2, box_w - 10, 60 + (k + 1) * lh - 2], fill=(85, 78, 30))
            d.rectangle([10, 60 + k * lh - 2, 16, 60 + (k + 1) * lh - 2], fill=(250, 210, 60))
    d.text((24, 14), label, font=LABEL, fill=(166, 226, 46))
    y = 60
    code = "\n".join(snippet)
    x = 24 + fnt.getlength("0000 ")
    for k in range(len(snippet)):
        d.text((24, y + k * lh), f"{first + k:>4}", font=fnt, fill=(117, 113, 94))
    line_i, cx = 0, x
    for tt, val in PythonLexer().get_tokens(code):
        for part_i, part in enumerate(val.split("\n")):
            if part_i > 0:
                line_i += 1
                cx = x
            if part:
                if cx < box_w - 20:
                    d.text((cx, y + line_i * lh), part, font=fnt, fill=tok_color(tt))
                cx += fnt.getlength(part)
    return im, label


def fit(path, bw, bh):
    im = Image.open(path).convert("RGB")
    im.thumbnail((bw, bh), Image.LANCZOS)
    return im


# ---------------------------------------------------------------- slide render
def render(i, s, total, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    kind = s.get("kind", "text")
    col = KIND_COLOR[kind]
    d.rectangle([0, 0, W, 104], fill=col)
    d.text((44, 26), s["title"], font=TITLE, fill="white")
    tag = KIND_LABEL[kind]
    d.rounded_rectangle([W - 60 - LABEL.getlength(tag) - 24, 34, W - 44, 72], 8, fill="white")
    d.text((W - 60 - LABEL.getlength(tag) - 12, 38), tag, font=LABEL, fill=col)
    # progress bar + footer
    d.rectangle([0, H - 8, W, H], fill=(225, 225, 220))
    d.rectangle([0, H - 8, int(W * (i + 1) / total), H], fill=col)
    d.text((44, H - 44), s.get("section", ""), font=SMALL, fill=MUTED)
    d.text((W - 200, H - 44), f"slide {i + 1} / {total}", font=SMALL, fill=MUTED)

    left_w, top, bot = 1240, 130, H - 60
    panel = None
    if kind == "handout":
        panel, cap = handout_image(s.get("pdf") or ("A3_handout.pdf" if "a3" in Path(sys.argv[1]).name.lower() else "A2_handout.pdf"), s["page"], s["find"], left_w, bot - top - 40)
    elif kind == "code":
        panel, cap = code_image(s["src"], s["start"], s.get("n", 16), left_w, bot - top, s.get("hl", ()))
    elif kind == "output":
        panel, cap = output_image(s["src"], s["start"], s.get("n", 16), left_w, bot - top, s.get("hl", ()))
    elif kind == "figure":
        ims = [resolve(p) for p in (s.get("image"), s.get("image2")) if p]
        bh = (bot - top - 15 * (len(ims) - 1)) // len(ims)
        parts = [fit(p, left_w, bh) for p in ims]
        side = [fit(p, (left_w - 20) // 2, bot - top) for p in ims] if len(ims) == 2 else None
        if side and sum(p.width * p.height for p in side) > sum(p.width * p.height for p in parts):
            panel = Image.new("RGB", (side[0].width + side[1].width + 20, max(p.height for p in side)), BG)
            panel.paste(side[0], (0, 0))
            panel.paste(side[1], (side[0].width + 20, 0))
        else:
            panel = Image.new("RGB", (max(p.width for p in parts), sum(p.height for p in parts) + 15 * (len(parts) - 1)), BG)
            yy = 0
            for p in parts:
                panel.paste(p, ((panel.width - p.width) // 2, yy))
                yy += p.height + 15
        cap = None
    if panel is not None:
        px, py = 40 + (left_w - panel.width) // 2, top + max(0, (bot - top - panel.height - (36 if kind == "handout" else 0)) // 2)
        if kind == "handout":
            d.text((40, py - 2), cap, font=LABEL, fill=col)
            py += 34
            d.rectangle([px - 3, py - 3, px + panel.width + 2, py + panel.height + 2], outline=(200, 200, 195), width=3)
        img.paste(panel, (px, py))
        bx = 40 + left_w + 40
        d.line([bx - 20, top, bx - 20, bot], fill=(215, 215, 210), width=2)
        draw_bullets(d, s["bullets"], bx, top + 10, W - bx - 30, BODY, col)
    else:
        bullets = list(s["bullets"])
        y = top + 40
        first = bullets[0] if bullets else ""
        if s.get("formula") or (("=" in first or "≈" in first) and len(first) < 110 and not first.lower().startswith(("q:", "q."))):
            formula = s.get("formula") or bullets.pop(0)
            fsz = 52
            while MATH(fsz).getlength(formula) > W - 260 and fsz > 30:
                fsz -= 2
            fm = MATH(fsz)
            lines = wrap_px(formula, fm, W - 260)
            bh = len(lines) * int(fsz * 1.4) + 50
            d.rounded_rectangle([90, y, W - 90, y + bh], 16, fill=(255, 250, 230), outline=col, width=3)
            yy = y + 25
            for ln in lines:
                d.text(((W - fm.getlength(ln)) / 2, yy), ln, font=fm, fill=INK)
                yy += int(fsz * 1.4)
            y += bh + 40
        draw_bullets(d, bullets, 90, y, W - 180, BODY_BIG, col, gap=22)
    p = out / f"slide_{i:03d}.png"
    import io
    buf = io.BytesIO()
    img.save(buf, "PNG")
    if not p.exists() or p.read_bytes() != buf.getvalue():   # keep mtime if unchanged (segment cache)
        p.write_bytes(buf.getvalue())
    return p


# ---------------------------------------------------------------- audio / video
FF = imageio_ffmpeg.get_ffmpeg_exe()


def speakable(t):
    t = t.replace("x̂", "x hat ").replace("ε", "epsilon").replace("ᾱ", "alpha bar").replace("β", "beta")
    t = t.replace("α", "alpha").replace("σ", "sigma").replace("×", " by ").replace("≈", " about ")
    return re.sub(r"\s+", " ", t)


async def tts_all(slides, out):
    sem = asyncio.Semaphore(4)

    async def one(i, s):
        mp3 = out / f"audio_{i:03d}.mp3"
        key = out / f"audio_{i:03d}.txt"
        text = speakable(s["narration"])
        if mp3.exists() and key.exists() and key.read_text(encoding="utf-8") == text:
            return
        async with sem:
            for attempt in range(4):
                try:
                    await edge_tts.Communicate(text, VOICE, rate=RATE).save(str(mp3))
                    break
                except Exception as e:
                    print("retry tts", i, e)
                    await asyncio.sleep(3)
            else:
                raise RuntimeError(f"tts failed {i}")
        key.write_text(text, encoding="utf-8")

    await asyncio.gather(*(one(i, s) for i, s in enumerate(slides)))


def duration(path):
    r = subprocess.run([FF, "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


def main():
    slides = runpy.run_path(sys.argv[1])["SLIDES"]
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    title = sys.argv[3]
    pngs = [render(i, s, len(slides), out) for i, s in enumerate(slides)]
    print("rendered", len(pngs), "slides")
    if "--check" in sys.argv:
        return
    asyncio.run(tts_all(slides, out))
    segs, chapters, transcript, t, last = [], [], [], 0.0, None
    for i, s in enumerate(slides):
        seg = out / f"seg_{i:03d}.mp4"
        mp3 = out / f"audio_{i:03d}.mp3"
        fresh = seg.exists() and seg.stat().st_mtime > max(pngs[i].stat().st_mtime, mp3.stat().st_mtime)
        if not fresh:
          subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-framerate", "2", "-i", str(pngs[i]),
                        "-i", str(out / f"audio_{i:03d}.mp3"), "-c:v", "libx264", "-tune", "stillimage",
                        "-pix_fmt", "yuv420p", "-r", "2", "-c:a", "aac", "-b:a", "128k", "-ar", "24000",
                        "-af", "adelay=500|500,apad=pad_dur=1.3", "-t", f"{duration(mp3) + 1.8:.2f}",
                        str(seg)], check=True)
        dur = duration(seg)
        if s.get("section") != last:
            chapters.append((t, s.get("section")))
            last = s.get("section")
        mm, ss = divmod(int(t), 60)
        transcript.append(f"[{mm:02d}:{ss:02d}] {s['title']}\n{s['narration']}\n")
        segs.append(seg)
        t += dur
        print(f"{i + 1}/{len(slides)} {dur:5.1f}s {s['title']}")
    (out / "concat.txt").write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in segs))
    meta = [";FFMETADATA1", f"title={title}"]
    for k, (st, name) in enumerate(chapters):
        end = chapters[k + 1][0] if k + 1 < len(chapters) else t
        meta += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={int(st * 1000)}", f"END={int(end * 1000)}", f"title={name}"]
    (out / "meta.txt").write_text("\n".join(meta) + "\n", encoding="utf-8")
    final = out / (re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_") + ".mp4")
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(out / "concat.txt"),
                    "-i", str(out / "meta.txt"), "-map_metadata", "1", "-map", "0", "-c", "copy",
                    "-movflags", "+faststart", str(final)], check=True)
    (out / "transcript.txt").write_text("\n".join(transcript), encoding="utf-8")
    with open(out / "chapters.txt", "w", encoding="utf-8") as fh:
        fh.write(f"{title}: total {int(t // 60)} min {int(t % 60)} s\n")
        for st, name in chapters:
            fh.write(f"{int(st // 60):02d}:{int(st % 60):02d}  {name}\n")
    print("TOTAL", round(t / 60, 1), "min ->", final)


if __name__ == "__main__":
    main()
