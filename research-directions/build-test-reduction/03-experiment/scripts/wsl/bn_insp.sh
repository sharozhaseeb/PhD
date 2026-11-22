W=$HOME/bt-lab/exp/work/bottleneck-replay
S=$HOME/bt-lab/exp/repos/bottleneck
cd $W
git log --format='%h %s' | head -8
for c in 22657ac HEAD; do echo $c $(git ls-tree -r --name-only $c | wc -l); done
echo src; git -C $S ls-tree -r --name-only 22657ac | wc -l
git -C $S config --get-regexp 'remote|partial|promisor'
git count-objects -v | head -3; git -C $S count-objects -v | head -3
git -C $W fsck 2>&1 | head -5
