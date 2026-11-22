export PATH=$HOME/.local/bin:$PATH
source $HOME/bt-lab/exp/venvs/bn38/bin/activate
export MAX_JOBS=1
W=$HOME/bt-lab/exp/work/bottleneck-replay
S=$HOME/bt-lab/exp/work/bn-scratch
R=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/results/raw/bottleneck
rm -rf $S; cp -a $W $S; cd $S
snap() { ls -l --time-style=full-iso bottleneck/*.so bottleneck/src/*.c bottleneck/src/move_median/*.c bottleneck/src/bn_config.h | awk '{print $7,$9}' | sed 's#bottleneck/##; s#\.cpython-38-x86_64-linux-gnu##'; }
step() { # name, command-to-edit
  echo "=== $1"; snap > /tmp/before.txt; sleep 2; eval "$2"
  ( time nice -n 19 python setup.py -v build_ext --inplace ) > $R/incr_$1.log 2>&1
  snap > /tmp/after.txt
  echo "changed files (mtime differs):"; diff /tmp/before.txt /tmp/after.txt | grep '^>' | awk '{print $3}'
  grep -E 'real' $R/incr_$1.log
  cp /tmp/before.txt $R/incr_$1.before.txt; cp /tmp/after.txt $R/incr_$1.after.txt
}
step B_reduce_template "sed -i '0,/^#include \"bottleneck.h\"/s//#include \"bottleneck.h\"  \/* scratch *\//' bottleneck/src/reduce_template.c"
step C_bottleneck_h "echo '/* scratch */' >> bottleneck/src/bottleneck.h"
step D_iterators_h "echo '/* scratch */' >> bottleneck/src/iterators.h"
step E_move_median_c "echo '/* scratch */' >> bottleneck/src/move_median/move_median.c"
step F_move_template "echo '/* scratch */' >> bottleneck/src/move_template.c"
step G_noop "true"
