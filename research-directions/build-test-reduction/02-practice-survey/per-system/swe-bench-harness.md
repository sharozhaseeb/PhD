# SWE-bench evaluation harness

Status: critic-checked 2026-11-21 (4 fixes; all code cites re-opened and OK; paper cites could not be re-opened) · Last checked: 2026-11-21
Artifact: https://github.com/SWE-bench/SWE-bench @ 02e7a74ffd0b707aab73d203fe87bdc7c76afc8e (local clone: `C:\Users\pc\study\bt-lab\survey\SWE-bench_SWE-bench`) · Paper: https://arxiv.org/abs/2310.06770 (Jimenez et al., ICLR 2024; read via arxiv HTML, summarised by a fetch tool, first ~100k of 189k chars only)
Evidence labels: **[src]** read in source (file path + line or paper section quoted/paraphrased), **[inf]** inferred by us from sources, **[unk]** not found (say where you looked).

Two code bases are covered. Section 0 = CLASSIC harness, release v4.1.0 (https://github.com/SWE-bench/SWE-bench @ 726c5461e2ef52d83cf1ea2107870a8bb3328d57, local `C:\Users\pc\study\bt-lab\survey\SWE-bench_v4.1.0`), which SWE-Perf/GSO/SWE-fficiency fork. Sections 1-8 = HEAD @ 02e7a74, a REFACTORED version that no longer contains the `docker_build.py` layering, `test_spec` generation, `get_test_directives` or `cache_level` in code. Sections 1-8 are HEAD unless stated.
CRITIC: every `[src] ... paper ...(per summary)` claim in this note is downgraded to UNVERIFIED: both arXiv PDF fetches for 2310.06770 timed out (300 s) so the paper text was not re-read; treat paper quotes/section numbers as [inf] until checked. All code-line claims were re-opened and match (sections 0-8) except the notes under CRITIC below.

## 0. Classic harness (v4.1.0 @ 726c546), paths under `swebench/harness/`
- **Three image layers + cache_level.** `base_image_key`, hashed `env_image_key` (sha256 of `env_script_list`, 22 chars), `instance_image_key`. [src] `test_spec/test_spec.py:72-112`; builders `docker_build.py:162` (`build_base_images`), `:270` (`build_env_images`), `:336` (`build_instance_images`); instance Dockerfile `dockerfiles/python.py:48-52` (`FROM` env image, `COPY setup_repo.sh`, `RUN /bin/bash /root/setup_repo.sh`). `--cache_level` choices none/base/env/instance, default env: `run_evaluation.py:635-641`. Semantics = which images are REMOVED after the run: base only at `none`; env at `none|base`; instance (`sweb.eval*`) at `none|base|env`: `docker_utils.py:295-311`. Existing images are reused: `docker_build.py:256`, `:496`.
- **Repo clone + install in the INSTANCE image, once per instance** (CRITIC: confirmed; `setup_repo.sh` also strips remote/tags and runs `git gc`, `python.py:277-292`): `make_repo_script_list_py` runs `git clone --single-branch`, `git reset --hard {base_commit}`, optional `pre_install`, then `specs["install"]`. [src] `test_spec/python.py:274,277,297-303`.
- **BUT the install is ALSO re-run inside every eval script**, i.e. per prediction, after the model patch is applied: `if "install" in specs: eval_commands.append(specs["install"])`. [src] `test_spec/python.py:443-444`. (So "install not per prediction" holds only for the image-build install.) Container is fresh per prediction (`docker_build.py:470` `build_container`); patch applied via `GIT_APPLY_CMDS` (`run_evaluation.py:64-68,166-179`) before `/bin/bash /eval.sh` (`run_evaluation.py:198-207`).
- **Eval script order**: activate env, informational `git diff {base}`, install, `git checkout {base} <test files>`, `git apply` test patch, start marker, test command, end marker, reset test files. [src] `test_spec/python.py:405-452`; header `set -uxo pipefail` (no `-e`) `test_spec/test_spec.py:57-62`.
- **`get_test_directives` (which test files run).** Directives = every path in `diff --git a/.* b/(.*)` of the `test_patch` minus non-test extensions (`NON_TEST_EXTS`); Django: strip `.py` and `tests/`, slashes to dots. [src] `test_spec/python.py:230-261`. Test command = per-repo/version `test_cmd` + directives (`python.py:418-425`). So per prediction ONLY test files touched by the gold test patch run, whatever the candidate edits. [src]
- **F2P/P2P grading.** `get_eval_tests_report` compares log-parsed status per test with the F2P/P2P lists (`grading.py:94`); `get_resolution_status`: F2P=1 and P2P=1 -> FULL, 0<F2P<1 and P2P=1 -> PARTIAL, else NO (`grading.py:215-228`). Pass/fail only. [src]
- [inf] Study-1: the eval-time install (`python.py:443-444`) is the per-candidate build cost a reduced-build arm would target; the test set is fixed per instance by the test patch, so per-edit reduction is a new mechanism, not an existing one.
- F2P/P2P derivation at curation is not in v4.1.0 `harness/` [unk: grepped `swebench/harness`]; see paper §A.3 below.

## HEAD (02e7a74): sections 1-8

## 1. What it is (2-3 lines)
Docker-based harness that applies a model patch to a repo at `base_commit` inside a per-instance container, runs a per-instance eval script, parses test logs and grades against FAIL_TO_PASS / PASS_TO_PASS lists. Correctness only; no performance measurement. [src] `swebench/harness/run_evaluation.py:229-429`, `swebench/harness/grading.py:309-326`.

## 2. Build / environment
- "Build" = Docker image build (buildx) of one image per instance from a per-task Dockerfile; the repo install happens at image build time and (in the paper's design) again at eval time. [src] `swebench/image_builder/docker_build.py:35-110` (`docker buildx build ... --load`); paper §A.4 (per summary): "install command is run again before the tests" (paraphrase, not verified verbatim).
- At this commit: `TestSpec` "assumes images are already built"; images are prebuilt and named `swebench/sweb.eval.x86_64.<id>:latest` (dunder replaced by `_1776_`). [src] `swebench/types.py:25-29`, `swebench/image_builder/image_spec.py:36-48`, `swebench/task/checks.py:66-69`. CHANGELOG: "`TestSpec` now assumes images already exist." [src] `CHANGELOG.md:45`.
- `build_instance_image` skips the build if the image already exists locally (reuse across predictions). [src] `swebench/image_builder/docker_build.py:167-182`.
- Task repo layout: each instance has `Dockerfile`, `eval.sh`, `tests.json` (FAIL_TO_PASS/PASS_TO_PASS), `gold.patch`, `test.patch`. The eval script is dataset data, not generated by harness code. [src] `swebench/task/repo.py:3-17`; `swebench/harness/utils.py:251-273` (`make_test_spec` takes `eval_script` from the instance).
- At HEAD the eval script (hence whether the install is re-run per prediction at HEAD) is dataset data from HF, not read: [unk] for HEAD; v4.1.0 code (section 0) is the evidence for the re-install. The three-layer design and `cache_level` survive at HEAD only in stale docs (`docs/guides/docker_setup.md:66-70,96-101`); `cache_level` is in no `.py` file at HEAD (grep, 0 hits). Authoritative code: section 0.
- No incremental/reduced build: each prediction runs in a FRESH container from the image, container removed afterwards. [src] `run_evaluation.py:284`, `run_evaluation.py:425-428`.
- Environments are per release version, not per instance (cost of manual setup). [inf] paper §A.3 (summary only; not re-opened by critic).

## 3. Correctness tests per candidate
- Per prediction: apply patch BEFORE the eval script runs (`git apply --verbose`, fallbacks `--3way`, `--reject`, `patch --batch --forward --fuzz=5 -p1`; HEAD adds `git checkout -- . ; git clean -fd` between attempts and a reverse-apply check), then run `/bin/bash /eval.sh` (default timeout 1800 s). [src] `run_evaluation.py:55-58`, `run_evaluation.py:299-337`, `run_evaluation.py:359-368`; `swebench/cli/evaluate.py:30`.
- Eval script does: reset test files, apply test patch, run test command on test files, record exit code, reset again (shape inferred from the exit-code helper docstring and marker checks). [src] `swebench/harness/utils.py:222-241` ("Eval scripts end with a `git checkout` that resets the test files"); `swebench/task/checks.py:46-47` (script must contain `>>>>> Start Test Output` / `End Test Output`).
- Which tests: paper says the test command runs "on the test files touched by the test patch"; success requires all F2P and P2P tests pass. [src] paper §A.4 (per summary; verify against PDF before quoting). `get_test_directives` is NOT at HEAD [unk: grepped `swebench/`, `docs/`]; real code is v4.1.0 `test_spec/python.py:230-261` (section 0), identical to SWE-Perf's copy (`evaluation/utils.py:297-328`).
- Grading: F2P success + P2P success => FULL; partial/none otherwise. [src] `grading.py:309-326`; status map from repo-specific log parsers `swebench/harness/log_parsers/*`.
- Anti-spoof check: log is cross-checked against the test command exit code. [src] `grading.py:162-176`.
- Curation of F2P/P2P: test patch applied, tests run before and after the gold patch; F2P = fail->pass, P2P = pass->pass; instances without at least one F2P are dropped; ImportError/AttributeError in pre-log drops the instance. [src] paper §2.1, §A.1, §A.3 (per summary). Code that derives lists (validation) is not in this clone beyond the grader [unk: looked in `swebench/collect/`, `swebench/task/`; the F2P derivation scripts are not present].
- Is it test selection? [inf] Yes, but FIXED per instance at curation time (test files from the test patch; listed tests from before/after gold run); it does not depend on which source lines the candidate edits.

## 4. Performance measurement per candidate
Not applicable: SWE-bench measures only resolution. Only a per-instance timeout (1800 s) bounds runtime. [src] `swebench/cli/evaluate.py:30`.

## 5. Cost per candidate (if reported)
- Disk: docs table says env cache ~100 GB, instance cache ~2,000 GB; >=120 GB free and 16 GB RAM recommended. [src] `docs/guides/docker_setup.md:13-14`, `docs/guides/docker_setup.md:96-101`.
- Per-prediction wall-clock cost: [unk] (not reported in the docs read).
- Result caching: keyed only on `run_id` + `instance_id`; a changed diff with same run_id is NOT re-evaluated. [src] `docs/faq.md:103` (paragraph at 102-105); `run_evaluation.py:272-273` (`if report_path.exists(): return`).

## 6. Iteration / cumulative re-validation
Single-shot: one patch per instance per run, graded independently. No multi-edit sequence, no cumulative re-check. [src] `run_evaluation.py:229-429` (one patch applied to a fresh container). Candidate reset between apply attempts is `git checkout -- . ; git clean -fd`. [src] `run_evaluation.py:303-309`.

## 7. Limitations the authors state
- Python only; test-passing does not capture efficiency/readability ("less comprehensive, efficient, or readable"). [src] paper §7 (per summary).
- Per-version environments instead of per-instance, because of manual cost. [src] paper §A.3 (per summary).
- Results cache ignores the diff. [src] `README.md:119`, `docs/faq.md:103`.

## 8. Relevance to Study 1 (reduced build + reduced test/benchmark per edit, deterministic)
- [src] Test selection in the base harness is static per instance (from test-patch files + precomputed F2P/P2P), which gives a baseline "fixed subset" arm; there is no per-edit selection or impact analysis. `swebench/harness/grading.py:237-247`.
- [src] Build reduction exists only as image reuse: image built once, fresh container per prediction, no incremental rebuild. `image_builder/docker_build.py:167-182`, `run_evaluation.py:284`.
- [inf] The eval script is a plain shell script stored with the task, so substituting a reduced test command (subset of tests) or skipping reinstall is a local change to `eval.sh`, testable for safety by comparing grading against the full script's F2P/P2P outcomes.
- [inf] Only pass/fail determinism is needed here (no timing noise), which makes SWE-bench the cleaner testbed for the correctness half of reduced validation.

## Sources
- v4.1.0 @ 726c546 read: `test_spec/test_spec.py` 55-112; `test_spec/python.py` 230-261, 264-318, 405-452; `docker_build.py` (grep); `dockerfiles/python.py` 48-52; `docker_utils.py` 295-311; `run_evaluation.py` 64-68, 150-207, 635-645; `grading.py` 94, 215-228.
- Files read (all @ 02e7a74): `swebench/harness/run_evaluation.py` 55-58, 229-440; `swebench/harness/utils.py` 215-273; `swebench/harness/grading.py` 160-326; `swebench/harness/constants/__init__.py` 1-82; `swebench/types.py` 1-49; `swebench/image_builder/docker_build.py` 1-185; `swebench/image_builder/image_spec.py` 1-125; `swebench/task/repo.py` 1-120; `swebench/task/checks.py` 1-240; `swebench/cli/evaluate.py` (grep); `docs/guides/docker_setup.md` 1-173; `docs/faq.md` (grep); `docs/guides/evaluation.md` (grep); `CHANGELOG.md` (grep); `README.md` (grep).
- Paper: https://arxiv.org/html/2310.06770 §2.1, §7, §A.1-A.5 (via fetch-tool summary; only first ~100k of 189k chars; quotes need re-verification against the PDF).
