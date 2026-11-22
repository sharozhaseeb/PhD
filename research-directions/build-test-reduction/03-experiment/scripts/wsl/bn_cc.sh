source $HOME/bt-lab/exp/venvs/bn38/bin/activate
python -c "import sysconfig;print(sysconfig.get_config_var('CC'), sysconfig.get_config_var('CFLAGS'))"
which clang gcc cc
cd ~/bt-lab/exp/work/bottleneck-replay; grep -n "verbose\|log\." setup.py bottleneck/src/bn_template.py | head; cat setup.cfg | head -20
