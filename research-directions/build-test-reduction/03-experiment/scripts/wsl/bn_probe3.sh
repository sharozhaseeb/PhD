R=$HOME/bt-lab/exp/repos/bottleneck
cd $R
git log --first-parent --no-merges --format='%h %ad %s' --date=short 2b9c661e..c5720c8d -- bottleneck/src bottleneck/*.py | cat
echo ---; git log --first-parent --format='%h %p %s' 2b9c661e..c5720c8d | cat
