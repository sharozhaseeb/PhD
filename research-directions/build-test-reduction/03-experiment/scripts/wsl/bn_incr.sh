# usage: bn_incr.sh <venv>
export PATH=$HOME/.local/bin:$PATH
V=$1
source $V/bin/activate
export MAX_JOBS=1
W=$HOME/bt-lab/exp/work/bottleneck-replay
S=$HOME/bt-lab/exp/work/bn-scratch
L=$HOME/bn_incr
mkdir -p $L
cd $W
echo "=== A: null rebuild in replay workdir (nothing touched)"
ls -l --time-style=full-iso bottleneck/*.so bottleneck/src/*.c 2>&1 | awk '{print $6,$7,$9}' > $L/A_before.txt
nice -n 19 python setup.py -v build_ext --inplace > $L/A_null.log 2>&1; echo rc=$?
ls -l --time-style=full-iso bottleneck/*.so bottleneck/src/*.c 2>&1 | awk '{print $6,$7,$9}' > $L/A_after.txt
cat $L/A_null.log | grep -v '^$' | head -40
diff $L/A_before.txt $L/A_after.txt && echo "NO FILE MTIME CHANGED (.so and generated .c)"
echo "=== B: scratch copy, one-line edit in reduce_template.c"
rm -rf $S; cp -a $W $S; cd $S
grep -n "BN_OPT_3" bottleneck/src/reduce_template.c | head -3
ls -l --time-style=full-iso bottleneck/*.so bottleneck/src/*.c | awk '{print $6,$7,$9}' > $L/B_before.txt
sleep 2
# one-line edit: append a comment to the first line after the license header (touches the template only)
sed -i '0,/^#include "bottleneck.h"/s//#include "bottleneck.h"  \/* scratch edit *\//' bottleneck/src/reduce_template.c
git diff --stat | cat
nice -n 19 python setup.py -v build_ext --inplace > $L/B_edit.log 2>&1; echo rc=$?
grep -v '^$' $L/B_edit.log | head -60
ls -l --time-style=full-iso bottleneck/*.so bottleneck/src/*.c | awk '{print $6,$7,$9}' > $L/B_after.txt
diff $L/B_before.txt $L/B_after.txt
echo "=== C: header-only edit (bottleneck.h) in scratch"
sleep 2
echo "/* scratch */" >> bottleneck/src/bottleneck.h
nice -n 19 python setup.py -v build_ext --inplace > $L/C_header.log 2>&1; echo rc=$?
grep -v '^$' $L/C_header.log | head -60
echo "=== D: iterators.h edit (NOT in setup.py depends=) in scratch"
sleep 2
echo "/* scratch */" >> bottleneck/src/iterators.h
nice -n 19 python setup.py -v build_ext --inplace > $L/D_iterators.log 2>&1; echo rc=$?
grep -v '^$' $L/D_iterators.log | head -30
echo "=== E: move_median.c edit in scratch"
sleep 2
echo "/* scratch */" >> bottleneck/src/move_median/move_median.c
nice -n 19 python setup.py -v build_ext --inplace > $L/E_movemedian.log 2>&1; echo rc=$?
grep -v '^$' $L/E_movemedian.log | head -30
mkdir -p /mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/results/raw/bottleneck
cp $L/*.log $L/*.txt /mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/results/raw/bottleneck/ 2>/dev/null
