import os, sys, json
from pathlib import Path
sys.path.insert(0, sys.argv[1] + "/harness")
from bth.mine import mine
from bth.replay import build_states
repo = Path(os.path.expanduser("~/bt-lab/exp/repos/bottleneck"))
recs = mine(repo, regex=r'(\bperf\b|speed ?up|faster|optimi[sz](e|ation|ing|ed)\b|performance|vectori[sz]|efficien)',
  src_globs=["bottleneck/**/*.py","bottleneck/src/*.c","bottleneck/src/*.h","bottleneck/src/**/*.c","bottleneck/src/**/*.h"],
  exclude_globs=["bottleneck/tests/**","bottleneck/benchmark/**","asv_bench/**","doc/**"], max_lines=200,
  before="2021-01-01", after="2019-12-01", rev="b0815406af6317f9fd163fb91526d0b8f199e2c6")
q=[r for r in recs if r["qualifies"]]
import subprocess
base=subprocess.run(["git","-C",str(repo),"rev-parse",q[0]["sha"]+"^"],capture_output=True,text=True).stdout.strip()
work=Path(os.path.expanduser("~/bt-lab/exp/work/bn-probe-alt"))
st=build_states(repo,work,base,[{"sha":r["sha"],"date":r["date"]} for r in q],["bottleneck",":(exclude)bottleneck/tests",":(exclude)bottleneck/benchmark"],None)
print("base",base,len(q))
for s in st: print(s["orig_sha"][:8],s["status"],s["reason"])
