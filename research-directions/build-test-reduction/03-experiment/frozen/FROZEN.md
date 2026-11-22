
## networkx fault candidates (frozen by scripts/gen_faults.py, seed 20261121)
Sites available per step: mutants [40, 47, 20, 7, 13, 9, 23, 10, 37, 4, 10, 8, 13, 4, 81, 2, 30, 5], slowdowns [2, 2, 1, 2, 3, 1, 0, 6, 2, 1, 2, 3, 1, 0, 2, 0, 1, 1].
Chosen: 25 mutants, 10 slowdowns (round-robin over steps).
- `networkx.mutants.json` sha256 `a6da4e85d21ebb3ca0d6c62c1a507bde89587a9f07fbc2f12b6c410ba180b19e`
- `networkx.slowdowns.json` sha256 `d45efd3774a775dcd73707138996b6110aaeca1d54dd9e5d585e6f17689047aa`

## networkx slowdown out-of-reach spot-check sample (seed 20261121, 10 of 171)
- `networkx.slowdown_spotcheck.json` sha256 `4ab9b51bc081c73e9d6853ce96be7f40f27b187a5cabb9f798e254098e6dfffd`

## A/A noise-floor sample (Q2, PM 2026-11-22 06:27)

- **File:** `networkx.aa_noise_sample.json`, sha256 `8cb74ff95a5ee2eab8f1eae189eaeb547d8ff04753b19b88d25e9c8cfa191208`.
- **Draw:** seed 20261122, stratified: 10 of 49 `benchmark_algorithms` cases and 30 of 122 cases from the other modules.
- **Frozen:** 06:40 PKT, before any A/A measurement.
- **Cut to 26 cases** (PM 07:43; amendment frozen 07:47, before any measurement): `networkx.aa_noise_sample_cut26.json`, sha256 `016b12ed470cf9a72b4b363c490f65b5a21310e8c07878b6eeaeac6ac093f452`. It takes the first 6 `benchmark_algorithms` draws and the first 20 other draws from the same seeded draws.
- **A/A re-run sample** (proposed 10:08, before any A/A data exist): `networkx.aa_noise_sample_cut23.json`, sha256 `44f8b8c76a33550ff350f54951d165ba94bf52738dcd1c93cd733eddc4fba260` (re-hashed 10:12 after correcting a wrong 'frozen_at' stamp; the 23 cases are unchanged; old sha 6361b329…). It takes the first 3 `benchmark_algorithms` draws and the first 20 other draws, a subset of cut26.

## Q3 edit lists (frozen before any reach was computed)
- `edits/geopandas.q3.candidates.json` sha256 `f5a73f62d2649ad1e6767ab685c84f4398f13f8c17a45ec2340494fca8d96d65` (20 qualifying; head `3e92048f6289`)
- `edits/pvlib-python.q3.candidates.json` sha256 `e094b9cc8a7285e6f0bbb62d1fe4ea232aaa2af4aaa3a6a796507f0486749e70` (14 qualifying; head `91a21d9dc316`)

## Night queue 2026-11-22 (PM 15:20; frozen 15:33 PKT, before any night measurement; plan timestamps corrected from guessed 15:55/16:05 to real file times before hashing)
- `frozen/night-2026-11-22.cases.json` sha256 `e359fcae7a3a42307a7f8282783ce51e33433d3f65b2972ad3ee26a6ff5a76e8`
- `results/raw/night-2026-11-22/PLAN.md` sha256 `dd0b97c0ef9099fa0e87f3101fcdb7b41251496b23247ae179dbc1c3f35539fa`
- `results/raw/networkx/bench/aa_flagged/plan.md` sha256 `248fd41845d386f707b1d6fa6cfe9cf02af13c74554cae6a467af4418b275b38`
- `results/raw/networkx/slowdowns/repeat/plan.md` sha256 `729d96f065467c75b79336fcf35005a7d09f3159ef4e4bec2f99644f3f97bc7b`
- `results/raw/networkx/bench/drift/plan.md` sha256 `4716649ccb9028078f4730c024928168b550efa4715cfbb549270d8141f2125f`
- `results/raw/bottleneck/bench/plan.md` sha256 `f34a7f8289660b1669ec5510adab599717f2c9fcbfc2cf0372c05eaa7255fa5c`
- `scripts/night_analyse.py` sha256 `3d30eae4e9d3a637848213f5d8c6414411cbbfa5468b94d1a5cd9be13f8d20f0`
- `scripts/night_nx.py` sha256 `ca104873ed1595bc53e43043235bf93e00904ee786ce056fc2a779b06c7c70d1`
- `scripts/wsl/night_queue.sh` sha256 `8f15879d66c2dfc76d9809c5c80c5fb82d70395808893c85cdf98cc22e5e54a0`
- **Amendment 1 (15:35 PKT, before any measurement):** the block gate's Windows-CPU probe (`SP.wincpu`, a powershell call) timed out at 60 s and returned 100, so the gate could never open. Queue killed in its first gate (no run had started) and restarted 15:35:12. Windows CPU now comes from the telemetry file (mean of samples in the last 30 s). Thresholds unchanged. New `scripts/night_nx.py` sha256 `fa04a9ae9bda800080fe74f2a3075151db337e8fa0602a28d5ab49ea379c619c`.

## Mining-precision labelling input (owner decision 15:43; frozen 15:44 PKT, before any labelling)
- `frozen/labelling/sheet.jsonl` sha256 `19d5cdaf74d672985646ac5fb5dcd4f09899ca8b05b541d94cad50aa3236b7e5`
- `frozen/labelling/codebook.md` sha256 `8cf954cc5a4f75e186a2ccae45a0222b329969f2b6965d527543e4d6c417b303`
- `scripts/labelling_jsonl.py` sha256 `242f5c9c3c0311c9937e80716f45e56ebf58ca2ea6d13720b09436efcd4aa84b`
- Built during night item (b) at nice 19, CPUs 0–1 (benchmarks on 2–5), 15:43:5x–15:44:02: logged as concurrent in results/raw/night-2026-11-22/CONCURRENCY.md.
- **Amendment 2 (15:50 PKT; PM 15:46, after W1 read asv's source):** exact two-sided MWU is primary in `scripts/night_analyse.py`, and the earlier scipy 'auto' test is shown next to it. Thresholds and the 1 + 3σ rule are unchanged. No analysis had run; a smoke run at 15:51 was deleted. New sha256: `scripts/night_analyse.py` `0ef09fa9c06984b94787aa154ccf659ab44695ad0aef55c4436b046eedb535a5`, `harness/bth/stats.py` `e2bad4d8eb8db67b4f954ab0c6567ff89a63f7b4953d238fd83991094ffb204e` (new `mwu_p` methods; asv_rule's default is unchanged, so running drivers are unaffected).

## Labelling outputs and codebook v2 (PM 15:55 D26; recorded 15:53 PKT)
- `results/labelling/final_labels.jsonl` sha256 `5c0159d34a39299a9b6eb5007ba9fe95e79ef9c4fdf14e46ebe5b1544bb78760`
- `results/labelling/rater1.jsonl` sha256 `e2597192d4e79711541cb751c466b5773f15420601c1fe2180ea2906d32117e0`
- `results/labelling/rater2.jsonl` sha256 `de60d9379594b47f9fae100c39f0a59de1139b6fa7d71763fc244c2417df3184`
- `results/labelling/adjudication.jsonl` sha256 `8a40c8537864f49bd2fd1bc4db1c7d6c1fb4e574a1c1ba6be02ba4c80c8efb21`
- `results/labelling/codebook-notes.md` sha256 `d58ba58571ba5ef7c9c79a81a4bcc83f9881a53c211881ece99253689cab8ae6`
- `frozen/labelling/codebook-v2.md` sha256 `fd5f5bd118ec8fba95188a453b01f7df94fd40b7978b60ddb7ca250265c6d0e2`
- `scripts/labels_b1.py` sha256 `ad080e3944eda95395648d3359f7eb7e96d18b60fed4297c845fcebb2dcfad01`
- `results/labelling/precision_b1.json` sha256 `bb54159064a7ac53ec434bc24fa08ea90fc21db68e7b71d208626a685765d14b`
- codebook v2 frozen 15:53, before any v2 labelling; v1 unchanged.

## E5 setup-cached pass plan (PM 16:44; frozen 16:52 PKT, before implementation or measurement; for the night of 23→24 Nov)
- `results/raw/networkx/bench/setup_cached/plan.md` sha256 `58f95a566618a486f24c9761c949d14cc3eb7c64be11bf6be7cd68a303d5e22a`
- Also recorded: `scripts/edit_share.py` `de64545bd5eb7039af9afff3ba0de73b6ee3ca8f219556110319df02f6420cb6`, `results/raw/networkx/edit_share.json` `ddb6753b024f366b12c1234ec8d32178906e77390675058900a854cd0a217b52`
