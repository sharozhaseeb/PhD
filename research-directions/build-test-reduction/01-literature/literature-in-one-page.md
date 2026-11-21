# Study 1 literature in one page

*W1-LIT v3.2, 21 Nov 2026.*

**Evidence boundary.** A targeted primary-source review, not a systematic one. It covers 138 references and 72 open-access PDFs, and includes ACM DL and IEEE Xplore searches (123 records screened). Every claim is labelled in `review.md`.

**The question.** When code is optimized through many small edits, can each edit be validated with a *reduced* build and a *reduced* test and benchmark set chosen by deterministic rules, and still be trusted?

**What the literature says.** Every reduction technique is safe only under stated assumptions:
- incremental builds need complete dependencies [Mokhov et al. JFP 2020 §3.6];
- regression test selection needs "controlled regression testing" and fresh dependency data [Rothermel & Harrold 1997; Ekstazi §5];
- benchmark selection needs performance effects to stay where the coverage is.

The backstop in industry is a periodic or final full run (Google, Meta).

## Four mechanisms Study 1 measures

| | Where existing reduction may become unsafe for optimization edits | Basis | Searched? |
|---|---|---|---|
| **C5** | **C-extension boundary.** coverage.py sees Python lines only, so edits to C or Cython are invisible to testmon-style selection. | PerfAgent §VI names it as a hole; RTSLinux (FSE'17) and Elsner (ICSE-SEIP'22) are non-Python analogues; Kauhanen (SANER'21) measures pure-Python RTS misses. | No Python measurement found. |
| **C7** | **Stale dependency data.** Reduced runs refresh only the tests that ran, so dependency maps age over a chain of edits. | Ekstazi §3.3, §5. Chittimalli & Harrold (TSE 2009): outdated coverage harms selection for one version step. | Partial: no measurement as the refresh interval grows over edits. |
| **C11** | **Dropped benchmarks.** Covering the change is not enough: 74–77% of covering tests show no known speed-up (Ding, ICSE'20). Reduced suites miss trends (Grambow, TCC). | The literature mostly *orders* benchmarks. | No per-edit miss rate for Python. |
| **C8** | **Incremental rebuilds.** setuptools and Cython rebuild by file timestamps and ignore flag and directive changes. | Their source code; C/C++ studies (Licker ICSE'19, BuildFS OOPSLA'20). | No Python-extension study found. |

**The RQ3 policy follows from these.** It has three parts:
- one rule per mechanism: native fallback, refreshing dependency and profile data, profile-based benchmark selection plus a fixed sentinel set, and a clean-vs-incremental check;
- a full check when accumulated change crosses a threshold;
- a cap at k edits.

## Five closest works

1. **PerfAgent** (arXiv 2607.19653, 2026; read in full). An LLM optimization loop that runs testmon-selected tests on every iteration (for example 109 of 34,458 numpy tests). It never runs the full suite, reports no misses, and names the native-extension hole.
2. **NameRTS** (arXiv 2605.25356, 2026). Python RTS at name level: −45.6% time, safe on 99.6% of commits. It excludes commits that change only non-Python files. Code is public (a replication package); it is planned as a comparator after the meeting.
3. **Sayedsalehi et al.** (arXiv 2604.00222, 2026, Mozilla; read in full; see also Bavand & Rigby, ICSME'21, dynamic batching from failure history). Batches performance tests and flushes a batch when a *learned* cumulative risk sum passes a threshold. **Our full-check trigger is a model-free variant of this.**
4. **Fallahzadeh, Rigby, Adams** (EMSE 2025; read in full). Compares selection with variable-size batching at scale: selection misses up to 55% of failures. Combining the two is left as future work.
5. **Ekstazi / pytest-testmon** (ISSTA'15 / tool). The baseline selectors; per-revision, Python-lines-only for testmon.

## What we do NOT claim

- A better test selector.
- Per-edit test selection in optimization loops (PerfAgent).
- A two-sided "faster and no regression" gate (SemOpt, PerfAgent).
- Periodic full runs (Meta, Google).
- Batching, bisection, or variable and risk-based batch size (Ericsson, Fallahzadeh, Sayedsalehi).
- Comparison with a stable baseline (MongoDB).
- Culprit finding (deferred).
- Any novelty beyond "not found in our recorded searches".

**Claim C1, as narrowed.** We found no evaluation of a model-free accumulated-change trigger on top of a per-edit reduced check, for chains of dependent edits, compared with fixed-k batching at matched cost.

*Details:*
- `README.md`
- `closest-works.md` (20 works)
- `beyond-literature-claims.md`, which gives each claim's search and the W3 evidence it needs
- `figures/positioning.svg`
