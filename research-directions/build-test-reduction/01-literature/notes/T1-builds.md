# T1 - Reduced / incremental builds: literature notes

Date of research: 2026-11-21. Scope: build-system theory, build-dependency-error studies, build avoidance/caching, Python/Cython build pitfalls.

Label legend: [read-in-source] = I read the passage in the downloaded PDF or fetched page (location given). [read-via-fetch] = a web page/source file fetched through WebFetch, whose tool returns an extract/summary of the page (treat quotes as paraphrase-level; re-check before quoting verbatim). [abstract-only] = only abstract/metadata seen. [inferred] = my reasoning. [unknown] = not verified.

Page numbers for the JFP paper are the journal page numbers printed in the PDF (Cambridge pagination). For other PDFs I give section numbers.

---

## (a) Source cards

### A1. Mokhov, Mitchell, Peyton Jones - Build Systems a la Carte (ICFP 2018) and "theory and practice" (JFP 2020)
- Citations: Mokhov, A., Mitchell, N., Peyton Jones, S. "Build systems a la carte." Proc. ACM Program. Lang. 2(ICFP), Article 79, 2018. DOI 10.1145/3236774. Expanded: "Build systems a la carte: theory and practice." J. Functional Programming 30, e11, 2020. DOI 10.1017/S0956796820000088.
- Files: `papers/2018-Build-Systems-a-la-Carte.pdf`, `papers/2020-Build-Systems-a-la-Carte-JFP.pdf`. I read the JFP version; the ICFP PDF was downloaded and text-extracted but I did NOT read passages from it (ICFP content below is [abstract-only] / via search metadata).
- Minimality: "A build system is minimal if it executes tasks at most once per build, and only if they transitively depend on inputs that changed since the previous build." [read-in-source: JFP p.4, Sec. 2.1]. Make's minimality relies on file modification times; footnote: Make "is therefore minimal only under the assumption that you do not" alter mtimes with `touch` [read-in-source: JFP p.5, footnote 5].
- Early cutoff: if a comment is added to main.c, the rebuild stops after detecting main.o is unchanged, so main.exe and dependents are not rebuilt [read-in-source: JFP p.6, Fig. 3, Sec. 2.3]. Make cannot do this natively; Shake and Bazel can [read-in-source: Sec. 2.3/2.4 table, p.7-9, approx.].
- Correctness definition (Sec. 3.6, pp.15-16): after the build, (i) inputs in the result equal inputs in the initial store; (ii) for every non-input key, recomputing its task on the result store gives the stored value (`getValue k result == compute task result`). Stated as holding only for acyclic task descriptions; adjusted for non-determinism and shallow cloud builds (Sec. 8.3, 8.4) [read-in-source].
- Rebuilders / traces: verifying traces record hashes of dependencies used last time; a key is rebuilt if any differs (Sec. 5.2, pp.23-24). Constructive traces also store the result so it can be shared (cloud builds) (Sec. 5.3). Dirty-bit rebuilders can reach minimality and early cutoff if the bit is cleared when the value did not change (Sec. 5.1) [read-in-source].
- Impurity (Sec. 8.3): tasks may have "untracked dependencies" - e.g. a C compile lists source.c but not the version of gcc; non-determinism; volatility. Bazel's sandboxing "guard[s] against missing dependencies, but none are likely to capture all dependencies right down to the CPU model and microcode version." Buck assumes task determinism to cut cloud lookups [read-in-source].
- Relevance: gives the formal yardstick ("equal to recompute from scratch") that a reduced-build rule must be judged against; shows timestamps weaken minimality/correctness and hashes are preferred.

### A2. Spall, Mitchell, Tobin-Hochstadt - Build Scripts with Perfect Dependencies (OOPSLA 2020; Rattle)
- Citation: Spall, S., Mitchell, N., Tobin-Hochstadt, S. "Build scripts with perfect dependencies." Proc. ACM Program. Lang. 4(OOPSLA), 2020. DOI 10.1145/3428237 (DOI as listed on the arXiv page per search result); arXiv:2007.12737.
- File: `papers/2020-Build-Scripts-Perfect-Dependencies.pdf` (25 pages; the arXiv text carries a placeholder "Article 1, January 2016" footer, so use the ACM version for page citations). Dependencies are inferred by tracing a build script's commands instead of being declared; parallelism is recovered through speculation (abstract, via search result) [abstract-only]. Hazards: "Writing to a file after it has already been either read or written is the only circumstance in which a build, where every individual command is well-formed ..., is incorrect"; read-then-write and write-then-write hazards are defined there (Sec. 2.4-2.6) [read-in-source, text extract].

### A3. Spall, Mitchell, Tobin-Hochstadt - Forward Build Systems, Formally (CPP 2022)
- Citation: Spall, S., Mitchell, N., Tobin-Hochstadt, S. "Forward build systems, formally." CPP '22, pp. (pages not verified), 2022. DOI 10.1145/3497775.3503687 (from OpenAlex URL in search results); arXiv:2202.05328. File: `papers/2022-Forward-Build-Systems-Formally.pdf`.
- Correctness: "A forward build system is correct if, for every build, it either produces the same result as running the commands in order, or reports an error." [read-in-source: Sec. 1].
- Hazards (read-before-write, write-before-write, speculative write-before-read) detect bad behaviour; absence of hazards implies correct [read-in-source: Sec. 2.1, partially read].
- Key assumption: Rattle "assumes tracing data is complete and correct, if it is not, then Rattle might make the wrong decision about when to re-run commands and which commands it is safe to run in parallel" [read-in-source: Sec. 2, tracing paragraph].
- Intro states that omitted/incorrect dependencies lead to "failure to rebuild in the presence of changes (often requiring a 'clean' step) to outright incorrect results", citing Licker & Rice [read-in-source: Sec. 1].
- Relevance: a "forward" model (a script of commands, memoized by traced reads/writes) is the closest formal fit to an agent that applies edits and runs build commands.

### A4. Erdweg, Lichter, Weiel - Pluto (OOPSLA 2015)
- Citation: Erdweg, S., Lichter, M., Weiel, M. "A sound and optimal incremental build system with dynamic dependencies." OOPSLA 2015, pp. 89-106. DOI 10.1145/2814270.2814316. File: `papers/2015-Pluto-Erdweg-OOPSLA.pdf`.
- Definitions: sound = after a build, generated files consistently reflect the latest sources; optimal/efficient = rebuild as few units as possible; formalized in Sec. 4, rebuild algorithm verified in Sec. 5 [read-in-source: abstract and Sec. 1 contribution list].
- Argues that Make's static declared dependencies force over-approximation, "as a missing dependency makes the build script unsound"; Shake is non-optimal because it rebuilds as soon as last-modified time of a dependency changes [read-in-source: Sec. 1-2].
- Relevance: supports fine-grained, dynamically discovered dependencies (file-level and builder-level) rather than coarse static rules.

### A5. Licker, Rice - Detecting Incorrect Build Rules (ICSE 2019)
- Citation: Licker, N., Rice, A. "Detecting incorrect build rules." ICSE 2019, pp. 1234-1244. DOI 10.1109/ICSE.2019.00125. File: `papers/2019-Licker-Detecting-Incorrect-Build-Rules.pdf`.
- Method "build fuzzing": infer a dependency graph by tracing system calls during a CLEAN build; then modify each input file, run an incremental build, compare the set of changed outputs to the set expected from the graph [read-in-source: Abstract, Sec. III].
- Result: issues in 30 open-source projects (the search-engine summary said 31; the PDF abstract says 30) [read-in-source: Abstract, Sec. VII conclusion]. Tool overhead: ptrace slows builds "by a factor of two" on clean 4-thread builds [read-in-source: discussion section]. They note false positives from over/under-constrained graphs and Unix pipes [read-in-source: Sec. III-IV].
- Example in intro: a CMake rule lists the template input but not the Python generator script nor the Python files it imports; edits to those scripts do not regenerate output [read-in-source: Sec. I]. A table lists "python import" among issue categories [read-in-source: results table].
- Relevance: the differential method (touch/modify input -> incremental build -> compare to expectation) is directly reusable as a periodic safety check; also generated code driven by Python scripts is a known blind spot.

### A6. Sotiropoulos, Chaliasos, Mitropoulos, Spinellis - A Model for Detecting Faults in Build Specifications (OOPSLA 2020; BuildFS)
- Citation: Proc. ACM Program. Lang. 4(OOPSLA), Article 144, 2020. DOI 10.1145/3428212. File: `papers/2020-Sotiropoulos-BuildFS.pdf`.
- Approach: analyse ONE full build's file-system operations, translate to the BuildFS model, check for violations of each task's declared inputs/outputs (faults for incremental and parallel builds). 612 Make and Gradle projects; 247 issues in 47 projects confirmed and fixed; median/mean speedup 39x/74x over a state-of-the-art Make tool [read-in-source: Abstract].
- Relevance: a single traced build suffices to validate the declared dependency set - cheaper than clean-vs-incremental fuzzing.

### A7. Lyu, Li, Zhang, Zhang, Rong, Rigger - Detecting Build Dependency Errors in Incremental Builds (arXiv 2024; EChecker)
- Citation: arXiv:2404.13295 (cs.SE), v2 April 2024. Authors as listed on arXiv page. Publication venue not verified [unknown]. File: `papers/2024-Detecting-Build-Dependency-Errors-Incremental-Builds.pdf`.
- The v2 PDF I first downloaded was truncated/corrupt; I replaced it with arXiv v1 (`papers/2024-Detecting-Build-Dependency-Errors-Incremental-Builds-v1.pdf`, 12 pages), which opens correctly. Read: abstract and the "Evaluation results" discussion [read-in-source, v1]. Make/C/C++; MDs and RDs are the most prevalent errors; state-of-the-art detectors need clean builds ("up to a few hours for large-scale projects"); EChecker updates actual build dependencies from C/C++ preprocessor directives and Makefile changes in new commits, "which avoids clean builds when possible"; 12 projects, 240 commits; in the evaluation discussion 2,298 errors detected with 32 false positives. Efficiency numbers (F-1 +0.18; 85.14x average, 16.30x median) come from the arXiv v2 abstract page [abstract-only]; v1 may differ. Venue [unknown].
- Relevance: a per-commit (per-edit) dependency-error check - the same granularity our study needs - but C/C++ + Make only.

### A8. Bezemer, McIntosh, Adams, German, Hassan - Unspecified dependencies in make-based build systems (EMSE 2017)
- Citation: Empirical Software Engineering 22(6):3117-3148, 2017. DOI 10.1007/s10664-017-9510-8. File: `papers/2017-Bezemer-Unspecified-Dependencies-Make-EMSE.pdf`.
- GLIB, OpenLDAP, Linux, Qt; "6 common causes in more than 1.2 million unspecified dependencies" [read-in-source: Abstract]. Incomplete rules make incremental builds omit necessary commands, so "sources and deliverables [are] out-of-sync"; the "industry standard" workaround is to remove all generated files and do a full build, or run the incremental build repeatedly until a fixed point [read-in-source: Sec. 1].

### A9. Esfahani et al. - CloudBuild (ICSE SEIP 2016)
- Citation: "CloudBuild: Microsoft's distributed and caching build service." ICSE '16 Companion, 2016. DOI 10.1145/2889160.2889222 (from search result). First author Hamed Esfahani; full author list not verified here. File: `papers/2016-CloudBuild-Esfahani-ICSE-SEIP.pdf`.
- Caching is content-based: whether to run a project or reuse earlier outputs is decided from the pertinent source files and parent projects (Sec. 1-2) [read-in-source].
- Sec. 3.4: each task runs in a sandbox (directory of symlinks to declared + inferred inputs); "any missed dependencies will be runtime errors"; file accesses observed with Detours binary injection and accesses beyond predicted ones are surfaced as errors. They state mistakes in dependencies "will lead to false cache fingerprints and hence false cache hits", and that some tools produced non-deterministic outputs [read-in-source: Sec. 3.4, Sec. 1].
- Speed-ups 1.3x-10x: [abstract-only] (search metadata; the PDF text has dropped digits so I could not confirm numbers in the body).

### A10. Gallaba, Ewart, Junqueira, McIntosh - Kotinos (TSE 2020/2022)
- Citation: "Accelerating continuous integration by caching environments and inferring dependencies." IEEE Trans. Softw. Eng. (early access 2020; volume 48, pp. 2040-2052 per search metadata, 2022). DOI not verified. File: `papers/2020-Gallaba-Kotinos-TSE.pdf`.
- Infers the build dependency graph (BDG) from system-call traces of a cold build; skips unaffected steps in warm builds; "To avoid incorrect build behaviour, BDG-based acceleration is bypassed for commits that will likely modify the structure of the BDG (e.g., those that add or rename files)" [read-in-source: Sec. 4 approach]. 14,364 CI build records, >=87.9% builds get an acceleration; 74% of accelerated builds >=2x faster; median CPU <1%; "does not compromise build outcomes" [read-in-source: Abstract].
- Stated preconditions (Future-work section after Sec. 9): deterministic dependency resolution with pinned lock files; isolated, idempotent test suite; minimal conditional behaviour during the build (dynamic analysis may be incomplete) [read-in-source].

### A11. Ghaleb, da Costa, Zou - The Promise and Reality of CI Caching (arXiv 2601.19146; EASE '26 per arXiv page)
- File `papers/2026-Promise-Reality-CI-Caching.pdf` (12 pages, arXiv v2, 19 Mar 2026). 513,384 Travis CI builds, 1,279 projects; ~30% adopt caching; only 24% of adopters maintain the cache configuration (Obs. 2.1, Sec. 4.2.3); "27% of the studied projects have unused dependencies in the CI cache" and caching frequently updated dependencies "can leave outdated versions" (Obs. 4.3, RQ4) [read-in-source]. This is unused/outdated cache content, not a measured wrong-result rate. Venue acceptance (EASE '26) is from the arXiv listing only.

### A12. ccache manual (what is hashed; direct-mode unsafety)
- URL: https://ccache.dev/manual/latest.html [read-via-fetch].
- Hashed in both modes: compiler name, compiler size+mtime by default (`compiler_check` = mtime; alternatives content, none, string, command), current directory if `hash_dir` (default on, for -g builds), contents of `extra_files_to_hash`. Preprocessor mode adds the `-E` output and command-line options; direct mode adds the source file and options plus a manifest of include-file hashes.
- Unsafety: direct mode "fails to pick up new header files in some rare scenarios" (headers that would have been read had they existed are not recorded). `sloppiness` options (file_stat_matches, time_macros, include_file_mtime, etc.) trade correctness for hit rate. Direct mode is disabled when `__TIME__` appears.

### A13. sccache README
- URL: https://github.com/mozilla/sccache (README.md) [read-via-fetch].
- Absolute paths must match for a hit by default (`SCCACHE_BASEDIRS` normalizes); flags hashed verbatim; Rust crates that invoke the system linker (bin, dylib, cdylib, proc-macro) are not cacheable; incrementally compiled crates not cached by default; C++20 module flags bypass the cache.

### A14. Bazel docs - hermeticity and remote caching
- https://bazel.build/basics/hermeticity [read-via-fetch]: hermetic = same output for same source and configuration; sources of non-hermeticity (timestamps/build IDs, host binaries, absolute paths, writing to the source tree); detection suggestions: null sequential builds, comparing local cache hits across machines, build in a container with only the checkout, remote execution + sandboxing.
- https://bazel.build/remote/caching [read-via-fetch]: action cache maps action hashes (inputs, output names, command line, env vars) to results; only `--action_env` variables count; tools outside the workspace are not tracked, so users with different compilers "will wrongly share cache hits"; changing inputs during a build can upload invalid results (`--experimental_guard_against_concurrent_changes`).
- Buck2 and Pants docs: NOT read in this run [unknown].

### A15. Python / Cython / packaging mechanisms
- setuptools/distutils build_ext (source file `setuptools/_distutils/command/build_ext.py`, main branch) [read-via-fetch]: `depends = sources + ext.depends`; extension is skipped unless `self.force` or `newer_group(depends, ext_path, 'newer')` - i.e. an mtime comparison at whole-extension granularity; otherwise logs "skipping ... (up-to-date)". Headers are NOT automatically included - they must be listed in `depends` [inferred from the code plus the distutils-sig threads below]. The setuptools user guide page (ext_modules) says nothing about this [read-via-fetch: no statement found].
- distutils-sig threads (2006 "include files with C extensions"; 2016 cython-devel "Static checker for cython extension dependencies?") and a CPython tracker issue "Make extensions depend on header files" (python-bugs-list 2021-10) report stale builds when headers change [abstract-only: seen as search-result snippets, not opened].
- Cython `cythonize` (source: `Cython/Build/Dependencies.py`, master) [read-via-fetch]: regenerates a .c/.cpp if forced (env `CYTHON_FORCE_REGEN=1`), if missing or generated by another Cython version, or if `c_timestamp < newest dependency timestamp`, where dependencies are the .pyx plus transitively cimported .pxd files and `include`d files (`DependencyTree.immediate_dependencies`). `cdef extern from` headers are added to the Extension's `depends`, but the extracted code shows `m.depends` is not used in the timestamp comparison. No tracking of changes to compile_time_env/directives seen in the recompile decision (they enter only the cache fingerprint). The user-guide page documents dependency tracking only for pyximport (.pyxdep files).
- PEP 552 (https://peps.python.org/pep-0552/) [read-via-fetch]: .pyc invalidation modes - timestamp (default; header stores source mtime+size), checked hash (hash compared on import), unchecked hash (never re-checked; an external system must keep them fresh). `compileall --invalidation-mode`; interpreter `--check-hash-based-pycs {default,always,never}`. The fetched summary did not mention SOURCE_DATE_EPOCH.
- meson-python editable installs (https://mesonbuild.com/meson-python/how-to-guides/editable-installs.html) [read-via-fetch]: a stub rebuilds compiled parts at first import in each interpreter; build deps must stay installed (use `--no-build-isolation`); build dir (default `build/<ABI tag>`) must remain; reinstall needed for entry points, new dependencies, metadata changes. The page does not say whether edits to meson.build/new files are picked up [unknown].
- scikit-build-core editable (https://scikit-build-core.readthedocs.io/en/latest/configuration/editable.html; fetched page was the configuration index) [read-via-fetch]: redirect mode serves Python files live; rebuild-on-import is "experimental"; some entries are snapshots refreshed only on reinstall. Search snippets (not opened): a compiled extension already loaded cannot be unloaded, so rebuild takes effect only in a new process; new files require reinstall [abstract-only].
- uv cache (https://docs.astral.sh/uv/concepts/cache/) [read-via-fetch]: for directory dependencies uv's cache validity keys on the mtime of pyproject.toml, setup.py or setup.cfg (plus src dir add/remove); "may cause fewer reinstalls than you want"; `tool.uv.cache-keys` (file/git/env/dir) replaces defaults; explicitly passed local dirs are always rebuilt. Nothing specific on compiled extensions.
- pip wheel cache, importlib caches, `python -X` flags: NOT researched [unknown].

### A16. Not verified / not found
- "Escaping dependency hell" (as suggested in the brief): not found by any search; not cited.
- Gallaba et al. "Lessons from Eleven Years of CI build failures": no such title found. A search returned "Lessons from Eight Years of Operational Data from a Continuous Integration Service: A Case Study of CircleCI" (Gallaba, Lamothe, McIntosh); only a title snippet seen, abstract not read; NOT cited as evidence.
- Buck2/Pants/BuildXL docs, MkCheck (ISSTA 2020) body: not read. MkCheck appears only as a search-result mention [abstract-only].

---

## (b) Synthesis

| Technique | What is reduced | Granularity | Safety assumption | Overhead (location) | Python support |
|---|---|---|---|---|---|
| Make-style timestamp rebuild (A1) | Targets whose inputs' mtime is newer | File/target | Declared deps complete; mtimes monotone and not touched (A1 fn.5, p.5) | n/a | distutils build_ext / cythonize use the same scheme (A15) |
| Verifying traces / hash-based (Shake, Bazel; A1 Sec. 5.2) | Tasks whose recorded dependency hashes changed | Task/action | Task deterministic; deps tracked (A1 Sec. 8.3) | storage of traces (not quantified) | not Python-native |
| Early cutoff (A1 Sec. 2.3) | Dependents when a rebuilt output is byte-identical | Task | Needs content hashes of outputs | none stated | e.g. comment-only .pyx edit still regenerates .c under mtime scheme [inferred] |
| Constructive traces / remote cache (A1 Sec. 5.3; A9; A14) | Whole actions via cache hit | Action | Complete action key; deterministic tools; hermetic inputs (A14) | not quantified here | via Bazel rules only |
| Pluto dynamic deps (A4) | Rebuild only builders whose observed reads changed | File + builder | Builders report all reads/writes | not read | none |
| Traced/forward builds (Rattle A2/A3; Kotinos A10) | Commands whose traced inputs unchanged | Command/step | Tracing complete (A3 Sec. 2); no structure change (A10 Sec. 4) | Kotinos <1% median CPU (A10 abstract); ptrace tracing 2x clean build (A5) | language-agnostic |
| ccache/sccache (A12, A13) | Compiler invocations | Translation unit | Hash covers all inputs; compiler identified by mtime+size by default (A12) | not quantified | caches the C compile step of extensions |
| Cython dependency tracker (A15) | .pyx -> .c regeneration | Module | .pxd/include tracked; C headers via depends | n/a | native |
| setuptools build_ext (A15) | Compile+link of an extension | Whole extension | mtime of sources+depends | n/a | native |
| Rebuild-on-import editable (meson-python A15) | Ninja incremental rebuild at import | Target | Build dir + build deps present | "usually small" (A15, qualitative) | native |

Key theoretical point [inferred from A1 Sec. 3.6, A3 Sec. 1]: a reduced build is acceptable iff its output store equals (or is observationally equivalent to) what a full build would produce; all surveyed systems achieve that only under "declared/traced dependencies are complete" plus "tasks are deterministic".

## (c) Unsafety causes and detection

Causes (with sources):
1. Missing/unspecified dependencies - incl. generator scripts and their imports (A5 Sec. I, results table), unspecified .so/header deps (A8), generated files (A8, A5).
2. Redundant deps -> unneeded rebuilds, not unsafe but costly (A7 abstract, A5).
3. Timestamps: touch/clock skew defeat Make-style minimality (A1 fn.5); ccache `file_stat_matches` and compiler mtime+size identity (A12); uv uses mtime of three files (A15).
4. Untracked environment: compiler version, flags, env vars, PATH (A1 Sec. 8.3; A14 remote caching known issues; A12 `compiler_check`; A13 flags hashed verbatim).
5. Non-determinism / volatility: timestamps/build IDs in outputs, `__TIME__` (A14, A12, A1 Sec. 8.3, A9).
6. New files / renamed files / new include-path headers: ccache direct mode misses new headers (A12); Kotinos bypasses acceleration when graph structure changes (A10); editable installs need reinstall for new files (A15 search snippet, A15 meson page).
7. Stale caches: 27% of studied Travis projects have unused dependencies in the CI cache and caches are rarely maintained (A11 RQ4, Sec. 4.2.3); outdated cached versions are possible.
8. Dynamic-analysis incompleteness: tracing sees only exercised paths (A10 future-work; A3 Sec. 2).
9. Process state: loaded extension modules cannot be reloaded in the same interpreter (A15 snippet) [abstract-only].

Detection methods:
- Build fuzzing: modify an input, incremental build, compare to expected set from traced graph (A5).
- Single-build trace checking against declared spec (BuildFS, A6); per-commit inference without clean build (EChecker, A7).
- Conceptual-vs-concrete dependency graph comparison (A8).
- Hermetic sandbox exposing missed deps as runtime "file not found" (A9 Sec. 3.4; A14 remote execution).
- Null sequential build check; cross-machine cache hit comparison; containerized build with only checkout (A14).
- Hazard detection (read-before-write etc.) in forward builds (A3 Sec. 2.1).
- Differential clean-vs-incremental output comparison: practiced informally ("remove all generated files and do a full build", A8 Sec. 1), and the formal criterion is A1 Sec. 3.6. No paper read gives a prescribed sampling schedule for this [unknown].

## (d) Assumptions likely to break under accumulated performance-motivated edits [inferred]

- Compiler/linker flag edits (-O levels, -march, LTO, -fno-semantic-interposition) live in setup.py/pyproject/meson.build, not in any file `newer_group` or cythonize watches; distutils' check is mtime of sources/depends vs the .so only (A15), so a flags-only change can leave a stale .so. Hash-based systems must include flags in the action key (A14, A13).
- Editing a .pxd or a C header changes behaviour of other modules (ABI/struct layout/inline functions); cythonize tracks .pxd (A15) but build_ext does not track headers unless `depends` is set (A15). Struct-layout changes can make unchanged dependent extensions binary-incompatible (stale .so with wrong offsets) [inferred; no source read].
- New C extension module or new file: dependency graph structure changes; Kotinos bypasses acceleration then (A10); editable installs need reinstall (A15).
- Cython directive/compile_time_env changes (e.g. boundscheck=False) may not trigger regeneration (A15 Dependencies.py) [partly read-via-fetch; verify empirically].
- Generated code (Cython .c, templated sources) checked in or left in the tree: stale generated files (A5, A8).
- Cumulative drift: many small edits each declared "safe" can leave build outputs from an earlier state; Rattle-style equivalence to full rerun (A3) is per build, not per sequence - a periodic clean rebuild is the backstop [inferred].
- Timestamps under agent workflows: git checkout/patch application and reverting edits can set mtimes older than the .so, so reverting a .pyx may not rebuild (mtime comparison is "newer than", A15) [inferred].
- Performance measurement validity: a cached/stale binary gives a "speed-up" that is not real - the build must be proven fresh before benchmarking [inferred].
- Python: .pyc timestamp mode compares source mtime+size recorded in header (A15 PEP 552); a same-size edit within the same recorded timestamp second is the classic stale-pyc case [inferred; PEP summary mentions timestamp+size only].

## (e) Candidate deterministic rules (each is a hypothesis to be validated by differential testing, not a proven rule)

R1. Edit touches only `.py` files in pure-Python packages (no generated code from them, not imported by build scripts such as setup.py/conf scripts): no native rebuild. Ensure freshness by running with hash-based pycs `checked-hash` or deleting `__pycache__` of touched files. Sources: PEP 552 (A15); A5 (build scripts importing Python are a hidden dependency, so exclude files imported by setup.py/generators).
R2. Edit touches `.pyx`: re-run cythonize on that module and rebuild only its extension; also rebuild extensions that `cimport` it (use cythonize's own transitive tracker). Sources: A15 Dependencies.py (immediate_dependencies/cimported_files), A1 minimality.
R3. Edit touches `.pxd`, `.pxi`, or any header (`.h`, `.hpp`): rebuild the transitive closure of dependents; since distutils does not track headers unless `depends` lists them, compute dependents with a trace (strace/compiler `-MMD` depfiles) or a conservative rule "all extensions". Sources: A15, A5/A6 (trace-derived dependency sets), A12 (new-header unsafety).
R4. Edit touches `setup.py`, `pyproject.toml`, `meson.build`, `CMakeLists.txt`, `setup.cfg`, compiler flag env, Cython directives, or adds/renames/deletes any source file: full (clean) rebuild of all native extensions. Sources: A10 (bypass when structure changes), A14/A13 (flags in action key), A15 (uv cache keys; editable reinstall needed).
R5. Hash, don't trust mtime: decide "unchanged" by content hash of inputs + flags + toolchain identity (compiler `--version`/content hash, Python ABI tag, Cython version), i.e. a verifying trace. Sources: A1 Sec. 5.2, Sec. 8.3; A12 (`compiler_check`, sloppiness); A14.
R6. Early cutoff: if a regenerated `.c` or object is byte-identical (e.g. comment/docstring-only .pyx edit), skip downstream relink and tests that depend only on it. Source: A1 Sec. 2.3; caveat - Cython embeds line numbers/paths in generated C so identity is rare [inferred].
R7. Periodic backstop: every N edits (and always before reporting a final speed-up) do a clean build in a fresh directory and compare artifacts (hash of .so after normalization, or behavioural equivalence on tests) with the incrementally built tree; any mismatch invalidates the incremental runs since the last clean point. Sources: A1 Sec. 3.6 (definition of correct), A8 Sec. 1 (practice), A5 (differential idea), A14 (null build / clean-container check). N is not given by any source [unknown].
R8. Trace once per structural change: record file reads of the full build (BuildFS/Kotinos style) to derive the file->extension map; reuse it for later edits until structure changes (R4). Sources: A6, A10, A5 (overhead 2x on a clean build).
R9. Sanity guard after each reduced build: null rebuild must be a no-op, and import of the rebuilt module must come from the expected path/ABI (guards against stale .so and editable path issues). Sources: A14 (null sequential build), A15 (editable build-dir/path requirements) [guard design inferred].
R10. Benchmark gating: run benchmarks only on artifacts whose build inputs hash (R5) is recorded; never reuse a cached binary across flag changes. [inferred from A12-A14].

## (f) Search log (all on 2026-11-21)

| # | Engine/database | Query | Notable hits | Looked for, not found |
|---|---|---|---|---|
| 1 | WebSearch | Build Systems a la Carte Mokhov Mitchell Peyton Jones ICFP 2018 pdf | MSR page, JFP PDF at MSR and Cambridge | - |
| 2 | WebSearch | Forward build systems, formally Spall Mitchell Tobin-Hochstadt arXiv | arXiv 2202.05328 | - |
| 3 | WebSearch | Licker Rice "Detecting incorrect build rules" ICSE 2019 | Cambridge PDF; EChecker, MkCheck, BuildFS hits | search summary said 31 projects; paper says 30 |
| 4 | WebSearch | Sotiropoulos "A model for detecting faults in build specifications" OOPSLA 2020 BuildFS | Spinellis PDF, arXiv 2005.06881 | - |
| 5 | WebSearch | Gallaba Accelerating CI by caching environments ... Kotinos | UWaterloo PDF; arXiv 2601.19146 | - |
| 6 | WebSearch | Pluto sound and optimal incremental build system Erdweg OOPSLA 2015 | Mainz PDF | - |
| 7 | WebSearch | CloudBuild Microsoft's distributed and caching build service Esfahani ICSE SEIP 2016 | MSR PDF | exact author list not confirmed |
| 8 | WebSearch | Bezemer unspecified dependencies make-based build systems | EMSE 2017 PDF (UWaterloo) | - |
| 9 | WebSearch | ccache manual direct mode sloppiness hash_dir compiler_check | ccache manuals, mailing-list threads | hash_dir details came from manual fetch |
| 10 | WebSearch | setuptools build_ext does not rebuild when header changes depends newer_group | distutils-sig 2006, cython-devel 2016, bpo 2021 | no current official doc statement |
| 11 | WebSearch | build system incorrect incremental build detection 2022 2023 2025 ... | EChecker 2024, MkCheck ISSTA 2020 | nothing 2025+ specific found |
| 12 | WebSearch | Python extension stale .so editable install rebuild pitfalls | scikit-build-core, meson-python, py-build-cmake pages, bpo msg | header-change tracking not addressed |
| 13 | WebSearch | Gallaba "Lessons from Eleven Years..." | CircleCI eight-year paper (title only) | "Eleven Years" title does not exist in results |
| 14 | WebSearch | Spall Mitchell Tobin-Hochstadt "Build Scripts with Perfect Dependencies" OOPSLA 2020 | arXiv 2007.12737 | - |
| 15 | WebFetch | arxiv.org/pdf/2202.05328 | binary only (saved) | summarizer could not decode; read via pdftotext instead |
| 16 | WebFetch | ccache.dev/manual/latest.html | hashing/direct mode/sloppiness | - |
| 17 | WebFetch | cython readthedocs source_files_and_compilation (2 fetches) | pyximport dependency docs only | cythonize dependency/force doc not on page |
| 18 | WebFetch | mesonbuild.com meson-python editable-installs | rebuild-on-import caveats | meson.build change handling not stated |
| 19 | WebFetch | bazel.build/basics/hermeticity | hermeticity, detection tips | - |
| 20 | WebFetch | peps.python.org/pep-0552 | invalidation modes | SOURCE_DATE_EPOCH not in fetched summary |
| 21 | WebFetch | setuptools ext_modules user guide | nothing about rebuild | rebuild/depends semantics not documented there |
| 22 | WebFetch | raw GitHub Cython/Build/Dependencies.py | recompile logic | - |
| 23 | WebFetch | raw GitHub setuptools _distutils build_ext.py | newer_group/depends/force | - |
| 24 | WebFetch | arxiv.org/abs/2404.13295 ; arxiv.org/abs/2601.19146 | abstracts | PDF bodies unreadable here |
| 25 | WebFetch | docs.astral.sh/uv/concepts/cache | cache-keys, mtime heuristics | compiled-extension specifics |
| 26 | WebFetch | scikit-build-core configuration index | editable mentions | editable.rebuild keys not on fetched page |
| 27 | WebFetch | bazel.build/remote/caching | action keying, known issues | hit verification not described |
| 28 | WebFetch | github mozilla/sccache README | caveats | timestamps not mentioned |
| 29 | curl | direct PDF downloads (MSR 403 w/o referer; resolved with referer; Cambridge OA PDF; arXiv; UWaterloo; Mainz; Cambridge CL; Spinellis) | see downloads.json | - |

Not searched: Buck2, Pants, BuildXL docs; pip wheel cache; importlib.invalidate_caches; `python -X` flags; Python bytecode pitfalls beyond PEP 552; 2025-2026 follow-ups beyond the two arXiv items.
