# FULL oracle for networkx replay states on Windows (LABEL: "Windows, provisional"; PM-approved 2026-11-21).
# Usage: oracle_nx_win.ps1 -What tests|depmap|bench|profile|build|all -Idx 0,1,2
param([string]$What = "all", [int[]]$Idx = @(0))
$ErrorActionPreference = "Stop"
$E  = "C:\Users\pc\study\PhD\research-directions\build-test-reduction\03-experiment"
$W  = "C:\Users\pc\study\bt-lab\exp\win\networkx-replay"
$PY = "C:\Users\pc\study\bt-lab\exp\win\venv-nx\Scripts\python.exe"
$env:PYTHONPATH = "$W;$E\harness"   # state dir first: the user-site networkx must never shadow the replayed source
$cfg = "$E\configs\networkx-winprov.toml"
$states = (Get-Content "$E\edits\networkx.states.json" -Raw | ConvertFrom-Json).states | Where-Object { $_.status -eq "applied" }
$base = "181f295117f7f7488644c87f04699290f8e49188"
foreach ($i in $Idx) {
  if ($i -eq 0) { $sha = $base } else { $sha = $states[$i - 1].state_sha }
  $lab = "S{0}_{1}" -f $i, $sha.Substring(0, 8)
  git -C $W -c core.autocrlf=false checkout -q --detach $sha
  Get-ChildItem "$W\networkx" -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
  $cpu = (Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 3).CounterSamples | Measure-Object CookedValue -Average
  $nxfile = & $PY -c "import networkx; print(networkx.__file__)" 2>$null
  Write-Output ("{0} cpu_before={1:N1}% networkx={2}" -f $lab, $cpu.Average, $nxfile)
  if (-not $nxfile.StartsWith($W)) { throw "networkx resolves outside the state dir: $nxfile" }
  if ($What -in @("build", "all")) {
    New-Item -ItemType Directory -Force "$E\results\raw\networkx-winprov\build" | Out-Null
    $t = Measure-Command { & $PY -m pip install -q -e $W --no-deps --no-build-isolation --no-index 2>&1 | Out-Null }
    @{ label = $lab; state_sha = $sha; cmd = "pip install -e --no-deps --no-build-isolation"; wall_s = [math]::Round($t.TotalSeconds, 3); platform = "Windows, provisional"; cpu_before = $cpu.Average } | ConvertTo-Json | Set-Content "$E\results\raw\networkx-winprov\build\$lab.json" -Encoding utf8
  }
  foreach ($sub in @("tests", "depmap", "bench", "profile")) {
    if ($What -in @($sub, "all")) {
      $name = @{ tests = "oracle-tests"; depmap = "depmap"; bench = "bench"; profile = "profile" }[$sub]
      $extra = @(); if ($sub -eq "tests") { $extra = @("--junit") }
      & $PY -m bth.orchestrate --exp-root $E $name --config $cfg --state-dir $W --label $lab --python $PY @extra
    }
  }
}
