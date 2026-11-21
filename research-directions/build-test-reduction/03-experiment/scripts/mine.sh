cd ~/bt-lab/exp/repos
RX='(\bperf\b|speed ?up|faster|optimi[sz]|performance|vectori[sz]|efficien|\bslow)'
for n in *; do
  tot=$(git -C $n log --no-merges --oneline | wc -l)
  hit=$(git -C $n log --no-merges --oneline -i -E --grep="$RX" | wc -l)
  hit5=$(git -C $n log --no-merges --since=2020-01-01 --oneline -i -E --grep="$RX" | wc -l)
  echo "$n total=$tot perfmsg=$hit since2020=$hit5"
done
