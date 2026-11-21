"""Render sections of the real repo documents to PNG with headless Edge.

Each shot is one contiguous section of a repo Markdown file, cut by heading text
(no rewording), converted with python-markdown and screenshotted at 1920 px width.
Output: <OUT>/docs/<shot>.png (trimmed to content height) + docs/manifest.json
"""
import json, re, subprocess, sys
from pathlib import Path
import markdown
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]          # research-directions/build-test-reduction
OUT = Path(r"C:\Users\pc\study\bt-lab\video")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SHOTS = [
    # id, file, start marker (line startswith), end marker (line startswith) or None
    ("lit_top", "01-literature/literature-in-one-page.md", "# Study 1 literature", "## Four mechanisms"),
    ("lit_mech", "01-literature/literature-in-one-page.md", "## Four mechanisms", "## Five closest"),
    ("lit_closest", "01-literature/literature-in-one-page.md", "## Five closest", "## What we do NOT"),
    ("lit_notclaim", "01-literature/literature-in-one-page.md", "## What we do NOT", "*Details:*"),
    ("w2_glance", "02-practice-survey/README.md", "## At a glance", "## Files"),
    ("w2_head", "02-practice-survey/README.md", "## Headline", None),
    ("w3_targets", "03-experiment/readiness.md", "### 1.2 Chosen targets", "Rejected, with reason"),
    ("w3_replay", "03-experiment/readiness.md", "## 2. Iterative session", "## 3. Arms"),
    ("w3_arms", "03-experiment/readiness.md", "## 3. Arms", "\\* F1 at **function**"),
    ("w3_report", "03-experiment/readiness.md", "### 4.4 Reporting", "**Secondary"),
]

CSS = """
body{margin:0;background:#fbfaf7;color:#1c2230;font-family:'Segoe UI',Arial,sans-serif;font-size:23px;line-height:1.45}
main{padding:44px 70px 40px 70px}
h1{font-family:Georgia,serif;font-size:44px;margin:0 0 18px}
h2,h3{font-family:Georgia,serif;font-size:36px;margin:0 0 16px;color:#14213d}
table{border-collapse:collapse;margin:10px 0 18px;font-size:19px;line-height:1.35}
th,td{border:1px solid #c9cdd6;padding:8px 11px;vertical-align:top;text-align:left}
th{background:#eceef3}
code{font-family:Consolas,monospace;font-size:0.9em;background:#eef0f4;padding:1px 4px;border-radius:3px}
a{color:#1d4ed8;text-decoration:none}
strong{color:#0f172a}
ul,ol{margin:6px 0 12px} li{margin:3px 0} p{margin:8px 0 12px}
del{color:#888}
"""


def section(text, start, end):
    lines = text.splitlines()
    s = next(i for i, l in enumerate(lines) if l.startswith(start))
    e = len(lines)
    if end:
        e = next(i for i in range(s + 1, len(lines)) if lines[i].startswith(end))
    return "\n".join(lines[s:e]).strip() + "\n"


def edge_shot(html_path, png, h=4200):
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--screenshot={png}", f"--window-size=1920,{h}", html_path.as_uri()],
                   check=True, capture_output=True, timeout=120)


def trim(png, bg=(251, 250, 247)):
    im = Image.open(png).convert("RGB")
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg)).getbbox()
    bottom = min(im.height, diff[3] + 40) if diff else im.height
    im.crop((0, 0, 1920, bottom)).save(png)
    return bottom


def main():
    d = OUT / "docs"; d.mkdir(parents=True, exist_ok=True)
    manifest = {}
    only = set(sys.argv[1:])
    for sid, rel, a, b in SHOTS:
        if only and sid not in only:
            continue
        md = section((ROOT / rel).read_text(encoding="utf-8"), a, b)
        (d / f"{sid}.md").write_text(md, encoding="utf-8")
        # python-markdown needs a blank line before a list that follows a paragraph
        fixed, prev = [], ""
        for l in md.splitlines():
            is_li = bool(re.match(r"\s*([-*]|\d+\.)\s", l))
            prev_li = bool(re.match(r"\s*([-*]|\d+\.)\s", prev))
            if is_li and prev.strip() and not prev_li and not prev.startswith("|"):
                fixed.append("")
            fixed.append(l); prev = l
        body = markdown.markdown("\n".join(fixed), extensions=["tables", "sane_lists"])
        html = d / f"{sid}.html"
        html.write_text(f"<!doctype html><meta charset='utf-8'><style>{CSS}</style><main>{body}</main>", encoding="utf-8")
        png = d / f"{sid}.png"
        edge_shot(html, png)
        hgt = trim(png)
        manifest[sid] = {"source": rel, "start": a, "end": b, "height": hgt}
        print(sid, hgt)
    # positioning figure: the real SVG, scaled into a 1920x1080 page
    if not only or "fig_positioning" in only:
        svg = ROOT / "01-literature/figures/positioning.svg"
        html = d / "fig_positioning.html"
        html.write_text("<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#fbfaf7}"
                        "img{display:block;margin:30px auto;height:960px}</style>"
                        f"<img src='{svg.as_uri()}'>", encoding="utf-8")
        edge_shot(html, d / "fig_positioning.png", h=1080)
        manifest["fig_positioning"] = {"source": "01-literature/figures/positioning.svg", "height": 1080}
    mf = d / "manifest.json"
    old = json.loads(mf.read_text()) if mf.exists() else {}
    old.update(manifest)
    mf.write_text(json.dumps(old, indent=1))


if __name__ == "__main__":
    main()
