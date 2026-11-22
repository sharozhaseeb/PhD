# usage: bn_hazard.sh <c8> <bench-filter-regex>
set -u
c8=$1; FILT=$2
export PATH=$HOME/.local/bin:$PATH
source $HOME/bt-lab/exp/venvs/bn38/bin/activate
export MAX_JOBS=1
E=/mnt/c/Users/pc/study/PhD/research-directions/build-test-reduction/03-experiment
R=$E/results/raw/bottleneck/hazard/$c8; mkdir -p $R
W=$HOME/bt-lab/exp/work/bottleneck-replay
H=$HOME/bt-lab/exp/work/bn-hazard/$c8; rm -rf $H; mkdir -p $H
NXPY=$HOME/bt-lab/exp/venvs/nx/bin/python
PY38=$HOME/bt-lab/exp/venvs/bn38/bin/python
read P C < <($NXPY - <<PY
import json
st=json.load(open("$E/edits/bottleneck.states.json"))
prev=st["base"]
for s in st["states"]:
    if s["status"]!="applied": continue
    if s["orig_sha"].startswith("$c8"):
        print(prev,s["state_sha"]); break
    prev=s["state_sha"]
PY
)
echo "parent_state=$P commit_state=$C" | tee $R/states.txt
hashso() { (cd $1; for f in bottleneck/*.so; do echo "$(sha256sum $f | cut -c1-16) $(strip --strip-debug -o /tmp/_s.so $f && sha256sum /tmp/_s.so | cut -c1-16) $f"; done | sed 's#bottleneck/##; s#\.cpython-38-x86_64-linux-gnu##'); }
mt() { (cd $1; ls -l --time-style=full-iso bottleneck/*.so | awk '{print $7,$9}' | sed 's#bottleneck/##; s#\.cpython-38-x86_64-linux-gnu##'); }
bld() { (cd $1; ( time nice -n 19 python setup.py build_ext --inplace ) > $2 2>&1; echo "build rc=$? $(grep real $2)"); }
echo "== (a) build parent state cleanly"
cp -a $W $H/inc; cd $H/inc; git checkout -q -f --detach $P; git clean -fdxq; bld $H/inc $R/a_build_parent.log
echo "cols: sha256(raw) sha256(strip --strip-debug) file" > $R/a_parent_so.txt; hashso $H/inc >> $R/a_parent_so.txt; cat $R/a_parent_so.txt
cp -a $H/inc $H/stale
echo "== (b) apply commit diff (= checkout of commit state)"
cd $H/inc; sleep 2; git diff --stat $P $C > $R/b_diff_stat.txt; git diff $P $C --stat | cat
git checkout -q --detach $C
mt $H/inc > $R/c_so_mtime_before.txt
echo "== (c) INCREMENTAL build"
bld $H/inc $R/c_build_incremental.log
mt $H/inc > $R/c_so_mtime_after.txt
echo "so files rebuilt (mtime changed) in incremental:"; diff $R/c_so_mtime_before.txt $R/c_so_mtime_after.txt | grep '^>' | awk '{print $3}' | tee $R/c_rebuilt.txt
echo "cols: raw strip file" > $R/c_incremental_so.txt; hashso $H/inc >> $R/c_incremental_so.txt
echo "== (d) CLEAN build in separate copy"
cp -a $H/inc $H/clean; cd $H/clean; git clean -fdxq; bld $H/clean $R/d_build_clean.log
echo "cols: raw strip file" > $R/d_clean_so.txt; hashso $H/clean >> $R/d_clean_so.txt
echo "== (e) compare incremental vs clean"
{ echo "incremental vs clean (raw / stripped):"; paste <(tail -n +2 $R/c_incremental_so.txt) <(tail -n +2 $R/d_clean_so.txt) | awk '{printf "%-16s raw:%s stripped:%s\n",$3,($1==$4?"EQUAL":"DIFF"),($2==$5?"EQUAL":"DIFF")}'; echo "parent vs clean (raw / stripped):"; paste <(tail -n +2 $R/a_parent_so.txt) <(tail -n +2 $R/d_clean_so.txt) | awk '{printf "%-16s raw:%s stripped:%s\n",$3,($1==$4?"EQUAL":"DIFF"),($2==$5?"EQUAL":"DIFF")}'; } | tee $R/e_compare.txt
echo "== probe: pre-fix setup.py (iterators.h absent from depends=), incremental from parent build"
cd $H/stale; git checkout -q --detach $C; sed -i '/"bottleneck\/src\/iterators.h",/d' setup.py; grep -c iterators.h setup.py > $R/stale_setup_grep.txt
mt $H/stale > $R/stale_so_mtime_before.txt; sleep 2
bld $H/stale $R/stale_build.log; mt $H/stale > $R/stale_so_mtime_after.txt
echo "so rebuilt in stale probe:"; diff $R/stale_so_mtime_before.txt $R/stale_so_mtime_after.txt | grep '^>' | awk '{print $3}' | tee $R/stale_rebuilt.txt
echo "cols: raw strip file" > $R/stale_so.txt; hashso $H/stale >> $R/stale_so.txt
paste <(tail -n +2 $R/stale_so.txt) <(tail -n +2 $R/d_clean_so.txt) | awk '{printf "%-16s stale-vs-clean raw:%s stripped:%s\n",$3,($1==$4?"EQUAL":"DIFF"),($2==$5?"EQUAL":"DIFF")}' | tee $R/stale_compare.txt
echo "== (f) tests"
for v in inc clean stale; do (cd $H/$v; nice -n 19 python -m pytest bottleneck/tests -p no:cacheprovider -q --junitxml=$R/f_junit_$v.xml > $R/f_test_$v.log 2>&1; echo "$v rc=$? $(tail -1 $R/f_test_$v.log)"); done
export PYTHONPATH=$E/harness
$NXPY - <<PY | tee $R/f_test_diff.txt
from bth.junit import parse
import json
r={v:parse("$R/f_junit_%s.xml"%v, rootdir="$H/inc") if False else parse("$R/f_junit_%s.xml"%v) for v in ("inc","clean","stale")}
for a,b in (("inc","clean"),("stale","clean")):
    ks=set(r[a])|set(r[b]); d=[k for k in ks if r[a].get(k,{}).get("outcome")!=r[b].get(k,{}).get("outcome")]
    print(f"{a} vs {b}: {len(r[a])} / {len(r[b])} tests, outcome differences: {len(d)}", d[:10])
for v in r:
    from collections import Counter
    print(v, dict(Counter(x["outcome"] for x in r[v].values())))
PY
echo "== (g) benchmarks (interleaved, 3 repeats): filter=$FILT"
cat /proc/loadavg | tee $R/g_loadavg_before.txt
$NXPY -m bth.benchrun interleave --state INC=$H/inc --state CLEAN=$H/clean --state STALE=$H/stale --python $PY38 --bench-dir asv_bench/benchmarks --filter "$FILT" --repeats 3 --cpus 2-5 --out $R/g_bench.json 2>&1 | tail -3
cat /proc/loadavg | tee $R/g_loadavg_after.txt
$NXPY - <<PY | tee $R/g_verdicts.txt
import json
from collections import defaultdict
from bth.stats import asv_rule
d=json.load(open("$R/g_bench.json")); S=defaultdict(lambda: defaultdict(list)); err=0
for x in d:
    if x.get("error") or x.get("skipped"): err+=1; continue
    S[x["id"]][x["label"]]+=x["samples"]
print("cases:",len(S),"errors/skipped entries:",err)
from collections import Counter
c1=Counter(); c2=Counter(); rows=[]
for i,v in sorted(S.items()):
    a=asv_rule(v["CLEAN"],v["INC"]); b=asv_rule(v["CLEAN"],v["STALE"])
    c1[a.status]+=1; c2[b.status]+=1
    rows.append((i,a,b))
print("INC vs CLEAN (ref=CLEAN):",dict(c1)); print("STALE vs CLEAN:",dict(c2))
for i,a,b in rows:
    if a.status!="same" or b.status!="same": print(i,"INC/CLEAN %.3f p=%.4g %s | STALE/CLEAN %.3f p=%.4g %s"%(a.ratio,a.p,a.status,b.ratio,b.p,b.status))
print("max |log ratio| INC/CLEAN: ratio range %.3f..%.3f"%(min(a.ratio for _,a,_ in rows),max(a.ratio for _,a,_ in rows)))
PY
