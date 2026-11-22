# Bottleneck build re-timing on an idle machine (amended base f51ed86), 3 repeats each. Scratch copy only.
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
O=$E/results/raw/bottleneck/retime-idle; mkdir -p $O
S=$HOME/bt-lab/exp/work/bn-retime; PY=$HOME/bt-lab/exp/venvs/bn38/bin/python
rm -rf $S; git clone -q --no-hardlinks $HOME/bt-lab/exp/work/bottleneck-replay $S
git -C $S checkout -q --detach f51ed862e619dcff7b7b3691e58d5fc6ead4076b
t() { s=$(date +%s.%N); (cd $S && $PY setup.py build_ext --inplace > /dev/null 2>&1); e=$(date +%s.%N); python3 -c "print(round($e-$s,3))"; }
for r in 1 2 3; do
  git -C $S clean -fdxq; c=$(t)
  n=$(t)
  echo "// retime $r" >> $S/bottleneck/src/reduce_template.c; tpl=$(t); git -C $S checkout -q -- bottleneck/src/reduce_template.c; t > /dev/null
  echo "/* retime $r */" >> $S/bottleneck/src/bottleneck.h; hdr=$(t); git -C $S checkout -q -- bottleneck/src/bottleneck.h; t > /dev/null
  echo "{\"repeat\":$r,\"base\":\"f51ed862\",\"clean_s\":$c,\"null_s\":$n,\"one_template_s\":$tpl,\"bottleneck_h_s\":$hdr,\"loadavg\":\"$(cut -d' ' -f1-3 /proc/loadavg)\"}" | tee $O/repeat$r.json
done
