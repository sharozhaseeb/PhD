# Study 1 paper: numbers and figures pipeline

Every number in the prose comes from `generated/numbers.tex` (`\Name{}` macros), which
`scripts/make_all.py` computes from the raw files under `../03-experiment/results/`
and checks against `scripts/macro_spec.py`. Figures are vector PDFs in `figures/`.

## Reproduce

    python scripts/make_all.py              # verify input sha256 vs data-manifest.yaml, recompute, write numbers.tex + figures
    python scripts/make_all.py --manifest   # after reviewing changed inputs: regenerate data-manifest.yaml
    python scripts/check.py                 # anchors, numbers.tex vs spec, digit lint of sections/*.tex, \cite keys, macros

Make: `make all | check | manifest`. Windows: `.\build.ps1 [all|check|manifest]`.
Needs Python 3 with numpy and matplotlib only (no scipy; Wilson CIs use z = 1.959964).
`make_all.py` exits non-zero and does not write `numbers.tex` if a computed value differs from the spec
(`--allow-mismatch` writes the spec values anyway, still exit 1; do not use it for a release).
Nothing here runs a benchmark, timing run or test: it only reads JSON and CSV.

## Rules

- Add a macro only via `scripts/macro_spec.py` (name, value, kind, anchor, source). Anchors are literal
  substrings of `results.md` (or `findings.md`, prefix `KB:`); `check.py` fails if they disappear.
- Do not type numbers in `main.tex` or `sections/*.tex`; `check.py` fails on bare numbers.
- Inputs listed in `data-manifest.yaml`. Overnight folders not yet written up are deliberately not read.

## PDF build

Toolchain: Tectonic 0.17.0 (XeTeX engine) in its own conda env, owner-approved 2026-11-22. Call it by full path; do not activate or change the env.

    python scripts/make_all.py --pdf        # numbers + figures, then check.py, then Tectonic -> build/main.pdf

Equivalent by hand:

    C:\Users\pc\miniconda3\envs\tectonic\Library\bin\tectonic.exe -X compile main.tex --outdir build --keep-logs

`--pdf` fails if `check.py` fails, if Tectonic fails, or if the log has any overfull box or any undefined citation or reference.
Set `$TECTONIC` to use another binary. Under pdfLaTeX (`latexmk -pdf main.tex`) the preamble falls back to T1 Times.
Compile only when needed: another workstream runs timing jobs on this machine.
Bibliography provenance notes are in the `annote` field of `refs.bib`, which IEEEtran does not print.
