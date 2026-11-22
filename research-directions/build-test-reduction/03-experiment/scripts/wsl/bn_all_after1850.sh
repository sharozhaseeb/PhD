E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
L=$E/results/raw/bottleneck/hazard; mkdir -p $L
while [ "$(date +%H%M)" -lt 1850 ]; do sleep 20; done
echo "start $(date)  load $(cat /proc/loadavg)" > $L/driver.log
bash /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_s0.sh > $L/s0_driver.log 2>&1
echo "s0 done $(date)" >> $L/driver.log
bash /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_hazard.sh c5720c8d '\.time_(nan)?median\((?!.*10000000)' > $L/c5720c8d.log 2>&1
echo "c5720c8d done $(date)" >> $L/driver.log
bash /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_hazard.sh a638b282 'reduce\.Time[12]DReductions\.time_nan(sum|min)\((?!.*10000000)' > $L/a638b282.log 2>&1
echo "a638b282 done $(date)" >> $L/driver.log
bash /mnt/c/Users/pc/study/bt-lab/exp/scripts/bn_hazard.sh 98b59df2 'reduce\.\w+\.time_nan(min|max)\((?!.*10000000)' > $L/98b59df2.log 2>&1
echo "98b59df2 done $(date)" >> $L/driver.log
