export PATH=$HOME/.local/bin:$PATH
source $HOME/bt-lab/exp/venvs/bn38/bin/activate
W=$HOME/bt-lab/exp/work/bottleneck-replay
cd $W
git rev-parse HEAD; git status --short | head
wc -l ~/bn38_build.log; cat ~/bn38_build.log | cut -c1-200 | head -40
ls bottleneck/*.so
mkdir -p /mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/results/raw/bottleneck
nice -n 19 python -m pytest bottleneck/tests -p no:cacheprovider -q > ~/bn38_test.log 2>&1; echo TEST_RC=$?
tail -15 ~/bn38_test.log
