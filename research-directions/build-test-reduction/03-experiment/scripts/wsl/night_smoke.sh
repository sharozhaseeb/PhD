#!/usr/bin/env bash
# Smoke test of scripts/night_nx.py (prep, not a measurement): case lists per block, and one 1-case interleave
# through the per-run gate (checkpoint in /tmp). Output is discarded except the printed summary.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && PYTHONPATH=$E/harness:$E/scripts $HOME/bt-lab/exp/venvs/nx/bin/python - <<'EOF'
import json, night_nx as N, spotcheck_powered_nx as SP
from pathlib import Path
SP.LOG = Path("/tmp/night_smoke.log")
for i in (1, 2, 3, 4, 8):
    print(i, "flagged", len(N.flagged(i)), "reached", len(N.reached(i)), "tier1", len(set(N.flagged(i) + N.reached(i))))
print("telemetry", N.win_telemetry())
SP.clone(SP.A, N.S0)
ck = Path("/tmp/night_smoke.ck.jsonl"); ck.unlink(missing_ok=True)
runs = N.interleave([("A", SP.A)], [N.CANARY[0]], 1, 1, ck)
print("smoke run:", runs[0]["id"], len(runs[0]["samples"]), "samples, pre_gate", runs[0].get("pre_gate"))
EOF
