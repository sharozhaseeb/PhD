#!/usr/bin/env bash
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && PYTHONPATH=$E/harness ~/bt-lab/exp/venvs/nx/bin/python scripts/c5_compare.py
