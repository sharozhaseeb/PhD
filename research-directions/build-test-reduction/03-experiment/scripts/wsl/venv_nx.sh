set -e
export PATH=$HOME/.local/bin:$PATH
mkdir -p ~/bt-lab/exp/venvs
cd ~/bt-lab/exp/venvs
[ -d nx ] || uv venv -q -p 3.12 nx
time uv pip install -q -p nx/bin/python numpy scipy pandas matplotlib lxml sympy pytest pytest-xdist pytest-testmon
uv pip install -q -p nx/bin/python -e ~/bt-lab/exp/work/networkx-replay --no-deps
nx/bin/python -c "import networkx, sys; print(networkx.__file__, sys.version)"
uv pip freeze -p nx/bin/python > ~/bt-lab/exp/venvs/nx-freeze.txt; wc -l ~/bt-lab/exp/venvs/nx-freeze.txt
