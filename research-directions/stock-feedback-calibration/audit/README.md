# How to interpret this audit

The local harness checks document presence, CSV schemas, declared protocols, and whether hypotheses have rivals and falsification conditions. It does not inspect mathematical proofs, reproduce literature, validate datasets, or estimate publication probability.

Initial scaffold run: 5 PASS, 7 WARN, 19 FAIL. This is the incomplete template baseline, not a scientific evaluation.

The completed package records candidate mechanisms, closest-work overlap, experiments, search limitations, and unresolved risks. See generated-audit-report.md for the actual latest counts. Warnings about novelty and data are intentionally unresolved.

## Important checker limitations

- A PASS for unsupported_claims means no row carries certain warning labels; it does not verify evidence for established claims.
- The checker now validates nonnegative integer search counts and their ordering, but does not verify their provenance. Missing historical search counts are deliberately left blank.
- A declared forward_test is a plan, not an executed prospective evaluation.
- Protocol booleans are commitments. Conditional applicability of costs, attribution, and LLM masking is explained in ../06-evaluation-protocol.md.
- Three Mermaid sources explain information flow, label maturity, and decision gates; the number of figures is a structural requirement, not scientific quality.

The 9 September 2026 harness update preserves this package's finance requirements through the legacy default profile. It adds a separate software-performance profile and input validation; no finance controls were removed to make this candidate pass. See ../05-advisor-questions.md for decisions that remain unresolved even if there are no structural failures.
