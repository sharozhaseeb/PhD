pkill -f bn_all_after1850.sh; sleep 1
ps aux | grep -E 'bn_all|bn_hazard|bn_s0|setup.py' | grep -v grep | cut -c1-140; echo remaining-check-done; date
ls ~/bt-lab/exp/work/bn-hazard 2>&1 | head -2
