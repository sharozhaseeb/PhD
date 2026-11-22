export PATH=$HOME/.local/bin:$PATH
W=$HOME/bt-lab/exp/work/bottleneck-replay
V=$HOME/bt-lab/exp/venvs/bn38
rm -rf $V
git -C $W status --short | head -3
uv venv --python 3.8 $V 2>&1 | tail -3
source $V/bin/activate
uv pip install "numpy==1.19.5" "pytest<8" "setuptools<60" wheel 2>&1 | tail -8
cd $W
export MAX_JOBS=1
python -c "import numpy,sys;print(sys.version, numpy.__version__)"
python -c "import sysconfig,os;print(os.path.exists(sysconfig.get_paths()['include']+'/Python.h'))"
nice -n 19 python setup.py build_ext --inplace > $HOME/bn38_build.log 2>&1
echo BUILD_RC=$?
tail -30 $HOME/bn38_build.log
