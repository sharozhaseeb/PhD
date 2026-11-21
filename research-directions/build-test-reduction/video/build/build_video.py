"""Build the Study 1 walkthrough: cards, framed doc shots with gentle motion, VO mix, clip list,
contact sheets. Rendering to MP4 is done by compose.ps1 (Windows MediaComposition, no ffmpeg).

python build_video.py            -> everything except the MP4
Outputs in C:\\Users\\pc\\study\\bt-lab\\video\\ : cards/, frames/, mix.wav, clips.txt, contact/
"""
import json, re, shutil, wave, struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]            # build-test-reduction
VID = Path(__file__).resolve().parents[1]             # video/
OUT = Path(r"C:\Users\pc\study\bt-lab\video")
W, H = 1920, 1080
HEAD, FOOT = 56, 50
VIEW_H = H - HEAD - FOOT                              # 974
FPS = 10
BG = (251, 250, 247); INK = (28, 34, 48); MUTED = (98, 106, 124); ACC = (190, 92, 20); BAR = (236, 233, 225)
FD = "C:/Windows/Fonts/"
F = lambda n, s: ImageFont.truetype(FD + n, s)
SERIF, SERIFB, SANS, SANSB, MONO = "georgia.ttf", "georgiab.ttf", "segoeui.ttf", "seguisb.ttf", "consola.ttf"
RES = ROOT / "03-experiment/results"

# ---------------------------------------------------------------- helpers

def canvas():
    return Image.new("RGB", (W, H), BG)


def text_wrap(d, xy, text, font, fill, width, gap=10):
    x, y = xy
    for para in text.split("\n"):
        line = ""
        for w in para.split(" "):
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) > width and line:
                d.text((x, y), line, font=font, fill=fill); y += font.size + gap; line = w
            else:
                line = t
        d.text((x, y), line, font=font, fill=fill); y += font.size + gap
    return y


def chrome(im, part, source):
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W, HEAD), fill=BAR)
    d.text((40, 13), part, font=F(SANSB, 24), fill=INK)
    t = "Study 1 walkthrough"; d.text((W - 40 - d.textlength(t, font=F(SANS, 22)), 15), t, font=F(SANS, 22), fill=MUTED)
    d.rectangle((0, H - FOOT, W, H), fill=BAR)
    if source:
        d.text((40, H - FOOT + 11), "Source: " + source, font=F(SANS, 22), fill=MUTED)
    return im


def pill(d, x, y, text, fill=ACC):
    f = F(SANSB, 26); w = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + w + 36, y + 46), radius=23, fill=fill)
    d.text((x + 18, y + 6), text, font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- cards

def card_title():
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((160, 330), "Study 1", font=F(SERIFB, 88), fill=INK)
    text_wrap(d, (160, 460), "Reduced build and test validation\nfor iterative code optimization", F(SERIF, 58), INK, 1600, 16)
    d.rectangle((160, 640, 240, 646), fill=ACC)
    d.text((160, 675), "Research walkthrough  ·  21 November 2026  ·  deterministic rules, no AI in the method",
           font=F(SANS, 32), fill=MUTED)
    return im


def card_roadmap():
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((160, 170), "Five parts", font=F(SERIFB, 64), fill=INK)
    rows = ["What the literature and existing optimizers do",
            "Future work the papers themselves state",
            "The gap we found, and what we do not claim",
            "The experiment designed on that gap, and its status so far",
            "What comes next"]
    y = 310
    for i, r in enumerate(rows, 1):
        d.ellipse((160, y, 222, y + 62), fill=ACC)
        d.text((191 - d.textlength(str(i), font=F(SANSB, 34)) / 2, y + 8), str(i), font=F(SANSB, 34), fill=(255, 255, 255))
        d.text((255, y + 6), r, font=F(SANS, 40), fill=INK); y += 110
    return im


def card_section1():
    src = (ROOT / "01-literature/literature-in-one-page.md").read_text(encoding="utf-8")
    q = re.search(r"\*\*The question\.\*\* (.+)", src).group(1).replace("*", "")
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((160, 250), "1", font=F(SERIFB, 120), fill=ACC)
    d.text((280, 280), "What the literature and practice show", font=F(SERIFB, 62), fill=INK)
    d.text((160, 470), "The question", font=F(SANSB, 30), fill=MUTED)
    text_wrap(d, (160, 520), "\u201c" + q + "\u201d", F(SERIF, 46), INK, 1600, 18)
    return chrome(im, "Part 1 · Literature and practice", "01-literature/literature-in-one-page.md")


FUTURE_ROWS = [  # (work, what the paper leaves open, quote or paraphrase, where it is recorded)
    ("PerfAgent (arXiv 2607.19653)", "\u201cextending selective testing to native-extension coverage\u201d", "§VII  ·  01-literature/notes/R1-perfagent-fullread.md"),
    ("Fallahzadeh, Rigby, Adams (EMSE 2025)", "\u201cexploring the impact of combining different test optimization algorithms\u201d", "p.54  ·  01-literature/notes/R2-batching-threats-fullread.md"),
    ("Ekstazi (ISSTA 2015)", "\u201cWe leave it as a future work to formally prove that Ekstazi is safe\u201d", "§3  ·  01-literature/notes/T2-rts.md"),
    ("Kotinos (IEEE TSE; early access 2020)", "Future-work section states its preconditions: pinned dependencies, idempotent tests, little conditional build behaviour (paraphrase)", "after §9  ·  01-literature/notes/T1-builds.md"),
    ("Agentic issue-resolution survey (arXiv 2512.22256)", "Program-analysis RTS \u201chas not been integrated\u201d; Python techniques \u201cremain unsafe\u201d", "§7.3  ·  01-literature/closest-works.md row 20"),
]


def card_future_papers():
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 90), "2", font=F(SERIFB, 90), fill=ACC)
    d.text((180, 108), "Future work the papers themselves state", font=F(SERIFB, 54), fill=INK)
    y = 245
    for work, what, where in FUTURE_ROWS:
        d.text((90, y), work, font=F(SANSB, 30), fill=INK)
        y2 = text_wrap(d, (90, y + 42), what, F(SERIF, 30), INK, 1740, 8)
        d.text((90, y2 + 2), where, font=F(SANS, 22), fill=MUTED)
        y = y2 + 46
    return chrome(im, "Part 2 · Future work stated in the literature", "quotes as recorded in the W1 reading notes (quotes under 15 words)")


def card_caveat():
    g = (ROOT / "01-literature/gap-and-search-log.md").read_text(encoding="utf-8")
    n = re.search(r"\*\*(\d+) records screened\.\*\*", g).group(1)
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((160, 200), "A caveat on the search", font=F(SERIFB, 62), fill=INK)
    rows = ["Targeted primary-source review, not a systematic one.",
            f"ACM DL and IEEE Xplore searched: {n} records screened.",
            "Not searched: Scopus, Web of Science.",
            "Forward citations screened only for PerfAgent and NameRTS.",
            "Novelty means only: \u201cnot found in our recorded searches\u201d."]
    y = 340
    for r in rows:
        d.rectangle((160, y + 20, 172, y + 32), fill=ACC)
        d.text((200, y), r, font=F(SANS, 40), fill=INK); y += 95
    return chrome(im, "Part 3 · The gap", "01-literature/README.md, gap-and-search-log.md")


def card_results():
    """Everything here is parsed from files in 03-experiment/results/ at render time."""
    files = sorted(p.relative_to(RES).as_posix() for p in RES.rglob("*") if p.is_file())
    nx = (RES / "raw/networkx_mining_subject_rule.txt").read_text(encoding="utf-8")
    m = re.search(r"subject-matching: (\d+) qualifying: (\d+)", nx)
    nx_rows = re.findall(r"^([0-9a-f]{8}) (\d{4}-\d{2}-\d{2}) ", nx, re.M)
    bn = (RES / "raw/bottleneck_mining.txt").read_text(encoding="utf-8")
    bm = re.search(r"# (\d+) subject matches, (\d+) qualifying", bn)
    bn_rows = re.findall(r"^([0-9a-f]{8}) (\d{4}-\d{2}-\d{2}) Y", bn, re.M)
    jx = next(RES.glob("raw/networkx/win-provisional/*.junit.xml")).read_text(encoding="utf-8")
    ts = re.search(r'<testsuite [^>]*failures="(\d+)" skipped="(\d+)" tests="(\d+)" time="([\d.]+)"', jx)
    facts = {
        "nx_match": m.group(1), "nx_qual": m.group(2), "nx_frozen": len(nx_rows),
        "nx_first": nx_rows[0][1], "nx_last": nx_rows[-1][1],
        "bn_match": bm.group(1), "bn_qual": bm.group(2), "bn_first": bn_rows[0][1], "bn_last": bn_rows[-1][1],
        "smoke_tests": ts.group(3), "smoke_time": ts.group(4), "smoke_fail": ts.group(1), "smoke_skip": ts.group(2),
        "files": files,
    }
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 95), "Data preparation so far", font=F(SERIFB, 54), fill=INK)
    pill(d, 1300, 100, "DATA PREPARATION, NOT RESULTS")
    col = [(90, "networkx: commit mining", "results/raw/networkx_mining_subject_rule.txt",
            [f"{facts['nx_match']} subject matches", f"{facts['nx_qual']} qualifying",
             f"latest {facts['nx_frozen']} frozen as the edit list", f"{facts['nx_first']} \u2192 {facts['nx_last']}"]),
           (700, "bottleneck: commit mining", "results/raw/bottleneck_mining.txt",
            [f"{facts['bn_match']} subject matches", f"{facts['bn_qual']} qualifying",
             "window " + re.search(r"window (\S+?)\.\.(\S+) \(exclusive\)", bn).group(1) + " .. " + re.search(r"window (\S+?)\.\.(\S+) \(exclusive\)", bn).group(2) + " (excl.)",
             f"{facts['bn_first']} \u2192 {facts['bn_last']}"]),
           (1310, "networkx: provisional smoke run", "results/raw/networkx/win-provisional/",
            [f"{int(facts['smoke_tests']):,} tests", f"{float(facts['smoke_time']):.1f} s wall time",
             f"{facts['smoke_fail']} failure, {facts['smoke_skip']} skipped",
             "Windows; superseded base 9c89eb0a", "not an experiment result"])]
    for x, title, path, lines in col:
        d.rounded_rectangle((x, 210, x + 560, 720), radius=14, outline=(205, 200, 190), width=2, fill=(255, 254, 251))
        d.text((x + 28, 232), title, font=F(SANSB, 30), fill=INK)
        y = 300
        for i, l in enumerate(lines):
            d.text((x + 28, y), l, font=F(SANSB if i == 0 else SANS, 40 if i == 0 else 31), fill=INK if i < 3 else MUTED)
            y += 72 if i == 0 else 56
        d.text((x + 28, 670), path, font=F(MONO, 19), fill=MUTED)
    text_wrap(d, (90, 750), "Frozen: 25 mutants and 10 slowdown candidates for networkx (frozen/FROZEN.md). Still to run: fault detection (kill sets), benchmark seconds, noise floor.",
              F(SANS, 30), INK, 1740, 8)
    d.text((90, 845), "RQ1 and RQ2 draft numbers follow.", font=F(SANS, 30), fill=MUTED)
    d.text((90, 905), f"{len(files)} files under 03-experiment/results/ at render time", font=F(SANS, 20), fill=MUTED)
    (OUT / "results_facts.json").write_text(json.dumps(facts, indent=1))
    return chrome(im, "Part 4 · Status: data preparation (preliminary)", "03-experiment/results/raw/ (numbers parsed from these files at render time)")


def card_rqs():
    ch = (ROOT / "pm/CHARTER.md").read_text(encoding="utf-8")
    sec = ch.split("## Research questions — revised")[1].split("## Research questions (original")[0]
    rqs = re.findall(r"- \*\*(RQ\d) — ([^.]+)\.\*\* (.+)", sec)
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 95), "Three research questions (revised)", font=F(SERIFB, 54), fill=INK)
    y = 220
    for rq, name, q in rqs:
        d.text((90, y), f"{rq} · {name}", font=F(SANSB, 34), fill=ACC)
        y = text_wrap(d, (90, y + 48), q, F(SANS, 30), INK, 1740, 8) + 34
    return chrome(im, "Part 1 · Research questions", "pm/CHARTER.md, “Research questions — revised 2026-11-21”")


def noisy_states():
    """State labels marked noisy in the RQ1 table of results/results.md (Load label column)."""
    md = (RES / "results.md").read_text(encoding="utf-8")
    return {m.group(1) for m in re.finditer(r"^\| (S\d+) \|[^\n]*\| \**noisy", md, re.M)}


def borderline_states():
    md = (RES / "results.md").read_text(encoding="utf-8")
    return {m.group(1) for m in re.finditer(r"^\| (S\d+) \|[^\n]*\| clean by rule, \**borderline", md, re.M)}


def card_cost():
    """Per-edit FULL cost chart plotted from a snapshot of results/rq1_networkx.csv; noisy states from results.md."""
    import csv, statistics
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = list(csv.DictReader(open(OUT / "rq1_networkx.snapshot.csv", encoding="utf-8")))
    noisy = noisy_states(); border = borderline_states()
    lab = [r["state"].split("_")[0] for r in rows]
    build = [float(r["build_s"]) for r in rows]
    tests = [float(r["tests_wall_s"]) for r in rows]
    clean = [i for i, l in enumerate(lab) if l not in noisy]
    ct = [tests[i] for i in clean]; share = [build[i] / tests[i] * 100 for i in clean]
    ntests = sorted({r["n_tests"] for r in rows}); nfail = sum(int(r["n_failed"]) for r in rows)
    total = sum(tests)
    fig, ax = plt.subplots(figsize=(11.2, 5.4), dpi=100)
    fig.patch.set_facecolor("#fbfaf7"); ax.set_facecolor("#fbfaf7")
    x = list(range(len(rows)))
    tc = ["#c9cdd6" if l in noisy else "#4a6fa5" for l in lab]
    ax.bar(x, build, color="#be5c14", width=0.65, label="Build (pip install -e .)")
    ax.bar(x, tests, bottom=build, color=tc, width=0.65, label="Full test suite, serial (wall)",
           hatch=None, edgecolor=["#8a8f9a" if l in noisy else "none" for l in lab])
    for i, l in enumerate(lab):
        if l in noisy:
            ax.text(i, build[i] + tests[i] + 2, f"noisy\n{tests[i]:.0f} s", ha="center", va="bottom", fontsize=10, color="#626a7c")
        elif l in border:
            ax.text(i, build[i] + tests[i] + 2, f"borderline\n{tests[i]:.0f} s", ha="center", va="bottom", fontsize=10, color="#1c2230")
    med = statistics.median(ct)
    ax.axhline(med, color="#1c2230", lw=1, ls="--")
    ax.text(len(rows) - 0.4, med + 2, f"clean median {med:.1f} s", ha="right", fontsize=10, color="#1c2230")
    ax.set_xticks(x, [l[1:] for l in lab], fontsize=11); ax.set_xlabel("replay state S0\u2013S18 (S0 = base)", fontsize=12)
    ax.set_ylabel("seconds per state", fontsize=12); ax.set_ylim(0, 165)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(frameon=False, fontsize=11, loc="upper left"); ax.grid(axis="y", color="#e3e0d8"); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(OUT / "rq1_chart.png", facecolor=fig.get_facecolor()); plt.close(fig)
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 85), "RQ1: what each edit costs to validate (networkx)", font=F(SERIFB, 50), fill=INK)
    pill(d, 90, 165, "PRELIMINARY \u00b7 SINGLE RUNS")
    im.paste(Image.open(OUT / "rq1_chart.png"), (40, 240))
    tx = 1200
    facts = [f"{len(rows)} states; {len(clean)} clean, {len(noisy)} noisy ({', '.join(sorted(noisy, key=lambda z: int(z[1:])))})"
             + (f"; {', '.join(sorted(border))} borderline clean" if border else ""),
             f"Serial tests, clean states: median {med:.1f} s, range {min(ct):.1f}\u2013{max(ct):.1f} s",
             f"{', '.join(f'{int(n):,}' for n in ntests)} tests, {nfail} failed at every state",
             f"Build / test time, clean states: {min(share):.2f}\u2013{max(share):.2f} %",
             f"Session total, serial tests, all {len(rows)} runs: {total:.0f} s (about {total / 60:.0f} min)",
             "Benchmarks: lower bound on the next card"]
    y = 255
    for f_ in facts:
        y = text_wrap(d, (tx, y), f_, F(SANS, 28), INK, 660, 6) + 16
    text_wrap(d, (tx, y + 6), "Noisy/borderline labels from results.md; that rule was written after the first look (not pre-registered). All states to be re-timed idle.",
              F(SANS, 22), MUTED, 660, 4)
    cf = {"rows": len(rows), "clean": len(clean), "noisy": sorted(noisy), "median": med, "range": [min(ct), max(ct)],
          "share_pct": [min(share), max(share)], "total_s": total, "n_tests": ntests, "failed": nfail}
    (OUT / "cost_facts.json").write_text(json.dumps(cf, indent=1))
    return chrome(im, "Part 4 \u00b7 Cost (RQ1), preliminary", "03-experiment/results/rq1_networkx.csv; noisy labels from results/results.md (RQ1 table)")


def card_contrast():
    import csv
    md = (RES / "rq1_bottleneck_build.md").read_text(encoding="utf-8")
    row = lambda key: re.search(r"^\| \**" + re.escape(key) + r"\** \|.*?\| \**([\d.]+)\** \|", md, re.M).group(1)
    clean = row("Clean build"); tmpl_b = row("B"); hdr_c = row("C"); iter_d = row("D"); e = row("E"); f_ = row("F"); null_g = row("G")
    tests = re.search(r"full test suite takes \*\*([\d.]+) s\*\* \((\d+) passed", md)
    share_bn = float(clean) / (float(clean) + float(tests.group(1))) * 100
    hz_label = re.search(r"\*\*Stale-build hazard \(([^)]*)\):\*\*", md).group(1)
    fx = re.search(r"Upstream fixed exactly this on (\d{4}-\d{2}-\d{2}) in `([0-9a-f]+)`", md)
    fix_date, fix_sha = fx.group(1), fx.group(2)
    assert "already contains the fix" in md
    nz = noisy_states(); rows = [r for r in csv.DictReader(open(OUT / "rq1_networkx.snapshot.csv", encoding="utf-8")) if r["tests_wall_s"] and r["state"].split("_")[0] not in nz]
    sh = [float(r["build_s"]) / (float(r["build_s"]) + float(r["tests_wall_s"])) * 100 for r in rows]
    bmin = min(float(r["build_s"]) for r in rows); bmax = max(float(r["build_s"]) for r in rows)
    tmin = min(float(r["tests_wall_s"]) for r in rows); tmax = max(float(r["tests_wall_s"]) for r in rows)
    incr = sorted(float(x) for x in (tmpl_b, hdr_c, e, f_))
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 85), "Build share: pure Python vs C extension", font=F(SERIFB, 50), fill=INK)
    pill(d, 90, 165, "PRELIMINARY \u00b7 SINGLE RUNS")
    cols = [(90, "networkx (pure Python)", f"{len(rows)} clean replay states (noisy {', '.join(sorted(nz))} excluded)",
             [f"Build {bmin:g}\u2013{bmax:g} s per state", f"Full tests {tmin:.1f}\u2013{tmax:.1f} s (serial)",
              f"Build share of build + tests: {min(sh):.1f}\u2013{max(sh):.1f} %"], "results/rq1_networkx.csv (snapshot)"),
            (990, "bottleneck (C extension)", "setup probes at the base; timing labelled noisy",
             [f"Clean build {clean} s vs full tests {tests.group(1)} s", f"Build share of clean build + tests: about {share_bn:.0f} %",
              f"Incremental {incr[0]:.2f}\u2013{incr[-1]:.2f} s; null rebuild {null_g} s",
              f"Probe D at the old base: iterators.h edit, nothing rebuilt ({iter_d} s)",
              f"Stale-build hazard ({hz_label})",
              f"Fixed upstream {fix_date} in {fix_sha}; our replay base already contains the fix",
              "A real unsafe-incremental-build bug the maintainers had to fix; we probe its consequence counterfactually"],
             "results/rq1_bottleneck_build.md")]
    for x, title, sub, lines, src in cols:
        d.rounded_rectangle((x, 250, x + 840, 880), radius=14, outline=(205, 200, 190), width=2, fill=(255, 254, 251))
        d.text((x + 30, 275), title, font=F(SANSB, 36), fill=INK)
        d.text((x + 30, 325), sub, font=F(SANS, 24), fill=MUTED)
        y = 395
        for i, l in enumerate(lines):
            y = text_wrap(d, (x + 30, y), l, F(SANSB if "share" in l else SANS, 28), ACC if "hazard" in l else INK, 780, 4) + 12
        d.text((x + 30, 835), src, font=F(MONO, 20), fill=MUTED)
    facts = dict(clean=clean, tests=tests.group(1), share_bn=share_bn, incr=incr, null=null_g, iter_d=iter_d,
                 nx_share=[min(sh), max(sh)], nx_build=[bmin, bmax], nx_tests=[tmin, tmax], nx_states=len(rows))
    (OUT / "contrast_facts.json").write_text(json.dumps(facts, indent=1))
    return chrome(im, "Part 4 \u00b7 Cost (RQ1), preliminary", "03-experiment/results/rq1_bottleneck_build.md and rq1_networkx.csv")


def md_table(text, first_header):
    """Rows of the first Markdown table whose header starts with first_header, as dicts keyed by bold-stripped header."""
    lines = text.splitlines()
    i = next(k for k, l in enumerate(lines) if l.startswith("| " + first_header))
    hdr = [h.strip().replace("*", "") for h in lines[i].strip("|").split("|")]
    out = []
    for l in lines[i + 2:]:
        if not l.startswith("|"):
            break
        cells = [c.strip().replace("*", "").replace("`", "") for c in l.strip("|").split("|")]
        out.append(dict(zip(hdr, cells)))
    return out


def _rq2():
    md = (RES / "results.md").read_text(encoding="utf-8")
    sec = md.split("## RQ2/RQ3")[1].split("## Harness")[0]
    return sec, md_table(sec, "Arm (rules.md)")


def card_rq2():
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    sec, rows = _rq2()
    by = {r["Arm (rules.md)"].split(" (")[0]: r for r in rows}
    arms = [("A0 FULL", "FULL"), ("A2 TESTMON", "testmon\n(PerfAgent-style)"), ("A3 CHANGED_MODULE", "changed-module\n(naive)"),
            ("A2 + full every k=5", "testmon +\nfull every k=5"), ("A2 + full every k=3", "testmon +\nfull every k=3"), ("A4 OURS", "OURS (A4)")]
    e2e = [float(by[a]["Est. end-to-end s"]) for a, _ in arms]
    meas = [by[a]["Measured end-to-end s"] for a, _ in arms]
    tests = [int(by[a]["Tests run (Σ 18 steps)"].replace(" ", "")) for a, _ in arms]
    fc = [int(by[a]["Full checks"]) for a, _ in arms]
    fig, ax = plt.subplots(figsize=(11.2, 5.8), dpi=100)
    fig.patch.set_facecolor("#fbfaf7"); ax.set_facecolor("#fbfaf7")
    cols = ["#8a8f9a", "#4a6fa5", "#4a6fa5", "#4a6fa5", "#4a6fa5", "#be5c14"]
    ax.bar(range(len(arms)), e2e, color=cols, width=0.6, label="estimated end-to-end")
    for i in range(len(arms)):
        m = meas[i].split(" ")[0]
        has = m not in ("\u2014", "-", "")
        top = e2e[i]
        lab = f"est. {e2e[i]:,.0f} s"
        if has:
            ax.plot([i - 0.3, i + 0.3], [float(m)] * 2, color="#1c2230", lw=3)
            top = max(top, float(m)); lab += f"\nmeasured {float(m):,.0f} s"
        ax.text(i, top + 25, lab + f"\n{tests[i]:,} tests \u00b7 {fc[i]} full", ha="center", va="bottom", fontsize=10.5, color="#1c2230")
    ax.set_xticks(range(len(arms)), [l for _, l in arms], fontsize=11.5)
    ax.set_ylabel("seconds over 18 edits (tests + build + startup)", fontsize=11.5)
    ax.set_ylim(0, max(e2e) * 1.32); ax.set_xlim(-0.6, len(arms) - 0.1)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="#e3e0d8"); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(OUT / "rq2_chart.png", facecolor=fig.get_facecolor()); plt.close(fig)
    cal = re.search(r"est\. end-to-end for FULL is (\d+) s, vs \*\*(\d+) s measured\*\*", sec)
    st = re.search(r"\*\*([\d.]+) s pytest startup\*\*", sec).group(1)
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 80), "RQ2/RQ3: test-side cost per arm (networkx, 18 edits)", font=F(SERIFB, 46), fill=INK)
    d.text((820, 158), "Cost only; benchmarks not yet included; functional misses next.", font=F(SANSB, 28), fill=INK)
    pill(d, 90, 150, "PRELIMINARY \u00b7 COUNTS ONLY")
    pill(d, 560, 150, "COST ONLY", fill=(98, 106, 124))
    im.paste(Image.open(OUT / "rq2_chart.png"), (40, 215))
    tx = 1200
    lines = [f"Est. end-to-end = est. test-seconds + build + {st} s pytest startup per step that runs tests.",
             f"Calibration: FULL est. {cal.group(1)} s vs {cal.group(2)} s measured.",
             "Black tick = measured end-to-end, where it exists; testmon's is labelled concurrent (CPU-pinned).",
             "Benchmarks are not in these totals.",
             "testmon and changed-module alone have no safety backstop.",
             "Cost alone ranks nothing: functional misses are on the next slide."]
    y = 245
    for l in lines:
        y = text_wrap(d, (tx, y), l, F(SANS, 26), INK, 670, 6) + 18
    (OUT / "rq2_facts.json").write_text(json.dumps({a: [e, m, t, f] for (a, _), e, m, t, f in zip(arms, e2e, meas, tests, fc)}, indent=1))
    return chrome(im, "Part 4 \u00b7 RQ2/RQ3 draft counts", "03-experiment/results/results.md (RQ2/RQ3 table); per-arm data in results/sim/networkx/")


def card_worked():
    md = (RES / "worked-edit.md").read_text(encoding="utf-8")
    edit = re.search(r"\*\*Edit:\*\* `([0-9a-f]+)` \u2014 (.+)", md)
    fn = re.search(r"\*\*Changed functions \(bth.changed_fns\):\*\* `([^`]+)`", md).group(1)
    rows = md_table(md, "Arm | Build")
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 85), "Worked edit: step 10, FULL vs reduced", font=F(SERIFB, 50), fill=INK)
    pill(d, 90, 160, "PRELIMINARY \u00b7 ONE EDIT, EXPLAINS THE MECHANISM")
    d.text((90, 240), f"Edit {edit.group(1)}: {edit.group(2)[:78]}", font=F(SANS, 28), fill=INK)
    d.text((90, 285), "Changed function: " + fn.split("::")[-1] + "  (" + fn.split("::")[0] + ")", font=F(MONO, 22), fill=MUTED)
    e2e_key = next(k for k in rows[0] if k.startswith("Est. end-to-end"))
    cols = [("Arm", "Arm", 90), ("Build", "Build", 700), ("Tests run", "Tests run", 1150), ("Benchmarks run", "Benchmarks run", 1450)]
    y = 350
    for title, _, x in cols:
        d.text((x, y), title, font=F(SANSB, 24), fill=INK)
    d.line((90, y + 40, 1830, y + 40), fill=(205, 200, 190), width=2)
    y += 56
    for r in rows:
        ours = "ours" in r["Arm"]
        for _, key, x in cols:
            v = r[key]
            if key == "Tests run":
                v = f"{int(v):,}"
            d.text((x, y), v[:36], font=F(SANSB if ours else SANS, 25), fill=ACC if ours else INK)
        y += 50
    d.text((90, y + 14), "Test counts only; seconds for this edit are in the file.", font=F(SANS, 22), fill=MUTED)
    cav = re.search(r"\*\*Caveat\.\*\* (.+)", md).group(1).replace("`", "")
    text_wrap(d, (90, y + 60), "Caveat (from the file): " + cav, F(SANS, 26), MUTED, 1740, 6)
    (OUT / "worked_facts.json").write_text(json.dumps(rows, indent=1))
    return chrome(im, "Part 4 \u00b7 Worked edit", "03-experiment/results/worked-edit.md")


def card_findings():
    sec, rows = _rq2()
    f1 = re.search(r"\*\*(A4 currently behaves like periodic full checks at k \u2248 4\.)\*\* Its score trigger fired at steps ([\d, and]+), plus the final check: (\d+) full checks", sec)
    f1b = re.search(r"Its cost \(([\d]+) s est\. end-to-end\) sits \*\*between A2 \+ k=5 \((\d+) s\) and A2 \+ k=3 \((\d+) s\)\*\*", sec)
    f2 = re.search(r"\*\*(Headline ratio, end-to-end where measured\.)\*\* testmon took \*\*(\d+) s measured\*\* for S1\u2013S18, vs \*\*(\d+) s measured\*\* for FULL serial tests \+ build: about \*\*(\d+)\u00d7 cheaper\*\*, not the (\d+)\u00d7 that test-seconds alone suggest \((\d+) vs (\d+)\)\. Startup and testmon's own analysis dominate its real cost\. Its first run \(DB build at S0\) took ([\d.]+) s vs ([\d.]+) s plain, ([\d.]+)\u00d7", sec)
    assert "design finding about the pre-registered score" in sec and "module-level edit" in sec
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 85), "Two draft findings, in W3's words", font=F(SERIFB, 50), fill=INK)
    pill(d, 90, 160, "PRELIMINARY \u00b7 DRAFT FINDINGS")
    y = 245
    d.text((90, y), "1 \u00b7 " + f1.group(1) + "  (design finding)", font=F(SANSB, 32), fill=ACC)
    y = text_wrap(d, (90, y + 50), f"Its score trigger fired at steps {f1.group(2)}, plus the final check: {f1.group(3)} full checks, each caused by a module-level edit, "
                  f"which expands to every function of the module and pushes the score past T = 10. Its cost ({f1b.group(1)} s est. end-to-end) sits between "
                  f"A2 + k=5 ({f1b.group(2)} s) and A2 + k=3 ({f1b.group(3)} s). T is not retuned.", F(SANS, 27), INK, 1740, 6) + 26
    d.text((90, y), "2 \u00b7 " + f2.group(1), font=F(SANSB, 32), fill=ACC)
    y = text_wrap(d, (90, y + 50), f"testmon took {f2.group(2)} s measured for S1\u2013S18, vs {f2.group(3)} s measured for FULL serial tests + build: about "
                  f"{f2.group(4)}\u00d7 cheaper, not the {f2.group(5)}\u00d7 that test-seconds alone suggest ({f2.group(6)} vs {f2.group(7)}). Startup and testmon's own "
                  f"analysis dominate its real cost. Its first run (DB build at S0) took {f2.group(8)} s vs {f2.group(9)} s plain, {f2.group(10)}\u00d7. "
                  "testmon's measured time is labelled concurrent (CPU-pinned).", F(SANS, 27), INK, 1740, 6) + 34
    d.rounded_rectangle((90, y, 1830, y + 150), radius=14, outline=(98, 106, 124), width=2)
    d.text((120, y + 20), "PENDING", font=F(SANSB, 28), fill=MUTED)
    d.text((120, y + 65), "Slowdown detection \u00b7 the bottleneck iterators.h hazard (consequence study) \u00b7 a measured full benchmark pass.",
           font=F(SANS, 27), fill=INK)
    d.text((120, y + 105), "Pending or scheduled (results.md). Latent re-check: done (0 of 5).", font=F(SANS, 27), fill=INK)
    (OUT / "findings_facts.json").write_text(json.dumps([f1.groups(), f1b.groups(), f2.groups()], indent=1))
    return chrome(im, "Part 4 \u00b7 Draft findings", "03-experiment/results/results.md (RQ2/RQ3 section, Reading)")


def card_bench():
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    md = (RES / "results.md").read_text(encoding="utf-8")
    sec = md.split("## RQ1 headline")[1].split("\n## ")[0]
    h = re.search(r"\*\*([\d.]+) h \(1 process\), ([\d.]+) h \(2 processes, asv's default\), ([\d.]+) h \(5 processes, our protocol\)\*\*", sec)
    rest = re.search(r"\*\*\u2248 (\d+) s for build \+ serial tests\*\*", sec).group(1)
    ratio = re.search(r"benchmarks about \*\*([\d\u2013]+)\u00d7\*\*", sec).group(1)
    obs = re.search(r"completed \*\*(\d+) of (\d+) cases in (\d+) s\*\*", sec)
    imp = re.search(r"takes \*\*([\d\u2013]+) s\*\*", sec).group(1)
    n49 = re.search(r"That module holds \*\*(\d+) of the (\d+) cases\*\*", sec)
    assert "lower bound" in sec and "scheduled" in sec
    hrs = [float(x) for x in h.groups()]
    labels = [f"build + serial tests\n(measured, \u2248{rest} s)", "benchmark pass, 1 process\n(lower bound)",
              "2 processes (asv default)\n(lower bound)", "5 processes (our protocol)\n(lower bound)"]
    vals = [float(rest)] + [x * 3600 for x in hrs]
    fig, ax = plt.subplots(figsize=(11.0, 4.6), dpi=100)
    fig.patch.set_facecolor("#fbfaf7"); ax.set_facecolor("#fbfaf7")
    ax.barh(range(4), vals, color=["#4a6fa5", "#be5c14", "#be5c14", "#be5c14"], height=0.55)
    ax.set_xscale("log"); ax.invert_yaxis()
    for i, v in enumerate(vals):
        ax.text(v * 1.08, i, f"{v:.0f} s" if i == 0 else f"\u2265 {hrs[i - 1]} h", va="center", fontsize=13, color="#1c2230")
    ax.set_yticks(range(4), labels, fontsize=12); ax.set_xlim(30, 1.2e5)
    ax.set_xlabel("seconds per edit (log scale)", fontsize=12)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color="#e3e0d8"); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(OUT / "bench_chart.png", facecolor=fig.get_facecolor()); plt.close(fig)
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 80), "RQ1 headline: benchmarks dominate per-edit cost", font=F(SERIFB, 50), fill=INK)
    pill(d, 90, 155, "PRELIMINARY \u00b7 LOWER BOUND (IMPORT COST ONLY)")
    d.text((90, 225), f"One FULL benchmark pass is about {ratio}\u00d7 the rest of FULL validation (networkx).", font=F(SANSB, 32), fill=INK)
    im.paste(Image.open(OUT / "bench_chart.png"), (60, 280))
    tx = 1220; y = 300
    for l in [f"Cause: benchmark_algorithms.py builds its graphs at import time: {imp} s per import.",
              f"It holds {n49.group(1)} of the {n49.group(2)} cases, and per-case process isolation repeats the import.",
              f"Observed: a concurrent run did {obs.group(1)} of {obs.group(2)} cases in {int(obs.group(3)):,} s, and was stopped.",
              "A measured full pass on an idle machine is scheduled."]:
        y = text_wrap(d, (tx, y), l, F(SANS, 26), INK, 650, 6) + 18
    (OUT / "bench_facts.json").write_text(json.dumps(dict(hours=hrs, rest=rest, ratio=ratio, obs=obs.groups(), imp=imp, n=n49.groups()), indent=1))
    return chrome(im, "Part 4 \u00b7 Cost (RQ1), preliminary", "03-experiment/results/results.md (RQ1 headline); raw/networkx/bench/")


def card_faults():
    md = (RES / "results.md").read_text(encoding="utf-8")
    sec = md.split("### Fault detection on the frozen mutant set")[1].split("\n### ")[0]
    rows = md_table(sec, "Arm | Missed")
    killed = re.search(r"\*\*(\d+) are killed by FULL\*\* at their state\. That makes N = (\d+)", sec)
    tot = re.search(r"\*\*Set:\*\* (\d+) frozen mutants", sec).group(1)
    assert "by construction" in sec and "buys no extra functional detection" in sec
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 80), "Fault detection: frozen mutants (networkx, functional)", font=F(SERIFB, 46), fill=INK)
    pill(d, 90, 150, "PRELIMINARY \u00b7 N = " + killed.group(2))
    d.text((560, 157), f"{tot} frozen mutants; {killed.group(1)} killed by FULL, so N = {killed.group(2)}. 0 / {killed.group(2)} is not \u201csafe\u201d.", font=F(SANS, 28), fill=INK)
    cols = [("Arm", 90, 640), ("Missed (k / N)", 760, None), ("95 % Wilson CI of miss rate", 1000, None), ("Caught by selection / full check / final", 1360, 470)]
    y = 230
    for t, x, _ in cols:
        d.text((x, y), t, font=F(SANSB, 22), fill=INK)
    d.line((90, y + 36, 1830, y + 36), fill=(205, 200, 190), width=2); y += 48
    for r in rows:
        a3 = r["Arm"].startswith("A3 CHANGED_MODULE")
        vals = [r["Arm"], r["Missed (k / N)"], r["95 % Wilson CI of miss rate"], r["Caught by selection / full check / final"]]
        for (t, x, w), v in zip(cols, vals):
            text_wrap(d, (x, y), v, F(SANSB if a3 else SANS, 22), ACC if a3 else INK, w or 340, 2)
        y += 44
    y += 16
    for l in ["Why A3 missed: its name rule maps no test file to the module (test_isomorphism.py, test_katz_centrality.py); any periodic full check catches both 1\u20133 steps later.",
              "Honest reading: on this fault class, selection catches almost everything by construction. At equal detection (20 / 20), plain testmon is the cheapest; our policy's extra cost buys no extra functional detection here."]:
        y = text_wrap(d, (90, y), l, F(SANS, 25), INK, 1740, 5) + 14
    (OUT / "fault_facts.json").write_text(json.dumps(dict(rows=rows, killed=killed.groups(), total=tot), indent=1))
    return chrome(im, "Part 4 \u00b7 Fault detection (RQ2/RQ3)", "03-experiment/results/results.md (Fault detection on the frozen mutant set); sim/networkx/rq2_steps.csv.faults.csv")


def card_coverage():
    md = (RES / "results.md").read_text(encoding="utf-8")
    sec = md.split("### Benchmark selection")[1].split("\n### ")[0]
    b1 = re.search(r"for \*\*(\d+) of the (\d+) edits\*\*, the S0 profile of \*\*no\*\* benchmark case executes any function the edit changed \(module-level lines excluded\)\. The steps are ([\d, \u2013and]+)\.", sec)
    oth = re.search(r"\(steps ([^)]*)\)", sec.split("**The other")[1]).group(1)
    covered = {int(a): int(b) for a, b in re.findall(r"(\d+): (\d+)", oth)}
    b2 = re.search(r"selects the benchmark: (\d+)/(\d+) at steps ([\d\u2013]+)\.", sec)
    assert "not a selection result" in sec and "Checkpoint re-profiling" in sec
    fsec = md.split("### Fault detection on the frozen mutant set")[1].split("\n### ")[0]
    lat = re.search(r"\*\*None becomes detectable at any later state, so there are (\d+) latent faults, fewer than (\d+)\.\*\*", fsec)
    surv = re.search(r"\*\*(\d+) survive FULL\*\*", fsec).group(1)
    assert "The pre-registered null stands" in fsec
    n = int(b1.group(2))
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 80), "Benchmark coverage, profile selection, latent faults", font=F(SERIFB, 46), fill=INK)
    pill(d, 90, 150, "PRELIMINARY \u00b7 COUNTS ONLY")
    d.text((90, 225), f"B1 \u00b7 For {b1.group(1)} of the {n} edits, no benchmark's S0 profile executes any edited function (module-level lines excluded).", font=F(SANSB, 30), fill=ACC)
    x0, w, y0 = 90, 96, 280
    for k in range(1, n + 1):
        c = covered.get(k)
        fill = (74, 111, 165) if c else (225, 222, 214)
        d.rounded_rectangle((x0 + (k - 1) * w, y0, x0 + (k - 1) * w + w - 10, y0 + 80), radius=8, fill=fill)
        d.text((x0 + (k - 1) * w + 10, y0 + 6), str(k), font=F(SANSB, 22), fill=(255, 255, 255) if c else INK)
        d.text((x0 + (k - 1) * w + 10, y0 + 40), f"{c} case{'s' if c != 1 else ''}" if c else "none", font=F(SANS, 19), fill=(255, 255, 255) if c else MUTED)
    d.text((90, y0 + 92), "edit step 1\u201318; blue = at least one benchmark case executes a changed function (count of cases)", font=F(SANS, 22), fill=MUTED)
    y = text_wrap(d, (90, 420), "So even FULL benchmarking cannot confirm the claimed speed-up of most of these commits with the project's own suite.", F(SANS, 28), INK, 1740, 6) + 26
    d.text((90, y), f"B2 \u00b7 Our profile selection, as specified, collapses to all benchmarks: {b2.group(1)}/{b2.group(2)} at steps {b2.group(3)}.", font=F(SANSB, 30), fill=ACC)
    y = text_wrap(d, (90, y + 48), "The rule needs profiles re-measured at each full check; only S0 profiles exist. A design gap (missing input), not a selection result. "
                  "Checkpoint re-profiling is not yet done.", F(SANS, 28), INK, 1740, 6) + 26
    d.text((90, y), f"Latent faults \u00b7 {lat.group(1)} of {surv} surviving mutants became detectable later (pre-registered threshold: {lat.group(2)}).", font=F(SANSB, 30), fill=ACC)
    text_wrap(d, (90, y + 48), "The pre-registered null for accumulation stands on networkx: reported as such, not as evidence for or against accumulation.",
              F(SANS, 28), INK, 1740, 6)
    (OUT / "coverage_facts.json").write_text(json.dumps(dict(b1=b1.groups(), covered=covered, b2=b2.groups(), latent=lat.groups(), survivors=surv), indent=1))
    return chrome(im, "Part 4 \u00b7 Benchmarks and latent faults", "03-experiment/results/results.md (Benchmark selection; Fault detection, latent re-check); raw/networkx/profile/S0_181f2951.json")


def card_future():
    rows = [("Benchmark coverage of optimized code (W3, B1)", "Most replayed edits are executed by no benchmark; how to confirm their speed-ups", "03-experiment/results/results.md, Finding B1"),
            ("Checkpoint re-profiling (W3, B2)", "Re-measure profiles at each full check so profile-based benchmark selection has its input", "03-experiment/results/results.md, Finding B2"),
            ("Literature (W1 open items)", "Backward citation screening; screening around Najafi 2019, Grambow 2022, Daly 2020; full text of Chittimalli & Harrold 2009", "01-literature/gap-and-search-log.md"),
            ("Comparator (W3)", "NameRTS (github.com/ZJU-CTAG/NameRTS) as a post-meeting comparator", "03-experiment/readiness.md §3"),
            ("Next study", "AI-based selection, measured against this deterministic baseline", "pm/CHARTER.md")]
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((90, 90), "5", font=F(SERIFB, 90), fill=ACC)
    d.text((180, 108), "Future work", font=F(SERIFB, 54), fill=INK)
    y = 250
    for a, b, c in rows:
        d.text((90, y), a, font=F(SANSB, 30), fill=INK)
        y2 = text_wrap(d, (90, y + 42), b, F(SANS, 32), INK, 1740, 8)
        d.text((90, y2), c, font=F(SANS, 22), fill=MUTED)
        y = y2 + 44
    return chrome(im, "Part 5 · Future work", "files named under each item")


def card_close():
    im = canvas(); d = ImageDraw.Draw(im)
    d.text((160, 360), "Study 1: where it stands", font=F(SERIFB, 70), fill=INK)
    d.rectangle((160, 470, 240, 476), fill=ACC)
    d.text((160, 510), "Literature and practice survey final  ·  gap stated  ·  experiment in preparation", font=F(SANS, 36), fill=MUTED)
    text_wrap(d, (160, 860), "Narration is synthetic; documents and analyses were prepared with AI assistance and reviewed by the student.",
              F(SANS, 28), MUTED, 1600)
    return im

# ---------------------------------------------------------------- doc shots with motion

def page_for(doc_png, fit=False):
    im = Image.open(doc_png).convert("RGB")
    if fit and im.height > VIEW_H:
        s = VIEW_H / im.height; im = im.resize((int(im.width * s), VIEW_H), Image.LANCZOS)
    ph = max(VIEW_H, im.height)
    page = Image.new("RGB", (W, ph), BG)
    page.paste(im, ((W - im.width) // 2, (ph - im.height) // 2))
    return page


def ease(t):
    return t * t * (3 - 2 * t)


def view(page, cx, cy, z):
    w = W / z; h = VIEW_H / z
    x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * page.height - h / 2, 0), page.height - h)
    return page.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, VIEW_H), Image.LANCZOS)


def framed(content, part, source):
    im = canvas(); im.paste(content, (0, HEAD)); return chrome(im, part, source)

# ---------------------------------------------------------------- timeline

PART = {1: "Part 1 · Literature and practice", 3: "Part 3 · The gap", 4: "Part 4 · The experiment"}
D = "01-literature/literature-in-one-page.md"
SEGMENTS = [
    # id, kind, arg, vo, extra kwargs
    ("00", "card", card_title, "00_title", {}),
    ("01", "card", card_roadmap, "01_roadmap", {}),
    ("02", "card", card_section1, "02_sec1", {}),
    ("02b", "card", card_rqs, "02b_rqs", {}),
    ("03", "doc", "lit_top", "03_lit_top", dict(part=PART[1], src=D, a=(.5, .5, 1), b=(.45, .62, 1.12))),
    ("04", "doc", "fig_positioning", "04_positioning", dict(part=PART[1], src="01-literature/figures/positioning.svg", fit=True, a=(.5, .5, 1), b=(.55, .8, 1.25))),
    ("05", "doc", "lit_closest", "05_closest", dict(part=PART[1], src=D, a=(.5, .5, 1), b=(.45, .45, 1.1))),
    ("06", "doc", "w2_glance", "06_w2_glance", dict(part=PART[1], src="02-practice-survey/README.md", fit=True, a=(.5, .5, 1), b=(.4, .38, 1.15))),
    ("08", "card", card_future_papers, "08_future", {}),
    ("09", "doc", "lit_mech", "09_mech", dict(part="Part 3 · Four suspected mechanisms (not found or partial in our searches)", src=D, a=(.5, .5, 1), b=(.42, .5, 1.1))),
    ("10", "doc", "lit_notclaim", "10_notclaim", dict(part=PART[3], src=D, a=(.5, .5, 1), b=(.48, .66, 1.12))),
    ("11", "card", card_caveat, "11_caveat", {}),
    ("12", "doc", "w3_targets", "12_targets", dict(part=PART[4], src="03-experiment/readiness.md §1.2", a=(.5, .5, 1), b=(.4, .5, 1.1))),
    ("13", "doc", "w3_replay", "13_replay", dict(part=PART[4], src="03-experiment/readiness.md §2", a=(.5, .5, 1), b=(.45, .5, 1.08))),
    ("14", "doc", "w3_arms", "14_arms", dict(part=PART[4], src="03-experiment/readiness.md §3", a=(.5, 0, 1), b=(.5, 1, 1), move=(0.12, 0.88))),
    ("15b", "card", card_cost, "15b_cost", {}),
    ("15g", "card", card_bench, "15g_bench", {}),
    ("15c", "card", card_contrast, "15c_contrast", {}),
    ("15d", "card", card_rq2, "15d_rq2", {}),
    ("15e", "card", card_worked, "15e_worked", {}),
    ("15h", "card", card_faults, "15h_faults", {}),
    ("15i", "card", card_coverage, "15i_coverage", {}),
    ("15f", "card", card_findings, "15f_findings", {}),
    ("17", "card", card_future, "17_future", {}),
    ("18", "card", card_close, "18_close", dict(hold=5.0)),
]
LEAD, TAIL = 0.4, 0.4


def wav_len(p):
    w = wave.open(str(p)); return w.getnframes() / w.getframerate()


def main():
    for sub in ("cards", "frames", "contact"):
        shutil.rmtree(OUT / sub, ignore_errors=True); (OUT / sub).mkdir(parents=True)
    clips, vo_at, t, contact = [], [], 0.0, []
    for sid, kind, arg, vo, kw in SEGMENTS:
        vlen = wav_len(OUT / "vo" / f"{vo}.wav")
        dur = max(kw.get("hold", 0), LEAD + vlen + TAIL)
        dur = round(dur * FPS) / FPS
        vo_at.append((t + LEAD, vo))
        if kind == "card":
            p = OUT / "cards" / f"{sid}.png"; arg().save(p)
            clips.append((p, dur)); contact.append((t, p, vo))
        else:
            page = page_for(OUT / "docs" / f"{arg}.png", kw.get("fit", False))
            m0, m1 = kw.get("move", (0.30, 0.30 + min(0.6, 7.0 / dur)))
            n = int(round(dur * FPS)); last_key, run_start, run_img = None, 0, None
            frames = []
            for i in range(n):
                u = min(max((i / n - m0) / (m1 - m0), 0), 1); e = ease(u)
                a, b = kw["a"], kw["b"]
                key = tuple(round(a[j] + (b[j] - a[j]) * e, 4) for j in range(3))
                if key != last_key:
                    frames.append([key, 1]); last_key = key
                else:
                    frames[-1][1] += 1
            for k, (key, cnt) in enumerate(frames):
                p = OUT / "frames" / f"{sid}_{k:04d}.jpg"
                framed(view(page, *key), kw["part"], kw["src"]).save(p, quality=90)
                clips.append((p, cnt / FPS))
                if k in (0, len(frames) - 1):
                    contact.append((t + sum(c for _, c in frames[:k]) / FPS, p, vo))
        t += dur
    total = t
    # VO mix: one mono 44.1 kHz 16-bit track
    sr = 44100; buf = bytearray(int(total * sr) * 2 + 2)
    for at, vo in vo_at:
        w = wave.open(str(OUT / "vo" / f"{vo}.wav")); assert w.getframerate() == sr and w.getsampwidth() == 2
        data = w.readframes(w.getnframes()); off = int(at * sr) * 2
        buf[off:off + len(data)] = data
    with wave.open(str(OUT / "mix.wav"), "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(bytes(buf))
    (OUT / "clips.txt").write_text("\n".join(f"{p}|{d:.3f}" for p, d in clips), encoding="utf-8")
    (OUT / "timeline.json").write_text(json.dumps({"total_s": total, "vo_at": vo_at, "clips": len(clips)}, indent=1))
    # contact sheets: 3x3 per sheet, labelled with time and VO id
    nar = {x["id"]: x["text"] for x in json.loads((VID / "narration.json").read_text(encoding="utf-8"))}
    for s in range(0, len(contact), 9):
        sheet = Image.new("RGB", (3 * 640, 3 * 420), (255, 255, 255)); dd = ImageDraw.Draw(sheet)
        for j, (tt, p, vo) in enumerate(contact[s:s + 9]):
            th = Image.open(p).resize((640, 360)); x, y = (j % 3) * 640, (j // 3) * 420
            sheet.paste(th, (x, y))
            dd.text((x + 6, y + 364), f"{int(tt // 60)}:{tt % 60:04.1f}  {vo}", font=F(SANSB, 18), fill=INK)
            dd.text((x + 6, y + 388), nar[vo][:70] + "\u2026", font=F(SANS, 15), fill=MUTED)
        sheet.save(OUT / "contact" / f"sheet_{s // 9 + 1}.png")
    print(f"total {total:.1f}s  clips {len(clips)}  contact frames {len(contact)}")


if __name__ == "__main__":
    main()
