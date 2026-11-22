E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
cd $E && (PYTHONPATH=$E/harness taskset -c 6-11 ~/bt-lab/exp/venvs/nx/bin/python scripts/killsets_nx.py --latent > /tmp/latent.log 2>&1; echo "=== latent done" >> /tmp/latent.log) &
bash /mnt/c/Users/pc/study/bt-lab/exp/scripts/profile_s0.sh
wait; cat /tmp/latent.log | tail -8
