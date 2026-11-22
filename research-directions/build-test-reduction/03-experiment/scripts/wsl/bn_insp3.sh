W=$HOME/bt-lab/exp/work/bottleneck-replay
cd $W
for c in 22657ac bth-replay; do echo $c $(git ls-tree -r --name-only $c | wc -l); done
git status --short | head -3
git checkout -q -f --detach 22657ac; git status --short | head -3; git ls-files | wc -l
# why conflict
git checkout -q -f bth-replay
git diff --binary --no-renames c5720c8^ c5720c8 -- bottleneck ':(exclude)bottleneck/tests' ':(exclude)bottleneck/benchmark' | git apply --3way --index --whitespace=nowarn - 2>&1 | head -8
git reset -q --hard; git clean -fdq
git checkout -q -f --detach 22657ac
rm -rf ~/bt-lab/exp/work/bn-probe-alt
python3 /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_probe_alt.py /mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment 2>&1 | tail -20
