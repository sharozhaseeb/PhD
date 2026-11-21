# W1-LIT outline and source list (2026-11-21, early)

Folder: research-directions/build-test-reduction/01-literature/ (uncommitted; W1 commits nothing).
Early relay for W3: `candidate-rules.md` v0 — rule IDs B1–B5 (build), F1–F5 (functional RTS), P1–P6 (benchmarks), C1–C4 (checkpoints/culprit). IDs are stable; sources are still to-verify.

## Topics and planned primary sources (being verified by researchers T1–T5)
- T1 builds: Build Systems à la Carte (ICFP'18/JFP'20); Rattle / forward build systems; Pluto; Licker & Rice ICSE'19; Sotiropoulos et al. OOPSLA'20 (BuildFS); CloudBuild ICSE-SEIP'16; Gallaba et al. TSE (Kotinos); Bazel/Buck2/Pants remote-cache docs; ccache/sccache docs; setuptools, Cython, meson-python editable, scikit-build-core, PEP 552 pyc.
- T2 RTS: Rothermel & Harrold TSE'96 / TOSEM'97; Harrold OOPSLA'01; Yoo & Harman STVR'12; Ekstazi ISSTA'15; STARTS FSE'16/ASE'17; HyRTS ICSE'18; Shi et al. ISSRE'19, OOPSLA'19; RTSCheck ICSE'19; pytest-testmon; Elbaum et al. FSE'14; Luo et al. FSE'14; Parry et al. TOSEM'21; (Meta predictive selection only as later AI study).
- T3 perf: Huang et al. ICSE'14; Perphecy ICST'17; PerfRanker ISSTA'17; Laaber et al. EMSE'21 (prioritization), FSE'20 (dynamic reconfiguration), EMSE'19 (cloud); Georges OOPSLA'07; Kalibera & Jones ISMM'13; Mytkowicz ASPLOS'09; Stabilizer ASPLOS'13; Barrett OOPSLA'17; Bulej ICPE'20 (duet); Ding et al. ICSE'20; Daly et al. ICPE'20; pyperf, asv, CodSpeed, pytest-benchmark.
- T4 safety eval: Rothermel & Harrold metrics; Just et al. FSE'14; Andrews et al. ICSE'05; Papadakis et al. survey; Petrović & Ivanković ICSE-SEIP'18; performance mutation testing; Jin et al. PLDI'12; Defects4J, BugsInPy, RTPTorrent; Shi et al. ISSTA'18.
- T5 batching/impact: Beheshtian et al. TSE (batch testing); Najafi et al. FSE'19; Ziftci & Reardon ICSE-SEIP'17; Memon et al. ICSE-SEIP'17; Henderson et al. ICST'23; Uber SubmitQueue EuroSys'19; Zeller FSE'99 / TSE'02; Abdalkareem TSE'19; Liang et al. ICSE'18; Law & Rothermel ICSE'03; Orso et al. FSE'03; Chianti OOPSLA'04; PyCG ICSE'21.
