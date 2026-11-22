set -e
R=$HOME/bt-lab/exp/repos/bottleneck
cd $R
git branch --show-current
git symbolic-ref refs/remotes/origin/HEAD || true
git rev-parse origin/HEAD origin/master 2>&1 || true
git rev-list --count origin/HEAD 2>&1
git log origin/HEAD --since=2019-09-01 --until=2021-01-01 --no-merges --format='%h %ad %s' --date=short | grep -i -E '\bperf\b|speed ?up|faster|optimi[sz]|performance|vectori|efficien' || true
