cd ~/bt-lab/exp/repos/bottleneck
H=b0815406af6317f9fd163fb91526d0b8f199e2c6
git ls-tree --name-only $H | tr '\n' ' '; echo
git show $H:setup.py | grep -n -B3 -A25 "def prepare_modules"
git log -1 --format='%h %ad %s' --date=short $H
git log --format='%h %ad %s' --date=short -S'iterators.h' -- setup.py | cat
git grep -n 'iterators.h' $H -- setup.py pyproject.toml meson.build setup.cfg | cat
