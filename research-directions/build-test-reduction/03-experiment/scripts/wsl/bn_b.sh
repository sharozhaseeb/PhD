cd ~/bt-lab/exp/work/bottleneck-replay
git show f51ed86:asv_bench/benchmarks/reduce.py | head -80; git ls-tree -r --name-only f51ed86 asv_bench
git ls-tree -r --name-only f51ed86 | grep -E "tests/|bottleneck/benchmark" | head
