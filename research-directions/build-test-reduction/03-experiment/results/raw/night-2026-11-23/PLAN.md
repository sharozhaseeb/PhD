# Night queue 2026-11-23 → 24 — pre-registered plan (amendment to the night-1 plan; PM ruling 06:32)

Written 06:31–06:36 PKT on 23 Nov (real file times), before any night-2 measurement. Analysis frozen in `scripts/night2_analyse.py`. Driver: `scripts/night2_nx.py`. Queue: `scripts/wsl/night2_queue.sh`. Case lists: `frozen/night-2026-11-23.cases.json`. sha256 of all of these in `frozen/FROZEN.md`.

**Why:** E3 tier 2 found 11 of 499 off-target non-"same" verdicts (2.2 %). In every A/B run so far, base ran in `nx-slow-A` and slow in `nx-slow-B`, so the edit and the clone directory are fully confounded. The 4 "faster" flips cannot come from an edit that only adds work (results.md "E3 tier 2").

## Items, in order

| # | Item | Design | Cap | Estimate |
|---|---|---|---|---|
| 1 | **Directory A/A** (decisive confound test) | identical code (slowdown #3's state `e773a6af`, unpatched) in `nx-slow-A` (label A) and `nx-slow-B` (label B); **the same 168 cases and design as tier-2 block t2_03** (2 × 3, 2 repeats, order rotated) | **2.5 h** | 1.2–2.2 h (t2_03 took 2 h 10 min including gate waits) |
| 2 | **E5 setup-cached** (plan `raw/networkx/bench/setup_cached/plan.md`, frozen 16:52 on 22 Nov) | STD, CACHED, STD, CACHED, STD, CACHED at S0. **Both arms in the same directory (`nx-slow-A`)**, so no directory confound arises, and a swap is not applicable (there is no A/B within an arm). CACHED = `bth.benchrun measure-cached`, 6 values per case. | **3 h** (plan said 2.5 h; raised because tonight's (d) STD passes took 20–50 min each) | 1.3–2.8 h |
| 3 | **E3 tier-2 resume, with DIRECTORY SWAP** | **#8 started fresh** (the fixed-directory partial `repeat/t2_08.partial.jsonl` is archived, not mixed in), then #1. Repeat 0: base@A, slow@B, base first. Repeat 1: base@B, slow@A, slow first. 2 × 3, the frozen tier-2 case sets (170 each). | **until the hard stop 06:25** | #8 ≈ 1–2 h; #1 ≈ 1–3 h |

- **Caps total:** 5.5 h for items 1–2, plus item 3 until 06:25.
- **Start:** a detached waiter starts the queue **not before 21:00 PKT on 23 Nov** (TPM rule: timing at night). The block gate and the per-run gate then apply as on night 1.
- **Window:** 21:00 → 06:25 = 9.4 h. If the gates are kind, all of items 1–2 and most of item 3 fit. The PM can move the start time.
- **Rules unchanged from night 1:** the block gate (3 × 60 s); the per-run gate (≤ 10 min postponement, then `ok = False`); per-run checkpoints (per module for CACHED); detached stall watchers (stall 450 s, and 900 s for E5); the gate-wait alarm; telemetry; hard stop 06:25. Amendments 1–4 of night 1 apply.

## Pre-registered analysis (code: `scripts/night2_analyse.py`)

**Directory A/A:**
- Per case: the pooled 12 v 12 exact-MWU asv verdict, B vs A, and the per-repeat ratios.
- **Rate:** non-"same" / complete, with Wilson 95 %, compared with t2_03's 6 of 166.
- **Recurrence** of the 6 t2_03 flips (slow ran in B): a flip recurs if the directory-A/A ratio B/A lies on the same side of 1 **and** |log ratio| ≥ half of the t2_03 |log ratio|.
- **Decision:**
  - **bias SUPPORTED** if ≥ 4 of 6 recur, or the Wilson lower bound of the rate exceeds 0.5 %;
  - **bias NOT SUPPORTED** if ≤ 1 of 6 recur **and** ≤ 1 non-"same" verdict;
  - otherwise **INCONCLUSIVE**.

**E5:** as its frozen plan, using the median STD and median CACHED pass totals, the CACHED split (import, setup, calibration, warm-up, loops, other), and the sample-shift count outside [0.8, 1.25].

**E3 resume:**
- Agreement with the original verdict, exact test primary.
- A non-"same" verdict whose two repeat ratios (slow in B, then slow in A) differ in sign is flagged **directory-inconsistent**.

## Q3 (PM): did the earlier A/A use two directories, and why did the bias not show?

- **Yes: two directories.** The 23-case S0 A/A (`raw/networkx/bench/aa/raw_runs.json`) ran label A in `nx-slow-A` and label B in `nx-slow-B` for every run. The (b) A/A did the same.
- **Why no bias showed:** that design could hardly show a ≈ 2 % per-case rate.
  - 0 of 46 per-repeat verdicts is consistent with 2.2 % (P(0) ≈ 0.36).
  - It covered only 2 of the 11 flipped cases, and at S0, not at #3's, #4's or #2's states.
  - 4 of its 23 cases did exceed ±10 % in one repeat.
  - If the bias is state- or layout-specific (different files at each state), an S0 A/A cannot detect it at the other states.
- That is why item 1 runs at #3's state, on #3's exact case set.

## What the results can claim

- **Item 1** decides only whether a directory effect exists **at #3's state, on these cases**. It does not establish the source of #2's or #4's flips.
- **Item 3's** swap makes any remaining off-target flag directory-balanced. It does not remove per-repeat process noise.
- **E5** is a cost lower bound for a suite with module-level setup caching, not an asv replacement.
