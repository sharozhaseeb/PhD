W=$HOME/bt-lab/exp/work/bottleneck-replay
git -C $W config --get-regexp 'remote.origin|extensions|core.partial'
git -C $W remote set-url origin https://github.com/pydata/bottleneck.git
time git -C $W checkout -f -q --detach 22657acaad5f27d9f692dd64362439ada8032c1b 2>&1 | tail -5
git -C $W status --short | head; git -C $W rev-parse HEAD; ls $W
