cd ~/bt-lab/exp/repos/bottleneck
for c in c5720c8d a638b282 98b59df2; do echo "##### $c"; git show $c --format='%h %s' -- bottleneck/src | grep -E '^(\+\+\+|@@|\+#|-#|[+-]\s*(static|REDUCE|BN_|#))' | head -60; done
