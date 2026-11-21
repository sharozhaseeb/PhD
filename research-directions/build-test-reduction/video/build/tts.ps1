# Offline stock Windows voice (System.Speech). One WAV per narration line; skips existing files.
param([string]$Narration, [string]$OutDir, [string]$Voice = 'Microsoft Zira Desktop', [int]$Rate = 0)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
New-Item -ItemType Directory -Force $OutDir | Out-Null
$items = Get-Content -Raw -Encoding UTF8 $Narration | ConvertFrom-Json
$fmt = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(44100, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
foreach ($it in $items) {
  $wav = Join-Path $OutDir ($it.id + '.wav')
  if (Test-Path $wav) { continue }
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $s.SelectVoice($Voice); $s.Rate = $Rate; $s.Volume = 100
  $s.SetOutputToWaveFile($wav, $fmt)
  $s.Speak($it.text)
  $s.Dispose()
  Write-Output ("wrote " + $it.id)
}
