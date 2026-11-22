#!/usr/bin/env bash
# A/A re-run (amendment 2): 23-case frozen subset, cap 55 min, per-run checkpoint aa/runs.partial.jsonl.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && AA_SAMPLE=frozen/networkx.aa_noise_sample_cut23.json PYTHONPATH=$E/harness timeout 3300 ~/bt-lab/exp/venvs/nx/bin/python scripts/aa_noise_nx.py
rc=$?; echo "$(date -Iseconds) driver exit $rc (124 = 55 min cap hit)" >> $E/results/raw/networkx/bench/aa/driver.log
