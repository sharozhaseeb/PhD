# Read-only Windows telemetry for night 2026-11-22 (TPM plan (d)). Changes no setting.
# Every 10 s: total CPU %, % Processor Performance (frequency proxy), available MB. Every 60 s: top 5 processes by CPU seconds used in the last minute.
# Usage: powershell -NoProfile -File telemetry_win.ps1 <out.jsonl> <stop file>
param([string]$Out, [string]$Stop)
$enc = New-Object System.Text.UTF8Encoding($false)
$counters = @('\Processor(_Total)\% Processor Time', '\Processor Information(_Total)\% Processor Performance', '\Memory\Available MBytes')
$prev = @{}; $i = 0
while (-not (Test-Path $Stop)) {
  try {
    $s = (Get-Counter -Counter $counters -SampleInterval 10 -MaxSamples 1 -ErrorAction Stop).CounterSamples
    $rec = [ordered]@{
      ts = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz'); epoch = [math]::Round(([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()) / 1000.0, 1)
      cpu = [math]::Round($s[0].CookedValue, 1); perf = [math]::Round($s[1].CookedValue, 1); avail_mb = [math]::Round($s[2].CookedValue)
    }
    if ($i % 6 -eq 0) {
      $now = @{}; $top = @()
      foreach ($p in Get-Process) { if ($p.CPU -ne $null) { $now["$($p.Id)"] = @($p.ProcessName, $p.CPU) } }
      if ($prev.Count -gt 0) {
        $top = $now.GetEnumerator() | ForEach-Object {
          $d = $_.Value[1] - $(if ($prev.ContainsKey($_.Key)) { $prev[$_.Key][1] } else { 0 })
          [pscustomobject]@{ n = $_.Value[0]; s = [math]::Round($d, 1) } } | Sort-Object s -Descending | Select-Object -First 5
      }
      $prev = $now; $rec.top_cpu_s_last_min = @($top)
    }
    [System.IO.File]::AppendAllText($Out, (($rec | ConvertTo-Json -Compress -Depth 4) + "`n"), $enc)
  } catch {
    [System.IO.File]::AppendAllText($Out, ('{"ts":"' + (Get-Date).ToString('s') + '","error":"' + ($_.Exception.Message -replace '"', "'") + '"}' + "`n"), $enc)
    Start-Sleep -Seconds 10
  }
  $i++
}
