# PhD Research Workspace

**Status:** 2026-11-21. The active research direction is Study 1 (reduced build and test validation for iterative code optimization). Earlier candidate directions are kept as background.

**Evidence boundary.** This is a working repository, not a published artifact. Each research folder carries its own status line and evidence boundary; read those before quoting a claim. Nothing here is advisor-approved: every "advisor review" file in the repository is AI-written (see [the advisor model](research-directions/build-test-reduction/pm/advisor/persona.md), section 1).

## Current research status

Study 1: validate each edit in an iterative code-optimization session with a reduced build and a reduced test/benchmark set chosen by deterministic rules, with no AI in the method.

| Workstream | State on 2026-11-21 | Entry point |
|---|---|---|
| W1 literature | v3.2, final for the meeting | [one-page summary](research-directions/build-test-reduction/01-literature/literature-in-one-page.md) |
| W2 practice survey | final draft, critic-checked (28 systems) | [README with at-a-glance table](research-directions/build-test-reduction/02-practice-survey/README.md) |
| W3 experiment | readiness v1.1; **PRELIMINARY** draft results, overnight runs pending | [results](research-directions/build-test-reduction/03-experiment/results/results.md) |
| Advisor meeting | about 2026-11-23/24 | [meeting pack](research-directions/build-test-reduction/meeting-2026-11-advisor/README.md) |

Front door for the study: [Study 1 README](research-directions/build-test-reduction/README.md).

## Repository map

| Area | What is there | Status |
|---|---|---|
| [`research-directions/`](research-directions/README.md) | Index of research directions | Study 1 is current |
| [`research-directions/build-test-reduction/`](research-directions/build-test-reduction/README.md) | **Study 1**: literature (W1), practice survey (W2), experiment (W3), project management (`pm/`), advisor meeting pack | Current |
| [`research-directions/llm-optimization-validation/`](research-directions/llm-optimization-validation/README.md) | "Understanding and Detecting Workload Regressions in Iterative Python Code Optimization" (Sept–Oct 2026 package, provisional, pre-pilot) | Background; superseded as the active direction by Study 1 |
| [`research-directions/2026-09-05-direction-review.md`](research-directions/2026-09-05-direction-review.md) | Cross-domain feasibility review of candidate directions | Historical |
| `research-directions/stock-feedback-calibration/`, `research-directions/stock-selective-routing/` | Earlier finance candidates | Not in the working tree (deleted, uncommitted); recoverable from git history (commit `a9de702`). Not linked here |
| [`Spark Elevate/`](Spark%20Elevate/README.md) | SPARK Stage 1 project concept packet | Ready for advisor discussion, not submission |
| `courses/` | First-semester course support (links below) | Course work |
| `output/pdf/`, `output/presentations/`, `output/video/` | Rendered study guides, decks and videos, e.g. [SemOpt advisor deck (PDF)](output/pdf/semopt-advisor-deck.pdf) and [PPTX](output/presentations/semopt-advisor-deck.pptx) | Generated files |
| [`research-audit-harness/`](research-audit-harness/README.md) | Local documentation-audit tool (Python standard library only) | See "Research audit harness" |
| `tmp/` | Scratch scripts and working folders | Not part of the research record |

## Course support guides

- [Applied Information Security — Lectures 1–3](courses/first%20sem/Applied%20information%20security/support.md)
- [Deep Learning — Lectures 1–5](courses/first%20sem/Deep%20Learning/support.md) — concise explanations, worked numerical videos, and optional longer lessons; [numerical practice with checked answers](courses/first%20sem/Deep%20Learning/numerical-practice.md).
- [Generative AI — Introduction, AE/VAE and GANs Parts 1–2](courses/first%20sem/genai/support.md) — short explanations, numerical video routes, optional depth, and assignment support; [numerical practice with checked answers](courses/first%20sem/genai/numerical-practice.md).

## Research audit harness

- [Harness documentation](research-audit-harness/README.md)
- [Harness schema and behavior reference](research-audit-harness/docs/reference.md)
- Run the Python optimization proposal audit (the earlier package):

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/llm-optimization-validation
  ```

- Two stock-forecasting commands were listed here before. They target `research-directions/stock-feedback-calibration` and `research-directions/stock-selective-routing`, which are not in the working tree, so they cannot run until those folders are restored from git history:

  ```powershell
  python research-audit-harness/scripts/audit.py research-directions/stock-feedback-calibration
  python research-audit-harness/scripts/audit.py research-directions/stock-selective-routing
  ```

- The harness checks that documentation records evidence, comparisons, protocols and unresolved risks. It is not a runtime experiment harness. The Study 1 experiment harness lives in [`03-experiment/`](research-directions/build-test-reduction/03-experiment/readiness.md).

The harness is deliberately local and uses only the Python standard library. It does not install or execute third-party agent skills.
