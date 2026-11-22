#!/usr/bin/env bash
# Prep for night item (c): a dedicated bottleneck clone at the amended base f51ed86, clean build (bn38), asv discovery.
# No timing. Writes results/raw/bottleneck/bench/prep.json.
set -euo pipefail
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
O=$E/results/raw/bottleneck/bench; mkdir -p $O
S=$HOME/bt-lab/exp/work/bn-bench; PY=$HOME/bt-lab/exp/venvs/bn38/bin/python
SHA=f51ed862e619dcff7b7b3691e58d5fc6ead4076b
[ -d $S ] || git clone -q --no-hardlinks $HOME/bt-lab/exp/work/bottleneck-replay $S
git -C $S checkout -q -f --detach $SHA; git -C $S clean -fdxq
(cd $S && $PY setup.py build_ext --inplace > $O/prep-build.log 2>&1)
PYTHONPATH=$E/harness $PY -m bth.benchrun discover --state $S --bench-dir asv_bench/benchmarks --out $O/discover.json --python $PY
$PY - <<EOF
import json
d = json.load(open("$O/discover.json")); c = d["cases"] if isinstance(d, dict) else d
kinds = {}
for x in c: kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
mods = {}
for x in c:
    if x["kind"] == "time": mods[x["id"].split(".")[0]] = mods.get(x["id"].split(".")[0], 0) + 1
json.dump({"state_sha": "$SHA", "clone": "$S", "kinds": kinds, "time_cases_per_module": mods,
           "head": "$(git -C $S rev-parse HEAD)"}, open("$O/prep.json", "w"), indent=1)
print(kinds, mods)
EOF
