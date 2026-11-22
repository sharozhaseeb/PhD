export PATH=$HOME/.local/bin:$PATH
W=$HOME/bt-lab/exp/work/bottleneck-replay
V=$HOME/bt-lab/exp/venvs/bn312
rm -rf ~/bt-lab/exp/work/bn-probe-alt $V
git -C $W checkout -q -f --detach 22657acaad5f27d9f692dd64362439ada8032c1b
uv venv --python 3.12 $V 2>&1 | tail -2
source $V/bin/activate
uv pip install "numpy<2" pytest setuptools wheel 2>&1 | tail -3
cd $W
export MAX_JOBS=1
python -c "import numpy,sys;print(sys.version, numpy.__version__)"
nice -n 19 python setup.py build_ext --inplace > $HOME/bn312_build.log 2>&1
echo BUILD_RC=$?
tail -30 $HOME/bn312_build.log
