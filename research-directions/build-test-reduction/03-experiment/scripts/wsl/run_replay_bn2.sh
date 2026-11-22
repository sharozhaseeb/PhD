set -e
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
export PYTHONPATH=$E/harness
D=$HOME/bt-lab/exp/work
[ -d $D/bottleneck-replay-5edit ] || mv $D/bottleneck-replay $D/bottleneck-replay-5edit
python3 $E/scripts/replay_bn.py $E 2>&1 | tee $E/results/raw/bottleneck/replay-run.txt | tail -28
W=$D/bottleneck-replay
python3 - <<PY
import json,subprocess
E="$E"; W="$W"
st=json.load(open(E+"/edits/bottleneck.states.json")); c={r["sha"]:r for r in json.load(open(E+"/edits/bottleneck.candidates.json"))}
prev=st["base"]; ok=True
for s in st["states"]:
    if s["status"]!="applied": continue
    got=sorted(subprocess.run(["git","-C",W,"diff","--name-only",prev,s["state_sha"]],capture_output=True,text=True).stdout.split())
    exp=c[s["orig_sha"]]["files"]
    print(s["orig_sha"][:8], "OK" if got==sorted(exp) else "MISMATCH", got if got!=sorted(exp) else "")
    prev=s["state_sha"]
PY
