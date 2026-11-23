#!/usr/bin/env bash
# Smoke test (not a measurement) of `bth.benchrun measure-cached` on real networkx: two small modules at S0, in the
# separate clone nx-share, nice 19 on CPUs 0-1. Output in /tmp only; prints a summary.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
C=$HOME/bt-lab/exp/work/nx-share; PY=$HOME/bt-lab/exp/venvs/nx/bin/python
git -C $C checkout -q -f --detach 181f295117f7f7488644c87f04699290f8e49188 && git -C $C clean -fdxq
rm -f /tmp/e5s.ck.jsonl
cd $E && PYTHONPATH=$E/harness OMP_NUM_THREADS=1 nice -n 19 $PY -m bth.benchrun measure-cached --state smoke=$C --python $PY \
  --bench-dir benchmarks/benchmarks --filter '^(benchmark_many_components|benchmark_to_networkx_graph)\.' --values 6 \
  --cpus 0-1 --out /tmp/e5s.json --checkpoint /tmp/e5s.ck.jsonl
$PY - <<'EOF'
import json
r = json.load(open("/tmp/e5s.json"))
print(len(r), "cases;", {x["module"] for x in r}, "errors", sum(1 for x in r if x.get("error")))
for x in r[:3]:
    print(x["id"][-50:], len(x["samples"]), x["number"], round(x["module_import_s"], 3), round(x.get("setup_s", 0), 3), round(x.get("loop_s", 0), 3))
print(open("/tmp/e5s.ck.jsonl").read().count("\n"), "checkpoint lines (modules)")
EOF
