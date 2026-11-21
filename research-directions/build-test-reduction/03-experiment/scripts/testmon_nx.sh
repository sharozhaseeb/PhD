#!/usr/bin/env bash
# A2 "PerfAgent-style per-edit RTS": real pytest-testmon, unchanged, chained over the replay states.
# Own clone (never the oracle workdir). S_0 builds the testmon DB (runs all); each S_t then runs what testmon selects.
# Selection = test ids present in that step's junit. End-to-end wall time includes testmon's own analysis (Ekstazi-style).
set -euo pipefail
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
SRC=$HOME/bt-lab/exp/work/networkx-replay
W=$HOME/bt-lab/exp/work/networkx-testmon
PY=$HOME/bt-lab/exp/venvs/nx/bin/python
O=$E/results/raw/networkx/testmon; mkdir -p $O
[ -d $W ] || git clone -q --no-hardlinks $SRC $W
export PYTHONPATH=$W
cd $W
shas=$(python3 -c "import json,tomllib;b=tomllib.load(open('$E/configs/networkx.toml','rb'))['replay']['base'];s=[x['state_sha'] for x in json.load(open('$E/edits/networkx.states.json'))['states'] if x['status']=='applied'];print(' '.join([b]+s))")
i=0
for sha in $shas; do
  git checkout -q --detach $sha
  lab="S${i}_${sha:0:8}"
  s=$(date +%s.%N)
  set +e; $PY -m pytest networkx --testmon -p no:cacheprovider -q --junitxml=$O/$lab.junit.xml > $O/$lab.log 2>&1; rc=$?; set -e
  e=$(date +%s.%N)
  echo "{\"label\":\"$lab\",\"state_sha\":\"$sha\",\"exit\":$rc,\"wall_s\":$(python3 -c "print(round($e-$s,3))"),\"loadavg_after\":\"$(cut -d' ' -f1 /proc/loadavg)\"}" > $O/$lab.json
  tail -1 $O/$lab.log
  i=$((i+1))
done
