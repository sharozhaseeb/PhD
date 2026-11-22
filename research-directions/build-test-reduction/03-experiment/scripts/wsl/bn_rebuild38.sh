export PATH=$HOME/.local/bin:$PATH
source $HOME/bt-lab/exp/venvs/bn38/bin/activate
export MAX_JOBS=1
W=$HOME/bt-lab/exp/work/bottleneck-replay
R=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/results/raw/bottleneck
cd $W
git clean -fdxq
git status --short --ignored | head
( time nice -n 19 python setup.py build_ext --inplace ) > $R/setup-build.log 2>&1; echo BUILD_RC=$?
wc -l $R/setup-build.log; grep -c "^gcc\|^x86_64" $R/setup-build.log; grep -E "building|^gcc|^x86_64|real|error" $R/setup-build.log | cut -c1-220 | head -30
ls bottleneck/*.so
nice -n 19 python -m pytest bottleneck/tests -p no:cacheprovider -q > $R/setup-test.log 2>&1; echo TEST_RC=$?
tail -4 $R/setup-test.log
python -c "import bottleneck,numpy,sys;print(bottleneck.__version__, numpy.__version__, sys.version)"
uv pip freeze > $R/env-freeze.txt; cat $R/env-freeze.txt
