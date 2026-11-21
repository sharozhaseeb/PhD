# Decode check of a rendered MP4: duration, audio track count, and frames grabbed at given seconds.
param([string]$Mp4, [string]$OutDir, [string]$Times)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$ext = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asOp = ($ext | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
function Await($op, [Type]$t) { $task = $asOp.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait(-1) | Out-Null; $task.Result }
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Editing.MediaComposition,Windows.Media.Editing,ContentType=WindowsRuntime] | Out-Null
$f = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Mp4)) ([Windows.Storage.StorageFile])
$clip = Await ([Windows.Media.Editing.MediaClip]::CreateFromFileAsync($f)) ([Windows.Media.Editing.MediaClip])
"duration: " + $clip.OriginalDuration.TotalSeconds
"audio tracks: " + $clip.EmbeddedAudioTracks.Count
$comp = New-Object Windows.Media.Editing.MediaComposition
[System.Collections.Generic.ICollection[Windows.Media.Editing.MediaClip]].GetMethod('Add').Invoke($comp.Clips, @($clip)) | Out-Null
New-Item -ItemType Directory -Force $OutDir | Out-Null
foreach ($t in $Times.Split(',')) {
  $s = Await ($comp.GetThumbnailAsync([TimeSpan]::FromSeconds([double]$t), 960, 540, [Windows.Media.Editing.VideoFramePrecision]::NearestFrame)) ([Windows.Graphics.Imaging.ImageStream])
  $ns = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($s)
  $fs = [System.IO.File]::Create((Join-Path $OutDir ("t_{0:000.0}.jpg" -f [double]$t)))
  $ns.CopyTo($fs); $fs.Close()
}
"frames: " + $Times.Split(',').Count
