cd ~/bt-lab/exp/repos
for r in jcrist/msgspec shapely/shapely; do n=$(basename $r); [ -d $n ] || git clone -q --filter=blob:none https://github.com/$r.git $n; done
RX='(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien|\bslow)'
for n in bottleneck networkx sqlglot more-itertools msgspec shapely pywt; do
  echo "=== $n $(git -C $n log --no-merges --since=2018-01-01 --oneline -i -E --grep="$RX" | wc -l)"
  git -C $n log --no-merges --since=2018-01-01 --format='%h %ad %s' --date=short -i -E --grep="$RX" | head -25
done
ls -d */benchmarks */asv_bench */bench* 2>/dev/null
