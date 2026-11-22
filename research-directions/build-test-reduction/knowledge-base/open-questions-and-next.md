# Open questions and next steps

Last updated 2026-11-22 ~06:12 PKT (after the critic pass, D18–D20 and the item-1 write-up).

## Pending work (W3)

| Item | State | Source |
|---|---|---|
| Powered out-of-reach spot-check re-run (≥ 5 processes, ≥ 15 vs 15 samples) | **Approved (D18), pending**: idle gate must postpone, not label; 1.5 h cap. Until it runs there is no reach-safety evidence (S3 withdrawn) | [decisions](decisions.md) D18; [results](../03-experiment/results/results.md) "Safety of reach-based selection" |
| M5 gate fix: postpone instead of label; also gate on Windows CPU | Needed: item 4 and all item-1 re-runs started above the gate; the 3.7× benchmark-cost spread is likely host load (R4) | [LABELS](../03-experiment/results/raw/networkx/bench/LABELS.md); [results](../03-experiment/results/results.md) "RQ1 headline", "RQ1 — idle re-timing" |
| Meeting pack and video: replace 40–180× / 19× / 22 % / 4× / spot-check figures | W4 asked 06:10 (meeting pack); video not yet asked | [WORKLOG](WORKLOG.md) 06:10; [03-results-summary](../meeting-2026-11-advisor/03-results-summary.md) |
| Benchmark A/A noise floor | Not run, not queued. Without it no speed-up or regression claim can be shown (TPM rule) | [readiness](../03-experiment/readiness.md) §5; [03-results-summary](../meeting-2026-11-advisor/03-results-summary.md) |
| Oracle repeatability (≥ 3 interleaved re-runs) | Not run. Would settle #1 and the `nanmin` outlier | [readiness](../03-experiment/readiness.md) §5 |
| Per-arm regression simulation | Not run | [results](../03-experiment/results/results.md) |
| Checkpoint re-profiling (S3, S5, S8, S13) | Not run; A4 selects all benchmarks without it (B2) | [results](../03-experiment/results/results.md) |
| C5 cap-only and additive-budget comparators; T ∈ {5, 20}; k ∈ {2, 8} | Not run | [rules](../03-experiment/rules.md) §6 |
| NameRTS comparator | Not run; post-meeting | [W1 README](../01-literature/README.md) |
| Caller faults (class 2); real testmon runs with mutants | Not run | [readiness](../03-experiment/readiness.md) §4.1b; [results](../03-experiment/results/results.md) |
| B4 fix (same path or `-ffile-prefix-map`) and re-validation | Post-meeting | [hazard](../03-experiment/results/build-hazard-iterators-h.md) §1 |
| Diagnose the missing prerequisite for `98b59df2`; recover bottleneck states 9–13 | Not done; main bottleneck result uses states 1–8 meanwhile (D19) | [hazard](../03-experiment/results/build-hazard-iterators-h.md) §4 |
| Bottleneck worked edit (shows a reduced build) | Not in any file | [03-results-summary](../meeting-2026-11-advisor/03-results-summary.md) S4 |
| scikit-learn cost-only measurement | Not reported | [readiness](../03-experiment/readiness.md) §8 |
| Follow-up commit of uncommitted work (W3 README, `scripts/wsl/`, overnight results) | Needs the owner's yes | transcript; `git status` |

## Asks for the advisor meeting (about 2026-11-23/24)

From [agenda and asks](../meeting-2026-11-advisor/01-agenda-and-asks.md). "Our position" is not an advisor decision; no advisor decision is recorded anywhere.

| # | Question | Our current position |
|---|---|---|
| A1 | Language / project type | Python plus compiled extensions (networkx + bottleneck) |
| A2 | Source of edit sequences | Mined historical perf commits, replayed in order |
| A3 | Definition of "stays optimized" | asv rule vs original and previous state, above the noise floor |
| A4 | Acceptable safety | "k of N missed" with Wilson CI; no general safety claim |
| A5 | What the contribution is | Lead with where reduction becomes unsafe (C5, C7, C11, C8) |
| A6 | Pilot scope | Two repos; networkx-only pilot fallback |
| A7 | NameRTS as a required baseline? | After the meeting |
| A8 | Replay limitation acceptable? | Accept as stated (threat T1) |
| A9 | Hand-over to Study 2 (AI) | Undecided |
| A10 | Venue and timeline | UNKNOWN |
| A11 | SPARK fit | UNKNOWN |
| A12 | Compute | Laptop only |
| **A13** | **Pivot toward benchmark coverage of optimization edits (B1)?** Functional selection looks solved by testmon on this data | Options: pivot; keep RQs and add B1 as a finding; wait for slowdown results |

**New evidence for A13 since the pack was written (2026-11-22):** the slowdown oracle shows FULL detects only 2–3 of 10 frozen slowdowns, and 5 of the 7 misses have no reaching benchmark at all ([findings](findings.md) S1–S4). This strengthens the B1 case. The meeting pack's results summary predates this and still says slowdowns are pending ([03-results-summary](../meeting-2026-11-advisor/03-results-summary.md)).

Other items the pack should now mention (inferred from the new results): the stale-binary false pass as a replay-artefact hazard mechanism and rule B0 (H1, D20); B4 invalid (H3); bottleneck main result = amended window states 1–8, 5-edit replay a sensitivity row (D19); benchmark pass 659–2444 s, median ≈ 730 s, 8–28× (R1, R4); bottleneck build ≈ 16–18 % (R2); testmon 3.5–4× (T1); spot check withdrawn, no reach-safety evidence yet (S3, D18).

## Open research questions

- Can benchmark coverage of optimization edits be measured and improved deterministically (for example by generating or selecting workloads that reach the edited function)? Raised by B1 and A13 (inferred direction; not yet in any plan file).
- Does the accumulation component matter on any subject with latent faults? networkx has none (0/5).
- Does C5 (native-extension blind spot of coverage-based RTS) produce real misses? Not yet measured; bottleneck tests were not run under testmon.
- Is the asv-rule verdict stable enough to count misses (oracle repeatability)?
- Is reach-based benchmark selection safe out of reach? Unknown: the first spot check had no power (S3); the D18 re-run should answer it for the 5 slowdowns with cases outside static reach.
- What drives the ≈ 3.7× spread in benchmark-pass cost under one protocol (R4)? Host-side load is inferred, not measured.

## Future work named in the literature

See [research](research.md) "The literature's own stated future work": native-extension coverage for selective testing (PerfAgent); combining selection with batching (Fallahzadeh et al.); a safety proof for Ekstazi.

## Out of scope for Study 1

AI-based selection (later study); culprit finding (C10, deferred); recorded optimizer sessions (A8).
