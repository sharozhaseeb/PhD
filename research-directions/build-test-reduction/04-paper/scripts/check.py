#!/usr/bin/env python3
"""Consistency checks for the paper. Exit status 1 if any violation is found.

(a) every spec anchor is a literal substring of results.md (or findings.md for "KB:" anchors);
(b) generated/numbers.tex matches macro_spec.py;
(c) no bare numbers in the prose of main.tex and sections/*.tex (numbers must come from macros);
(d) every \\cite key exists in refs.bib;
(e) every spec macro used as \\Name{} exists in numbers.tex, and capitalised \\Name{} macros that
    are neither spec names nor defined in the paper are reported as undefined.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
from macro_spec import SPEC  # noqa: E402

RESULTS = ROOT / "03-experiment" / "results" / "results.md"
FINDINGS = ROOT / "knowledge-base" / "findings.md"
errors = []
_warn = []


def err(where, msg):
    errors.append("%s: %s" % (where, msg))


# ------------------------------------------------------------------ (a)
def check_anchors():
    r = RESULTS.read_text(encoding="utf8")
    k = FINDINGS.read_text(encoding="utf8")
    for name, val, kind, anchor, source in SPEC:
        if anchor.startswith("FILE:"):
            # FILE:<path relative to build-test-reduction>::<literal text> (W6: literature logs)
            rel, a = anchor[5:].split("::", 1)
            f = ROOT / rel
            if not f.exists() or a not in f.read_text(encoding="utf8"):
                err("macro_spec.py", "%s: anchor not in %s: %r" % (name, rel, a))
        elif anchor.startswith("KB:"):
            if anchor[3:] not in k:
                err("macro_spec.py", "%s: anchor not in findings.md: %r" % (name, anchor[3:]))
            a = anchor[3:]
        else:
            if anchor not in r:
                err("macro_spec.py", "%s: anchor not in results.md: %r" % (name, anchor))
            a = anchor
        # the value itself should occur inside its anchor (catches drift between value and anchor)
        shown = val.replace("e-", "e-")
        digits = re.sub(r"\D", "", shown)
        if digits and digits not in re.sub(r"\D", "", a) and shown not in a:
            # thousands separators and thin spaces are normalised by the digit comparison above;
            # derived values (ratios, counts) legitimately differ, so this is only a warning.
            _warn.append("warn: %s value %r not visible in anchor %r" % (name, val, a))


# ------------------------------------------------------------------ (b)
def tex_value(val):
    m = re.fullmatch(r"(\d+(?:\.\d+)?)e(-?\d+)", val)
    return r"\ensuremath{%s\times10^{%d}}" % (m.group(1), int(m.group(2))) if m else val


def numbers_defs():
    p = PAPER / "generated" / "numbers.tex"
    if not p.exists():
        err(str(p), "missing; run scripts/make_all.py")
        return {}
    defs = {}
    for i, line in enumerate(p.read_text(encoding="utf8").splitlines(), 1):
        m = re.match(r"\\newcommand\{\\([A-Za-z]+)\}\{(.*)\}$", line)
        if m:
            defs[m.group(1)] = m.group(2)
    return defs


def check_numbers(defs):
    names = set()
    for name, val, kind, anchor, source in SPEC:
        names.add(name)
        if name not in defs:
            err("generated/numbers.tex", "missing macro \\%s" % name)
        elif defs[name] != tex_value(val):
            err("generated/numbers.tex", "\\%s = %r but spec says %r" % (name, defs[name], tex_value(val)))
    for n in defs:
        if n not in names:
            err("generated/numbers.tex", "macro \\%s is not in macro_spec.py" % n)
    return names


# ------------------------------------------------------------------ LaTeX scanning helpers
def strip_comments(src):
    out = []
    for line in src.splitlines():
        # a % not preceded by a backslash starts a comment
        out.append(re.sub(r"(?<!\\)%.*$", "", line))
    return out


def blank(text, start, end):
    """Replace text[start:end] by spaces, keeping newlines so line numbers survive."""
    seg = re.sub(r"[^\n]", " ", text[start:end])
    return text[:start] + seg + text[end:]


def match_brace(t, i):
    """t[i] == '{' -> index after the matching '}' (or len(t))."""
    depth = 0
    n = len(t)
    while i < n:
        c = t[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return n


def strip_command_args(t, names, nargs=1, optional=True):
    """Blank commands in `names` together with optional [..] / (..) args and up to nargs {..} args."""
    pat = re.compile(r"\\(?:%s)\*?" % "|".join(names))
    pos = 0
    while True:
        m = pat.search(t, pos)
        if not m:
            return t
        i = m.end()
        # optional args and parenthesised args
        while True:
            while i < len(t) and t[i] in " \t":
                i += 1
            if optional and i < len(t) and t[i] == "[":
                j = t.find("]", i)
                if j < 0:
                    break
                i = j + 1
                continue
            if optional and i < len(t) and t[i] == "(":
                j = t.find(")", i)
                if j < 0:
                    break
                i = j + 1
                continue
            break
        for _ in range(nargs):
            while i < len(t) and t[i] in " \t\n":
                i += 1
            if i < len(t) and t[i] == "{":
                i = match_brace(t, i)
            else:
                break
        t = blank(t, m.start(), i)
        pos = m.start() + 1


def strip_envs(t, names):
    for n in names:
        pat = re.compile(r"\\begin\{%s\*?\}.*?\\end\{%s\*?\}" % (n, n), re.S)
        while True:
            m = pat.search(t)
            if not m:
                break
            t = blank(t, m.start(), m.end())
    return t


NUM_CTX = [
    # section / figure / table / appendix numbers
    r"(?:Section|Sections|Sec\.|Figure|Figures|Fig\.|Table|Tables|Tab\.|Appendix|Algorithm|Listing|Equation|Eq\.|Theorem|Lemma|Proposition|Definition)s?~?\s*\d+(?:\.\d+)*",
    r"\\S\s*\d+(?:\.\d+)*",
    # slowdown ids and issue-like references
    r"\\#\s*\d+",
    # lengths
    r"-?\d*\.?\d+\s*(?:\\(?:linewidth|textwidth|columnwidth|textheight|baselineskip|paperwidth|hsize)|pt|em|ex|cm|mm|in|bp)(?![A-Za-z])",
    # years
    r"\b(?:19|20)\d\d\b",
    r"(?<![\w.])\(\d{1,2}\)",  # enumeration markers (1) (2)
]
NUM_CTX += [
    r"\b[Ss]teps?~?\d+(?:\s*(?:--|-|and|to)\s*\d+)?", r"\b[Ss]tates?~?\d+",
    r"\b[A-Za-z][A-Za-z0-9]*-[A-Za-z]*\d+[A-Za-z]*\b",   # i5-12400F, S2-S10
    r"\b(?:Ubuntu|Python|CPython|WSL|Linux|Windows|pytest|NumPy|SciPy|asv|GCC|gcc|clang|Java)\s*v?\d+(?:\.\d+)*",
]
NUM_CTX_RE = re.compile("|".join(NUM_CTX))
# applied after macro names are blanked (a macro such as \pct may sit between the number and its noun)
POST_CTX_RE = re.compile(r"Wilson\s+95\b|\b95\s*(?:\{\})?\s*(?=CI|confidence|interval)")


def lint_digits(path, rel):
    raw = path.read_text(encoding="utf8")
    lines = strip_comments(raw)
    t = "\n".join(lines)
    if "\\begin{document}" in t:
        i = t.index("\\begin{document}")
        t = blank(t, 0, i)
    # environments that are not prose
    t = strip_envs(t, ["tikzpicture", "thebibliography", "verbatim", "lstlisting", "equation", "align", "eqnarray",
                       "displaymath", "gather", "multline", "filecontents"])
    t = re.sub(r"\\\[.*?\\\]", lambda m: re.sub(r"[^\n]", " ", m.group(0)), t, flags=re.S)
    # commands whose arguments are keys, files, lengths or layout
    t = strip_command_args(t, ["cite[A-Za-z]*", "ref", "eqref", "autoref", "cref", "Cref", "pageref", "nameref", "label",
                               "includegraphics", "usepackage", "RequirePackage", "documentclass", "input", "include",
                               "bibliography", "bibliographystyle", "url", "href", "hyperref", "newcommand", "renewcommand",
                               "providecommand", "def", "DeclareMathOperator", "definecolor", "setlength", "addtolength",
                               "setcounter", "addtocounter", "geometry", "hypersetup", "vspace", "hspace", "vskip", "hskip",
                               "captionsetup", "lstset", "pgfplotsset", "tikzset", "usetikzlibrary", "usetikzlibrary",
                               "newtheorem", "theoremstyle", "setcitestyle", "pagestyle", "linespread", "tabcolsep",
                               "arraystretch", "colorlet", "newcolumntype", "graphicspath", "bibliographystyle"], nargs=3)
    t = strip_command_args(t, ["begin", "end"], nargs=1)
    t = strip_command_args(t, ["multicolumn", "multirow"], nargs=2)
    t = strip_command_args(t, ["cline", "cmidrule", "toprule", "midrule", "bottomrule", "hline"], nargs=1)
    # \TODO{...}
    t = strip_command_args(t, ["TODO", "todo", "FIXME"], nargs=1)
    # code-like spans: contents are identifiers, SHAs, quoted commit subjects
    t = strip_command_args(t, ["texttt", "verb", "code", "path", "lstinline", "file"], nargs=1)
    # contexts that legitimately contain digits (before macro names are blanked: lengths use \linewidth)
    t = NUM_CTX_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), t)
    # \Name{} number macros and other macro names
    t = re.sub(r"\\[A-Za-z@]+\*?", lambda m: " " * len(m.group(0)), t)
    t = POST_CTX_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), t)
    # inline math: formula constants such as 1+3\sigma are fine; decimals and 3+ digit numbers are results
    def math_ok(m):
        s = re.sub(r"[_^]\{?\d+\}?", lambda k: " " * len(k.group(0)), m.group(0))
        s = re.sub(r"(?<![\d.])\d{1,2}(?![\d.])", lambda k: " " * len(k.group(0)), s)
        return s
    t = re.sub(r"(?<!\\)\$[^$\n]*\$", math_ok, t)
    # identifiers such as RQ1, A4, S12, k2 (digits glued to a preceding letter) and hex-like tokens
    for ln, line in enumerate(t.splitlines(), 1):
        for m in re.finditer(r"(?<![A-Za-z_\\])\d[\d.,]*", line):
            tok = m.group(0)
            # allow a leading letter glued: handled by the lookbehind
            ctx = line.strip()
            err("%s:%d" % (rel, ln), "bare number %r in prose: %s" % (tok.rstrip(".,"), ctx[:90]))


def tex_files():
    fs = []
    m = PAPER / "main.tex"
    if m.exists():
        fs.append(m)
    s = PAPER / "sections"
    if s.exists():
        fs += sorted(s.glob("*.tex"))
    return fs


# ------------------------------------------------------------------ (d),(e)
def bib_keys():
    p = PAPER / "refs.bib"
    if not p.exists():
        return None
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", p.read_text(encoding="utf8")))


def check_cites_and_macros(files, names, defs):
    keys = bib_keys()
    defined = set()
    for f in files:
        raw = "\n".join(strip_comments(f.read_text(encoding="utf8")))
        defined |= set(re.findall(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)", raw))
        defined |= set(re.findall(r"\\(?:def|DeclareMathOperator|providecommand)\s*\{?\\([A-Za-z]+)", raw))
    std = {"TODO", "Cref", "Section", "Figure", "Table", "Appendix", "LaTeX", "TeX", "Large", "Huge", "LARGE", "Bigg",
           "Big", "S", "P", "L", "Gamma", "Delta", "Theta", "Lambda", "Pi", "Sigma", "Phi", "Psi", "Omega", "Re", "Im",
           "Pr", "Alph", "Roman", "Vert", "Updownarrow", "Rightarrow", "Leftarrow", "Leftrightarrow", "Downarrow",
           "Uparrow", "Longrightarrow", "Cap", "Cup", "Join", "Box", "Diamond", "Bbbk", "Finv", "Game"}
    for f in files:
        rel = f.relative_to(PAPER).as_posix()
        raw = "\n".join(strip_comments(f.read_text(encoding="utf8")))
        for ln, line in enumerate(raw.splitlines(), 1):
            for m in re.finditer(r"\\(?:cite(?!needed)[A-Za-z]*|parencite|textcite|autocite)\*?\s*(?:\[[^\]]*\]\s*)*\{([^}]*)\}", line):
                for k in [x.strip() for x in m.group(1).split(",") if x.strip()]:
                    if keys is None:
                        err("%s:%d" % (rel, ln), "\\cite{%s} but refs.bib does not exist" % k)
                    elif k not in keys:
                        err("%s:%d" % (rel, ln), "\\cite key %r missing from refs.bib" % k)
            for m in re.finditer(r"\\([A-Z][A-Za-z]*)(?![A-Za-z])(\s*\{\})?", line):
                n = m.group(1)
                # W6: also catch number-style macros used without {} (e.g. \Name\x);
                # only IEEEtran's own commands are skipped.
                if n.startswith("IEEE"):
                    continue
                if n in names:
                    if n not in defs:
                        err("%s:%d" % (rel, ln), "macro \\%s{} not in numbers.tex" % n)
                elif n not in defined and n not in std:
                    err("%s:%d" % (rel, ln), "undefined number-style macro \\%s{} (not in macro_spec.py or defined in the paper)" % n)


def main():
    check_anchors()
    defs = numbers_defs()
    names = check_numbers(defs) if defs else {n[0] for n in SPEC}
    files = tex_files()
    for f in files:
        lint_digits(f, f.relative_to(PAPER).as_posix())
    check_cites_and_macros(files, names, defs)
    if not files:
        print("note: no main.tex or sections/*.tex yet; digit lint and cite checks skipped")
    for e in errors:
        print("VIOLATION " + e)
    if _warn and "-v" in sys.argv:
        print(chr(10).join(_warn))
    print("%d violation(s); %d derived values not literally visible in their anchor (-v lists)" % (len(errors), len(_warn)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
