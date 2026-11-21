cd ~/bt-lab/exp/repos/networkx
RX='(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien)'
git log --no-merges --first-parent --before=2026-11-21 --format='%H' -i -E --grep="$RX" | head -60 > /tmp/nx_cands
n=0
while read h; do
  src=$(git diff --numstat $h^ $h -- 'networkx/*.py' ':(exclude)networkx/**/tests/**' ':(exclude)networkx/conftest.py' | awk '{s+=$1+$2; f++} END{print f+0, s+0}')
  f=${src% *}; l=${src#* }
  ok=$([ "$f" -ge 1 ] && [ "$l" -le 200 ] && echo Y || echo N)
  echo "$ok $(git log -1 --format='%h %ad' --date=short $h) files=$f lines=$l $(git log -1 --format=%s $h | cut -c1-70)"
done < /tmp/nx_cands
