# Usage: .\build.ps1 [all|check|manifest]   (default: all)
param([string]$Target = "all")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$py = if ($env:PY) { $env:PY } else { "python" }
switch ($Target) {
  "all"      { & $py scripts/make_all.py; if ($LASTEXITCODE) { exit $LASTEXITCODE }; & $py scripts/check.py; exit $LASTEXITCODE }
  "check"    { & $py scripts/check.py; exit $LASTEXITCODE }
  "manifest" { & $py scripts/make_all.py --manifest; exit $LASTEXITCODE }
  default    { Write-Error "unknown target $Target (all|check|manifest)" }
}
