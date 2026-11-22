O=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment/scripts/oracle_nx.sh
for i in $(seq 1 18); do bash $O build $i 2>&1 | grep -E "loadavg|GATE|rror" ; bash $O tests $i 2>&1 | grep -E "oracle-tests|GATE|rror"; done
