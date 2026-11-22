R=$HOME/bt-lab/exp/repos/bottleneck
cd $R
git show c916848^:setup.py
git ls-tree -r --name-only c916848^ | grep -v -E 'tests/|doc/|\.png' | head -80
