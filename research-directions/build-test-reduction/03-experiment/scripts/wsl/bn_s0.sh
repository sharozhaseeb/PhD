export PATH=$HOME/.local/bin:$PATH
source $HOME/bt-lab/exp/venvs/bn38/bin/activate
export MAX_JOBS=1
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
R=$E/results/raw/bottleneck
W=$HOME/bt-lab/exp/work/bottleneck-replay
cd $W
git checkout -q -f --detach f51ed862e619dcff7b7b3691e58d5fc6ead4076b; git clean -fdxq
git rev-parse HEAD; git ls-files | wc -l
( time nice -n 19 python setup.py build_ext --inplace ) > $R/s0-build.log 2>&1; echo BUILD_RC=$?
tail -5 $R/s0-build.log; ls bottleneck/*.so
nice -n 19 python -m pytest bottleneck/tests -p no:cacheprovider -q --junitxml=$R/s0-junit.xml > $R/s0-test.log 2>&1; echo TEST_RC=$?
tail -4 $R/s0-test.log
python -c "import bottleneck,numpy;print(bottleneck.__version__, numpy.__version__)"
{ echo; echo "## S_0 for the re-replay: base f51ed862e619dcff7b7b3691e58d5fc6ead4076b (bn38: py3.8.20 numpy 1.19.5), clean build, serial pytest"; cat $R/s0-build.log; tail -4 $R/s0-test.log; } >> $R/setup-log.txt
git status --short | head -3
