set -e
mkdir -p ~/bt-lab/exp/repos && cd ~/bt-lab/exp/repos
for r in networkx/networkx tobymao/sqlglot PyWavelets/pywt pydata/bottleneck msgpack/msgpack-python pytoolz/cytoolz more-itertools/more-itertools; do
  n=$(basename $r); [ -d $n ] || git clone -q --filter=blob:none https://github.com/$r.git $n
done
ls
