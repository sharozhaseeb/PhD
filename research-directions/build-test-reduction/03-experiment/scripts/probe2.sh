cd ~/bt-lab/exp/repos/bottleneck
git show 933b653:setup.py | grep -nE "Extension|depends|template|build_ext|def " | head -30
git log --no-merges --format='%h %ad %s' --date=short 2b9c661^..933b653 | wc -l
git log --no-merges --format='%h %s' -i -E --grep='PERF' 2b9c661^..933b653 | wc -l
cd ../networkx; git ls-tree -r --name-only HEAD networkx | grep -c "tests/test_.*py"; git ls-tree -r --name-only HEAD benchmarks/benchmarks | wc -l
git log --no-merges --since=2024-01-01 --format='%h' -i -E --grep='(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|efficien)' | wc -l
cd ../sqlglot; git log --no-merges --since=2025-01-01 --format='%h' -E --grep='^perf' | wc -l; git ls-tree -r --name-only HEAD tests | grep -c "test_.*py"
