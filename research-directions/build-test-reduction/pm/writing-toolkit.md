# Writing toolkit for the Study 1 paper (for W6-PAPER)

Author: W7 architect. Written 2026-11-22. Status: **recommendation**. The PM and owner decide every install. Nothing was installed, enabled, downloaded or run for this file.

Inputs from this repo: `pm/tpm-paper-plan.md` (§4 must-not-claim list, §5 W6 set-up: `04-paper/`, `generated/numbers.tex`, `data-manifest.yaml`, no hand-typed digits) and `pm/advisor/paper-plan-advice.md` (§1 thesis and contributions K1–K6, §3 threats table, §4 outline with RQ1–RQ4).

Inputs from outside: the claude.ai skill and plugin catalogs, searched in this session, and the web pages listed in §6. Each page was fetched on 2026-11-22 unless it is marked **[S]** (seen only as a search-result snippet) or **[U]** (not verified).

---

## 0. Bottom line

- **No dedicated SE-paper skill exists anywhere** I looked: not in Anthropic's repos and not in the catalog. The best toolkit is a small **project-local skill plus a reviewer subagent**, built from Anthropic's official anti-hallucination recipe and the **ACM SIGSOFT Empirical Standards** (CC0). It needs no install.
- **One install is worth asking the owner about: Deep Review** (Apache-2.0, a contained skill) for a second, independent hostile review. Every other catalog plugin is optional or a poor fit (§3).
- **Already enabled and useful now:**
  - `dataviz` for figures;
  - `anthropic-skills:pdf` for reading cited PDFs;
  - `anthropic-skills:deep-research` for the related-work search;
  - `superpowers:verification-before-completion` for checking numbers before any "done";
  - `anthropic-skills:skill-creator` for building the project skill.
- **The biggest risks are fabricated or misattributed citations and numbers that do not trace to raw files.** Section 5 lists the guards.

---

## 1. Resource table

"Installed?" was checked in this session with `ListSkills` / `ListPlugins` (claude.ai account) and from the session's skill list (local Claude Code). Catalog entries show `enabled: false` unless the table says otherwise.

### 1a. Claude catalogs (claude.ai skills and plugins)

Five searches were run:
- `SearchSkills`: paper, research paper, academic writing, LaTeX, literature review, scientific writing, peer review, citations, research methods, writing, review, academic. **0 results.**
- `SearchPlugins` (2 searches): research paper, academic writing, LaTeX, literature review, scientific writing, peer review, citations, figures, thesis, scientific figures, academic, empirical study, methodology.
- `ListSkills`: only the default Anthropic skills (docs, pdf, docx, pptx, xlsx, deep-research, skill-creator, …).
- `ListPlugins`: **none enabled on the account.**

| Name (catalog) | What it gives | Publisher / reach | Quality for us | License | Installed? |
|---|---|---|---|---|---|
| **Deep Review** (Dipak Krishnan) | One `deep-review` skill: a calibration interview, specialist passes, claims checked against sources and computations, self-critique, then a review ranked by severity (critical / significant / minor / questions). The referee persona can be set. Source: github.com/dipakkrishnan/deep-review-skill | community, directory-reviewed; **contained** (no remote server) | **Med-high.** The best ready-made hostile reviewer. The repo calls it "experimental". | Apache-2.0 | No |
| **Research Desk** (Naji Kayal) | Skills: citation-check (checks that references are real), related-work (drafted from your own sources), paper-critique (referee style), paper-compare, research-litnote, decision-matrix, llm-council. Two MCP servers: reference-lookup (one of them hosted) | community; **remote** (bib entries go to a hosted lookup service) | **Med, unverified.** No public repo found by search, so its quality and license could not be read. | not found | No |
| **research-superpowers** (Patrick Leiverkus) | 16 skills, idea → literature → draft → peer review: drafting-manuscript, literature-review, requesting-peer-review (constructive, then adversarial), add-to-library (checks metadata against Crossref/OpenAlex). Also agents and a SessionStart hook | community; **privileged** (installs a hook) | **Med.** A coherent workflow, but new, aimed at the humanities, and heavy (wiki scaffolding). | MIT (github.com/leiverkus/research-superpowers) | No |
| **letX** | Compile and fix LaTeX in a letX cloud account; templates | community; **remote** (uploads the draft) | Low to med. A third alternative to the TPM plan's three toolchain options. Uploading is the owner's call. | not checked | No |
| Corbis | Literature reviews, citation checks and referee reviews through the Corbis connector | community; remote | **Low.** Finance, real-estate and economics corpus. | not checked | No |
| anti-ai-writing | A style editor that strips "AI tells" | community; contained | **Low, and risky.** It rewrites at sentence level and can change technical meaning or hedges. Use only as a lint on prose the owner wrote, never on numbers or claims. | not checked | No |
| read-paper, Academic PDF Translation, Thesis Examiner, ArcDeck | Paper summaries, translation, viva questions, paper-to-slides | community | Low for drafting. Thesis Examiner might help with viva prep later. | not checked | No |

### 1b. Already available in this Claude Code setup (no install)

| Name | What it gives W6 | Quality |
|---|---|---|
| `dataviz` skill | Chart form, colour-blind-safe palette with a validator, mark specs. Use it for Fig. 2–5 in matplotlib (vector PDF, per TPM §5). | High |
| `anthropic-skills:deep-research` | Multi-source research with subagents. Use it for related work, and only as a **pointer finder**: every hit must be fetched and read (§5). | High as a search tool; not a citation authority |
| `anthropic-skills:pdf` | Reading and extracting text from cited papers' PDFs, to check quotes | High |
| `anthropic-skills:skill-creator` | Scaffolds and tests the project-local `paper-writing` skill (§2, #1) | High |
| `superpowers:verification-before-completion` | "Evidence before assertions": no "done" claim until checks pass, e.g. the macro check and a LaTeX build | High |
| `superpowers:requesting-code-review` | For `make_numbers.py` and `make_figures.py`, which are code | High |

### 1c. Anthropic official resources

| Name | Link | What it gives | Quality | License | Installed? |
|---|---|---|---|---|---|
| Prompting best practices (the old per-technique pages are now sections here) | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Clear and direct instructions; XML tags with `<documents><document index="n"><source>`; long data first and the query last (up to 30 % better in Anthropic's tests); quote-first grounding; self-correction chains (draft → review → refine as separate calls); warning that recent models overuse subagents | **High** | Docs (n/a) | — |
| Reduce hallucinations | https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations | Allow "I don't know"; extract word-for-word quotes first; **after drafting, find a supporting quote for each claim and retract any claim without one**; restrict answers to the provided documents; best-of-N consistency checks. The page itself says these techniques reduce hallucinations but do not remove them. | **High.** This is the core of every template below. | n/a | — |
| Prompt-engineering overview | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview | Define success criteria and evals before tuning a prompt | Med | n/a | — |
| Citations API | https://platform.claude.com/docs/en/build-with-claude/citations | Machine-checked pointers into supplied documents (text, PDF or custom chunks). It cannot be combined with structured outputs. Useful only if W6 scripts API calls; in Claude Code the prompt-based quoting is the equivalent. | Med | n/a | — |
| Prompt library | https://platform.claude.com/docs/en/resources/prompt-library/library | **Retired.** It redirects to the best-practices page, so there are no academic entries to cite. | — | — | — |
| anthropics/skills → **doc-coauthoring** | https://github.com/anthropics/skills (SKILL.md at https://raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md) | Three stages: (1) context gathering with 5–10 clarifying questions; (2) section-by-section scaffold, brainstorm, draft, targeted edits, with the sections that have the most unknowns first and the abstract last; (3) **reader testing**: a fresh subagent that sees only the document answers predicted reader questions, and the authors loop until it answers correctly. There are no research or LaTeX skills among the 19 in the repo. | **High** for the process. Stage 3 is the hostile-reader pattern. | The repo README says many skills are Apache-2.0. doc-coauthoring has **no license file**, so paraphrase it; do not copy it. | Not installed as a plugin. The idea is reused in §2 #1. |
| anthropics/claude-plugins-official → math-proof | https://github.com/anthropics/claude-plugins-official (README at https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/math-proof/README.md) | A design precedent. Fresh verifier subagents check line by line under a judge. A ledger records what is proved, refuted or open. It warns that citations quoted "from memory" are unverified. | Med (pattern only) | Apache-2.0 | No |
| anthropics/knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins | No writing plugin; bio-research covers biomedical literature only | Low | Apache-2.0 | No |
| Claude Code: Skills | https://code.claude.com/docs/en/skills | `.claude/skills/<name>/SKILL.md`. Frontmatter fields: `name`, `description`, `when_to_use`, `allowed-tools`, `context: fork`, `agent`, `model`, … Keep SKILL.md under 500 lines and move detail to supporting files. `$ARGUMENTS` and `` !`cmd` `` injection are supported. | **High** | n/a | — |
| Claude Code: Subagents | https://code.claude.com/docs/en/sub-agents | `.claude/agents/<name>.md`; `name` and `description` are required; a `tools:` allowlist (the read-only example is `Read, Grep, Glob`). Each subagent starts in a fresh context, with no conversation history. | **High.** This is what makes a reviewer that has not seen the drafting session possible. | n/a | — |

### 1d. Community resources (GitHub)

| Name | Link | Author | What it gives | Quality | License |
|---|---|---|---|---|---|
| claude-scientific-skills → **peer-review** | https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/skills/peer-review/SKILL.md | K-Dense | 11-stage referee workflow: a claim-to-evidence matrix; a stats and reproducibility audit (are "no effect" claims backed by precision?); comments as location → observation → criterion → why it matters → requested action; separate author and editor channels; a tone check | **High.** The best referee scaffold found. It leans towards biomedicine. | MIT (per-skill licence stated in each SKILL.md) |
| claude-scientific-skills → **citation-management** | https://github.com/K-Dense-AI/claude-scientific-skills/blob/main/skills/citation-management/SKILL.md | K-Dense | DOI/arXiv → BibTeX; a bib validator (fields, duplicates, unresolved keys, optional CrossRef DOI check) | Med-high. **It includes Python scripts: do not run them without the owner's approval** (the "never run downloaded code" rule). | MIT |
| claude-scientific-skills → scientific-writing, literature-review, venue-templates | https://github.com/K-Dense-AI/claude-scientific-skills | K-Dense | Claim traceability; venue LaTeX templates | Med. Not SE-specific. | MIT |
| ComposioHQ/awesome-claude-skills | https://github.com/ComposioHQ/awesome-claude-skills | ComposioHQ | Only generic research and writing skills | Low | Apache-2.0 |
| travisvn/awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills | travisvn | Only links to K-Dense | Low | none stated |

### 1e. Writing standards the prompts encode (no install; read and cite)

| Name | Link | What it gives | Quality | License |
|---|---|---|---|---|
| **ACM SIGSOFT Empirical Standards** | https://github.com/acmsigsoft/EmpiricalStandards ; site https://www2.sigsoft.org/EmpiricalStandards/ ; review tool https://www2.sigsoft.org/EmpiricalStandards/tools/ [S] | Essential, desirable and extraordinary attributes; antipatterns; **invalid criticisms** (do not fault limitations that are inherent to the method, and do not demand a different study design) | **High.** It is the reviewing norm at ESEM-style venues. | **CC0-1.0** |
| ↳ General standard | https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/docs/standards/GeneralStandard.md | See the checklist in §4.3 | High | CC0 |
| ↳ Engineering Research | …/docs/standards/EngineeringResearch.md (same base path) | Need; artifact description; conceptual and empirical evaluation; comparison with the state of the art, or a reason why not | High (fits RQ4 and the A4 policy) | CC0 |
| ↳ Benchmarking | …/docs/standards/Benchmarking.md | Justify the benchmark; replicable setup and workload; fair comparison; enough repetitions and duration; construct validity | **High** (fits RQ1 and RQ3) | CC0 |
| ↳ Repository Mining | …/docs/standards/RepositoryMining.md | Unit of analysis; selection criteria; validated inclusion; multiple annotators with inter-rater reliability; metric validity; external validity | **High** (edit mining, R-4 precision, two raters with κ) | CC0 |
| ↳ Optimization Studies, Data Science | …/OptimizationStudies.md, …/DataScience.md | Search-based SE and predictive modelling | Low fit. Use Data Science only for "infrastructure described; results beyond one summary value". | CC0 |
| Wohlin et al., *Experimentation in Software Engineering*, 2nd ed. | DOI 10.1007/978-3-662-69306-3 [S] | Four-way classification of threats: conclusion, internal, construct, external | Canon | Springer |
| Verdecchia, Engström, Lago, Runeson, Song (2023), "Threats to validity in SE research: a critical reflection", IST 164:107329 | DOI 10.1016/j.infsof.2023.107329 [S]; https://robertoverdecchia.github.io/papers/IST_2023.pdf [S] | Critique of boilerplate threats sections. Use it to justify **specific, mitigated** threats. | High | Elsevier |
| Sjøberg & Bergersen, "Construct validity in SE", IEEE TSE | DOI 10.1109/TSE.2022.3176725 [S]; EASE 2023 follow-up DOI 10.1145/3593434.3593449, https://arxiv.org/abs/2306.05336 [S] | How to report construct-validity threats properly ("executed" ≠ "able to detect") | High | IEEE / ACM |
| Papadopoulos et al. (2019), "Methodological principles for reproducible performance evaluation in cloud computing", IEEE TSE 47(8) | https://d3s.mff.cuni.cz/publications/papadopoulos_methodological_2019/ ; DOI 10.1109/TSE.2019.2927908 | Eight principles: repetitions, independent experiments, statistical evaluation, units, setup description, artifacts, … (**exact P1–P8 wording not verified**; read the paper before citing any one principle) | High for ICPE | IEEE |
| Kalibera & Jones (2013), "Rigorous benchmarking in reasonable time", ISMM | DOI 10.1145/2464157.2464160 [S] | How many repetitions to run at each level, and how to report them | High | ACM |
| Georges, Buytaert, Eeckhout (2007), "Statistically rigorous Java performance evaluation", OOPSLA | DOI 10.1145/1297027.1297033 or …/1297105.1297033 [S]: **check which DOI resolves** | Confidence intervals, not single runs | High | ACM |
| ESEM 2026 Registered Reports track | https://conf.researchr.org/track/eseiw-2026/eseiw-2026-esem---registered-reports-track | Stage 1 contents: motivation, RQs, hypotheses, design, planned analyses, power analysis where appropriate, outcome-neutral checks such as positive controls. 9 + 2 pages, LIPIcs format. **The 2026 dates have passed; 2027 is unknown.** | High (format model for the E1 pre-registration) | — |
| MSR 2027 Registered Reports track | https://2027.msrconf.org/track/msr-2027-registered-reports | Required parts: structured abstract; RQs with rationale; variables (independent, dependent and confounding, with how each is operationalised); datasets and why they were chosen; execution plan. 6 + 1 pages, IEEE format. **Initial-report deadline 20 Nov 2026, now passed.** | High (format model) | — |
| ACM Artifact Review and Badging v1.1 | https://www.acm.org/publications/policies/artifact-review-and-badging-current (returned 403) [S] | Badges: Available (archived, e.g. Zenodo DOI), Functional, Reusable, Reproduced | Med (artifact section) | — |

---

## 2. Top 5 to use, and why

1. **A project-local `paper-writing` skill and a `hostile-reviewer` subagent, built by W6 with `skill-creator`. No install needed.**
   - Where: `04-paper/.claude/skills/paper-writing/SKILL.md` and `04-paper/.claude/agents/hostile-reviewer.md`, or the repo-level `.claude/` (the PM decides).
   - The skill holds templates 4.1, 4.3, 4.4 and 4.5 as supporting files. The subagent holds template 4.2 and has `tools: Read, Grep, Glob` only.
   - *Why:*
     - A fresh-context reviewer that never saw the drafting conversation is the strongest guard against a writer who has talked itself into its own claims (Claude Code subagents docs; doc-coauthoring stage 3).
     - Everything in it comes from sources we read and control, so there is no supply-chain risk.
2. **Anthropic's "Reduce hallucinations" and "Prompting best practices" recipe**, applied to our own files:
   - wrap each result file in `<document><source>`;
   - extract quotes first;
   - retract any claim that has no supporting quote.
   - *Why:* it is the official method, and it fits the rule that every number is a macro: the "quote" for a number is the line in `generated/numbers.tex` and its raw-file comment.
3. **ACM SIGSOFT Empirical Standards: General + Benchmarking + Repository Mining + Engineering Research** (CC0), used as the checklist pass in 4.3 and as the reviewer's rubric.
   - *Why:* ESEM reviewers use these standards. Their "invalid criticisms" lists also keep our own reviewer from demanding a different study.
4. **Deep Review plugin** (Apache-2.0, contained). **Ask the owner to approve installing it.** Its persona is set to "ESEM PC member, measurement-strict".
   - *Why:* it gives a second hostile review that is independent of the prompts we wrote. If the owner declines, use the K-Dense peer-review SKILL.md as a **read-only reference** for comment format (location → observation → criterion → why → requested action). Its MIT licence allows adapting it.
5. **The threats and performance-method canon:** Wohlin (classification), Verdecchia et al. 2023 (avoid boilerplate), Sjøberg & Bergersen (construct validity), Kalibera & Jones and Georges et al. (repetitions and CIs), Papadopoulos et al. (reproducible performance evaluation).
   - *Why:* ICPE and ESEM reviewers will attack measurement first (advisor §1.4), and these are the papers they expect to see cited.
   - **W1 must verify each DOI before it enters `refs.bib`**; several are [S] above.

Not in the top 5:
- **Research Desk.** It has no readable source or licence, and it sends bib entries to a hosted service.
- **research-superpowers.** It installs a hook, and its workflow overlaps the PM/W1/W6 set-up.
- **anti-ai-writing.** It can change technical meaning.
- **letX.** It uploads the draft. It is a toolchain choice for the owner, alongside the TPM plan's three options.

---

## 3. Install asks for the owner (via the PM)

| Ask | Recommendation | Risk |
|---|---|---|
| Install **Deep Review** (claude.ai catalog plugin) | **Yes** | Low: a contained skill, Apache-2.0, readable source. It is called "experimental", so treat its output like any reviewer's. |
| Install **Research Desk** | Optional; not needed | Unknown source and licence; bib text goes to a remote lookup service |
| Run K-Dense `validate_citations.py --check-dois` | Not now. W1 can check DOIs by fetching doi.org pages instead. | Running downloaded code would need the owner's explicit approval |
| research-superpowers, letX, anti-ai-writing | No | Hook install, draft upload, meaning drift |

---

## 4. Prompt templates (adapted to Study 1)

How to use them:
- Paste a template into a fresh subagent or session, filling in the `{…}` slots.
- Long inputs go **first**, inside `<documents>`; the task goes **last** (best practices, long context).
- Each template ends with an output contract, so the result can be checked mechanically.

Shared inputs:
- `MACROS` = `04-paper/generated/numbers.tex`
- `MANIFEST` = `04-paper/data-manifest.yaml`
- `RESULTS` = `03-experiment/results/results.md` plus the raw files it names
- `MUSTNOT` = `pm/tpm-paper-plan.md` §4 (the 16-item must-not-claim list)
- `ADVICE` = `pm/advisor/paper-plan-advice.md` §1–§4

### 4.1 Section drafting from results (every number is a macro)

```text
<documents>
  <document index="1"><source>04-paper/generated/numbers.tex</source><content>{MACROS}</content></document>
  <document index="2"><source>03-experiment/results/results.md (sections: {list})</source><content>{RESULTS excerpt}</content></document>
  <document index="3"><source>pm/tpm-paper-plan.md §4 must-not-claim</source><content>{MUSTNOT}</content></document>
  <document index="4"><source>pm/advisor/paper-plan-advice.md §1 + §4 row for this section</source><content>{ADVICE excerpt}</content></document>
  <document index="5"><source>04-paper/sections/{neighbouring sections}.tex</source><content>{optional}</content></document>
</documents>

You are drafting Section {N} ("{title}", answering {RQk}) of an empirical
software-engineering paper for {ESEM|ICPE}. The study validates iterative Python
optimization edits with reduced builds and reduced test/benchmark selection, using
deterministic rules only. Subjects: networkx (main), bottleneck (build cost).

Step 1 - Evidence. In <evidence> tags, list every result you intend to use. For each:
  the macro name from document 1, its value, the raw-file comment on that macro, and
  a word-for-word quote from document 2 that states the same result. If a result has
  no macro, do NOT invent one: list it under <missing_macros> with the raw file and
  computation you think it needs, and leave it out of the prose.
Step 2 - Draft. Write LaTeX for sections/{file}.tex:
  - Every number, percentage, ratio, count or CI is a macro (e.g. \BOneUnreachedShare{}).
    No digit may appear in prose except years, section/figure/table numbers and
    citation keys. Write ranges as ranges (macros for both ends) and never as a single point value.
  - Scope every claim to its evidence: "on networkx", "in this replay", "on this
    machine". Use "replayed edit sequence", never "iterative session".
  - Do not state anything in document 3. Do not add citations: write \citeneeded{topic}
    where a citation belongs; W1 supplies the keys.
  - Report negative and null results plainly (K5). Separate results from interpretation.
  - Plain, short sentences. No "novel", "first" or "significant" (unless it is a statistical test
    with its test named).
Step 3 - Self-check. In <check>, for every sentence with a claim: the evidence item it
  rests on, or "RETRACTED" if none (then remove it from the draft). List any sentence that
  conflicts with document 3.

Output: <evidence>, <missing_macros>, the LaTeX in <draft>, <check>. Nothing else.
If the evidence does not support a section the outline asks for, say so instead of
writing it.
```

### 4.2 Hostile-reviewer critique (run in a fresh subagent: `Read, Grep, Glob` only)

```text
<documents>
  <document index="1"><source>04-paper/main.pdf text or sections/*.tex</source><content>{PAPER}</content></document>
  <document index="2"><source>04-paper/generated/numbers.tex</source><content>{MACROS}</content></document>
  <document index="3"><source>Empirical Standards: General, Benchmarking, Repository Mining, Engineering Research (essential attributes + invalid criticisms)</source><content>{STANDARDS excerpt}</content></document>
</documents>

You are Reviewer 2 on the {ESEM|ICPE} program committee. You are expert in performance
measurement (benchmark noise, repetitions, A/A tests, CIs; Kalibera & Jones; Georges et
al.) and in mining software repositories. You lean towards rejection and read for the weakest
link. You have NOT seen the authors' notes, only this paper.

Review it as follows:
1. Summarize the claimed contributions in 3 sentences, in your own words. If you cannot,
   that is finding #1.
2. Build a claim-evidence matrix: every claim in the abstract, introduction and conclusion
   -> the result, table or figure that supports it -> verdict (supported / overstated /
   unsupported). Quote the sentence.
3. Attack measurement: single-laptop WSL2 platform, machine drift, the number of repetitions,
   the A/A noise floor and its sample size, power to detect a 1.2x or 2x slowdown, multiple
   comparisons, CIs on small N (for example, a Wilson interval on 15 edits), and whether
   "executed by a benchmark" is being read as "able to detect a regression".
4. Attack the sample: networkx as the subject, how optimization edits were identified
   (regex precision, number of raters, kappa), replayed historical commits as a stand-in
   for an optimization session, profiles taken at one base state.
5. Attack novelty: which prior work on performance-test selection or benchmark coverage
   you expect to see compared against, and whether the paper oversells.
6. Check reproducibility: the artifact, raw data, pinned versions, and whether you could
   rerun it.
Rules: do not demand a different study (Empirical Standards "invalid criticisms"); do
not invent literature. When you name a paper you believe exists, mark it [verify]. Do not
praise.
Output: each comment as `[severity: critical|major|minor] §loc - observation - standard
or criterion violated - why it matters - requested change`, sorted by severity, then a
recommendation (accept / weak accept / weak reject / reject) with one sentence why, and
the 3 changes that would most move your score.
```

### 4.3 Empirical-Standards checklist pass

```text
<documents>
  <document index="1"><source>04-paper/sections/*.tex</source><content>{PAPER}</content></document>
  <document index="2"><source>EmpiricalStandards GeneralStandard.md</source><content>{fetched text}</content></document>
  <document index="3"><source>EmpiricalStandards Benchmarking.md</source><content>{fetched text}</content></document>
  <document index="4"><source>EmpiricalStandards RepositoryMining.md</source><content>{fetched text}</content></document>
  <document index="5"><source>EmpiricalStandards EngineeringResearch.md</source><content>{fetched text}</content></document>
</documents>

Apply the four standards above to the paper. Use the standards' own wording, from
documents 2-5. Do not use any other version of them.
For EVERY Essential attribute in documents 2-5, output one row:
  standard | attribute (quoted, short) | status: MET / PARTLY / NOT MET / N.A. |
  where in the paper (section + quoted sentence) | what is missing | smallest fix.
"N.A." needs a reason. For example, Engineering Research applies to the A4 policy and the
reduction arms (RQ4), but not to RQ2's coverage measurement.
Then list the Desirable attributes we already meet (such as registered or pre-registered
protocol, deviation log, multiple raters, released artifact) and any we could
meet cheaply.
Pay particular attention to these Study 1 items:
  - Benchmarking: repetitions and duration for every timing claim; a fair comparison
    between arms (interleaved A/B, ABBA); construct validity of the "detects slowdown"
    measure.
  - Repository Mining: unit of analysis (edit = commit? function?); the inclusion rule for
    "optimization edit"; inter-rater reliability; regex-precision audit.
  - General: the assumptions of statistical tests are stated and checked (Mann-Whitney,
    Wilson); limitations disclosed; no misleading visuals (axis ranges, single-pass bars).
Output: the table, then a list of fixes ordered by effort, the smallest first. Do not rewrite
the paper.
```

### 4.4 Related-work synthesis with citation tracing

```text
<documents>
  <document index="1"><source>01-literature/closest-works.md</source><content>{…}</content></document>
  <document index="2"><source>01-literature/database-search-2026-11-21.md and W1 novelty-search record</source><content>{…}</content></document>
  <document index="3"><source>04-paper/refs.bib</source><content>{…}</content></document>
  <document index="k"><source>{citekey}: full text or abstract read by W1 ({URL or DOI}, fetched {date})</source><content>{…}</content></document>
  ... one document per cited paper ...
</documents>

Write the Related Work section (LaTeX) for the paper, grouped by these themes:
(a) regression test selection and its end-to-end overhead; (b) performance-test and
benchmark selection or prioritization; (c) benchmark coverage of code changes and
microbenchmark suite quality; (d) performance-measurement methodology (noise, repetitions,
A/A); (e) LLM and automated code-optimization pipelines and how they validate edits.
Mention (e) only as a validation context. This paper's method uses no AI.

Hard rules:
- You may cite ONLY keys that exist in document 3 AND have a source document (index >= 4).
  Never cite from memory. If a theme needs a paper we do not have, write
  \citeneeded{description} and add it to <search_requests>.
- For every sentence that describes a paper, give in <trace> the citekey and a word-for-word
  quote (at most 25 words) from that paper's document that supports the sentence. If you
  find no supporting quote, delete the sentence.
- Do not claim we are "first" or that a "gap" exists unless document 2 records a search that
  supports it. Quote that record. Otherwise, use "to our knowledge, prior work has not
  measured X for Python optimization edits", and only if document 2 allows even that.
- For each theme, end with one sentence that relates it to our work, using only claims
  allowed by pm/tpm-paper-plan.md §4.
Output: <draft> (LaTeX), <trace> (sentence -> citekey -> quote), <search_requests>,
<bib_problems> (keys whose bib entry is missing a DOI/venue/year, or contradicts the source).
```

### 4.5 Threats-to-validity drafting

```text
<documents>
  <document index="1"><source>pm/advisor/paper-plan-advice.md §3 threats table</source><content>{…}</content></document>
  <document index="2"><source>pm/tpm-paper-plan.md risk register (R-1..R-8) and §4 must-not-claim</source><content>{…}</content></document>
  <document index="3"><source>03-experiment/results/results.md deviation log + A/A + drift sections</source><content>{…}</content></document>
  <document index="4"><source>04-paper/generated/numbers.tex</source><content>{MACROS}</content></document>
  <document index="5"><source>04-paper/sections/{design,results}.tex</source><content>{…}</content></document>
</documents>

Draft the Threats to Validity section in LaTeX. Use four subsections in Wohlin et al.'s
classification, in this order: construct, internal, external, conclusion. Add a short
"reliability / research process" paragraph covering artifacts, deviations from the
pre-registration, and disclosure of AI assistance in tooling and writing.
For each threat:
  1. Name the specific threat in this study. Do not list generic textbook threats. Follow
     Verdecchia et al. 2023: if a threat would apply to any paper, drop it.
  2. Say which result or RQ it affects, and in which direction it could bias that result.
  3. Describe the mitigation we actually applied. It must be stated in documents 3-5;
     quote where. A mitigation that is planned but not done is written as a limitation,
     not as a mitigation.
  4. Say what remains (the residual threat), with a macro for any number.
Must cover at least: B1 rests on one project and few edits (with its CI); replayed
historical commits stand in for a session; static vs. profiled reach, with the
profile taken at one base state; "executed" vs "able to detect" (Sjøberg & Bergersen construct
validity); synthetic slowdowns as probes and not as models of real regressions; machine drift on
one WSL2 laptop (timings are reported as ranges); low power of 6-vs-6 comparisons;
multiplicity across off-target comparisons; regex precision when mining edits;
post-hoc analyses and deviations from the pre-registration.
Rules: every number is a macro; no new claims; do not soften anything in document 2's
must-not-claim list.
Output: <draft>, then <trace> (threat -> mitigation quote -> file), then <unmitigated>
(threats with no applied mitigation, for the PM).
```

### 4.6 Orchestration (suggested loop for W6)

For each section:
1. Draft it with template 4.1.
2. Run `make check` (the macro/digit lint from TPM §5).
3. Get a critic pass.
4. Run the hostile reviewer (4.2, fresh subagent) on the whole paper at the outline, mid-draft and full-draft stages.
5. Run the checklist pass (4.3) once the draft is full.
6. Get the advisor-persona review (TPM §5).
7. Revise. These are separate calls, as in the "chain complex prompts" self-correction pattern in Anthropic's best-practices guide.

For a second, independent opinion, also run Deep Review if the owner installs it.

---

## 5. What to avoid

1. **Fabricated or misattributed citations.**
   - Never cite from model memory. This applies even to titles that look certain, such as the "titles from memory" in TPM R-6. Every `refs.bib` entry needs a fetched source: a DOI that resolves, or a publisher or arXiv page that was read.
   - Each entry gets a `note = {verified <date> via <URL>}` field.
   - Template 4.4 enforces sentence → citekey → quote.
   - The pages behind the [S] items in §1e must be fetched before they are cited. Georges et al. has two candidate DOIs.
2. **Unverifiable or hand-typed numbers.**
   - Every number comes from `numbers.tex`, and every macro carries a comment naming its raw file and its computation, plus the sha256 from `data-manifest.yaml`.
   - The text never shows a point value for something the data gives only as a range (drift, R1 8–28×).
   - `make check` must pass before any review.
3. **Claims beyond evidence.**
   - The 16-item must-not-claim list (TPM §4) is pasted into every drafting and review prompt.
   - Banned without a recorded novelty search: "most", "first", "novel", "gap", "significant" (unless it names a test).
4. **Models filling silence.**
   - Every template lets the model say "missing" or "not supported", and asks for `<missing_macros>`, `<search_requests>` and `<unmitigated>` instead of invented content (Reduce hallucinations: allow "I don't know").
5. **Style tools that change meaning.**
   - Do not run anti-ai-writing-style rewriters over claims, hedges or numbers.
   - Language polishing is the last step, and a diff is checked against macros and hedges afterwards.
6. **Reviewer echo.**
   - The reviewer subagent must not see the drafting conversation or the PM's notes. It sees only the paper and the standards.
   - Do not hand it our own threats table (advisor §3) first, or it will confirm that table instead of finding new attacks. Compare the two afterwards.
7. **Running downloaded code**, such as K-Dense's scripts, without the owner's approval.
8. **Uploading the draft** to third-party services (letX, Overleaf, remote citation checkers) without the owner's approval.
9. **AI-use disclosure.**
   - Follow the chosen venue's policy, and check it when the CFP is verified.
   - The owner re-derives every headline number from the raw files before submission (advisor §3, last row).

---

## 6. Sources read (fetched 2026-11-22 unless marked [S]/[U])

Anthropic:
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
- https://platform.claude.com/docs/en/build-with-claude/citations
- https://platform.claude.com/docs/en/resources/prompt-library/library (redirects to best practices)
- https://github.com/anthropics/skills
- https://github.com/anthropics/skills/tree/main/skills
- https://raw.githubusercontent.com/anthropics/skills/main/README.md
- https://raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md
- https://raw.githubusercontent.com/anthropics/skills/main/skills/docx/LICENSE.txt
- https://github.com/anthropics/knowledge-work-plugins
- https://github.com/anthropics/claude-plugins-official
- https://raw.githubusercontent.com/anthropics/claude-plugins-official/main/plugins/math-proof/README.md
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents

Community:
- https://github.com/K-Dense-AI/claude-scientific-skills
- …/skills/peer-review/SKILL.md
- …/skills/citation-management/SKILL.md
- https://github.com/leiverkus/research-superpowers
- https://github.com/dipakkrishnan/deep-review-skill
- https://github.com/ComposioHQ/awesome-claude-skills
- https://github.com/travisvn/awesome-claude-skills
- Research Desk: in the claude.ai catalog (author Naji Kayal); no public repo found [U]

Standards and methodology:
- https://github.com/acmsigsoft/EmpiricalStandards
- https://www2.sigsoft.org/EmpiricalStandards/
- raw `docs/standards/{GeneralStandard,EngineeringResearch,Benchmarking,RepositoryMining,OptimizationStudies,DataScience}.md` under https://raw.githubusercontent.com/acmsigsoft/EmpiricalStandards/master/
- https://conf.researchr.org/track/eseiw-2026/eseiw-2026-esem---registered-reports-track
- https://2027.msrconf.org/track/msr-2027-registered-reports
- https://d3s.mff.cuni.cz/publications/papadopoulos_methodological_2019/
- [S]: Wohlin 2nd ed. DOI; Verdecchia et al. 2023; Sjøberg & Bergersen (TSE, EASE 2023); Kalibera & Jones 2013; Georges et al. 2007; ACM badging pages (403); SIGSOFT review tool page.

Catalog searches: `SearchSkills`, `SearchPlugins` (×2), `ListSkills`, `ListPlugins`, run in this session on 2026-11-22.
