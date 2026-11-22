W=$HOME/bt-lab/exp/work/bottleneck-replay
cd $W
git branch -a | cat
for c in bth-replay bth-replay~1 bth-replay~4 bth-replay~5; do echo $c $(git rev-parse --short $c) $(git ls-tree -r --name-only $c | wc -l) $(git log -1 --format=%s $c); done
git config remote.origin.promisor true
git config remote.origin.partialclonefilter blob:none
git config extensions.partialclone origin
git remote -v
