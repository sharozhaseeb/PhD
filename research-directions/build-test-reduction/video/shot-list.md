# W5-VIDEO shot list: Study 1 research walkthrough (Gate 1)

**Status:** v2, 2026-11-21. Provisionally approved by the PM; v2 applies the advisor-persona deltas (beats 2b, 6 merged with 7, 9 retitled, 15b added, 16 relabelled). Audience: the owner (PhD student), as a catch-up before the advisor meeting. Not a client demo.

**Format.** No app to demo, so every visual is a real repo artefact:
- repo Markdown files rendered to HTML with a plain stylesheet and screenshotted by headless Edge (`build/render_docs.py`);
- the real `01-literature/figures/positioning.svg`;
- simple slide cards drawn with PIL (title, section cards, quote cards, results charts plotted from raw files in `03-experiment/results/`).

Every document shot carries a footer with its repo path. Gentle zooms are done as slow crops of the same still (no invented content).

**Tooling (adapted, no downloads).**
- No ffmpeg is installed (only Playwright's VP8-only stub). The MP4 is rendered with Windows' built-in `Windows.Media.Editing.MediaComposition` (H.264/AAC 1080p), tested OK.
- `OPENAI_API_KEY` is not set, so the voice is the stock offline Windows voice (System.Speech, "Microsoft Zira Desktop").
- Large intermediates live in `C:\Users\pc\study\bt-lab\video\`. Build scripts live in this folder.

**Length target:** about 6.5 min (owner allowed 5–8).

## Beats

| # | Part | Beat | Visual (source file) | Post | Target |
|---|---|---|---|---|---|
| 0 | — | Title | Card: "Study 1: reduced build and test validation for iterative code optimization", subtitle "Research walkthrough, 21 Nov 2026" | — | 8 s |
| 1 | — | Roadmap | Card: the five parts | — | 12 s |
| 2 | 1 | Section card + the question | Card: "1 · What the literature says"; the question from `01-literature/literature-in-one-page.md` | — | 12 s |
| 2b | 1 | Research questions (revised) | Card from `pm/CHARTER.md` "Research questions — revised" (text parsed from the file) | — | 25 s |
| 3 | 1 | Evidence boundary + the three assumptions | Screenshot `01-literature/literature-in-one-page.md` (top) | slow zoom to "What the literature says" | 35 s |
| 4 | 1 | Positioning figure | `01-literature/figures/positioning.svg` | slow zoom | 25 s |
| 5 | 1 | Five closest works | Screenshot `literature-in-one-page.md` "Five closest works" | pan down | 35 s |
| 6 | 1 | How optimizers validate each candidate (W2), merged with the headline | Screenshot `02-practice-survey/README.md` at-a-glance table | slow zoom | 30 s |
| 8 | 2 | Future work the papers themselves state | Quote card, each row with its source note: PerfAgent §VII (native-extension coverage; `notes/R1`); Fallahzadeh 2025 p.54 (combining selection and batching; `notes/R2`); Ekstazi §3 (formal safety proof; `notes/T2`); Kotinos future-work section (preconditions; `notes/T1`); agentic survey §7.3 (program-analysis RTS not integrated; `closest-works.md` #20). Quotes ≤15 words, as in the notes. | — | 45 s |
| 9 | 3 | Four suspected mechanisms (not found or partial in our searches); taken from W1 v3.2 (C7 partial) | Screenshot `literature-in-one-page.md` mechanisms table (C5, C7, C11, C8) | zoom per row | 40 s |
| 10 | 3 | C1 narrowed + what we do NOT claim | Screenshot `literature-in-one-page.md` "What we do NOT claim" + "Claim C1, as narrowed" | — | 30 s |
| 11 | 3 | Search caveat | Card: targeted review, not systematic; ACM DL and IEEE Xplore searched (count parsed from `gap-and-search-log.md`); no Scopus / Web of Science; forward citations only for PerfAgent and NameRTS | — | 15 s |
| 12 | 4 | Experiment design: targets + replay | Screenshot `03-experiment/readiness.md` §1.2 targets and §2 replay | pan | 30 s |
| 13 | 4 | Arms compared | Screenshot `03-experiment/readiness.md` §3 arms table | pan | 35 s |
| 14 | 4 | Safety and timing rules | Screenshot `03-experiment/rules.md` / readiness §4–5 (asv rule, k of N with Wilson CI, estimated seconds) | — | 25 s |
| 15b | 4 | Cost (RQ1) | Per-edit chart of build vs tests vs benchmarks from `results/rq1_cost.csv`. If absent at render time: card "cost measurement running", no numbers (plus the worked edit if `results/worked-edit.md` exists) | — | 15–40 s |
| 16 | 4 | Status: **data preparation, not results** (mining counts, provisional smoke run) | Cards/charts plotted from files in `03-experiment/results/` at render time, filename on screen. At v1 only `results/raw/networkx_mining_subject_rule.txt` exists (110 subject matches, 101 qualifying, latest 20 frozen). Re-rendered when W3 posts draft results. | "Preliminary" pill | 25–60 s |
| 17 | 5 | Future work | Card: W1 open items (citation screening; Chittimalli & Harrold full text); NameRTS as post-meeting comparator; scikit-learn cost-only measurement; cap-only and additive-budget baselines; the later AI-based selection study | — | 30 s |
| 18 | — | Close | Card with disclosure | — | 8 s |

## Honesty notes

- Every number on screen appears verbatim in the named file; the Gate 2 critic checks each against its file.
- Part 4 shows only what exists in `03-experiment/results/` at render time, labelled **PRELIMINARY** if partial, and says what is still running.
- No novelty beyond "not found in our recorded searches"; the narration states the C1 concession (model-free variant of risk-mass batching, Sayedsalehi 2026).
- Closing card: "Narration is synthetic; documents and analyses were prepared with AI assistance and reviewed by the student." No house disclosure found in `pm/advisor/persona.md`.
- No personal details on screen (no name, roll number or email). Paper authors appear only as citations.

## Decisions for the PM

1. Encoder: Windows built-in MediaComposition instead of ffmpeg (no download). Loudness normalisation is not available; the stock voice is rendered at a fixed level.
2. Zooms are stepped crops at about 10 fps (smooth enough at the slow speeds used).

## Build record

- Scripts: `build/render_docs.py` (doc screenshots), `build/tts.ps1` (voice, rate +2), `build/build_video.py` (cards, frames, VO mix, contact sheets), `build/compose.ps1` (MP4), `build/verify.ps1` (decode check).
- Rebuild: `python build/render_docs.py; python build/build_video.py; compose.ps1 -Clips ...\clips.txt -Audio ...\mix.wav -Out ...\study1-walkthrough-vN.mp4`.
- Results and cost cards parse their numbers from `03-experiment/results/` at build time (`results_facts.json` is written next to the frames).

## v9 (2026-11-21, owner's version): Part 4 as rendered

Order after beat 14 (arms): 15b RQ1 test cost chart (all 19 states; S16 noisy, S17 borderline) → 15g benchmark dominance (lower bound, 40–180×) → 15c build-share contrast and the iterators.h historical upstream bug → 15d RQ2 end-to-end cost per arm (headline of record: results.md end-to-end column) → 15e worked edit at step 10 (test counts only) → 15h fault detection on the frozen mutants (N = 20, with the honest reading) → 15f draft findings plus a PENDING box (latent faults, slowdown detection, benchmark selection, measured benchmark pass) → 17 future work, opening with the segue "benchmark selection is where a policy can matter most".

Dropped for length: the readiness §4.4/§5 reporting-rules doc beat and the separate data-prep card.

Every Part 4 number is parsed from `03-experiment/results/` at build time; the parsed values are written to `bt-lab/video/*_facts.json`.

## v11 (2026-11-22, final results): Part 4 rebuilt

Story order (PM, 15:03): 15r1 R1 cost → 15b1 B1 coverage (18-step strip, 9/15 true optimizations) → 15pw oracle power (slowdown oracle, A/A, profile completeness) → 15t1 testmon (T1) → 15a4 A4 negatives → 17 future work led by A13 (pre-registered B1 replication first).
Every Part 4 card asserts at build time that each number it shows appears verbatim in `03-experiment/results/results.md` (A13 wording: `meeting-2026-11-advisor/01-agenda-and-asks.md`). Superseded figures (≥ 0.9 h, 40–180×, bottleneck 22 %, "most", "10×") no longer appear.
