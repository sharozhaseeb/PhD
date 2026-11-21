# Render clips.txt (image|seconds per line) + mix.wav to H.264/AAC 1080p MP4 with Windows MediaComposition.
param([string]$Clips, [string]$Audio, [string]$Out)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$ext = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asOp = ($ext | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
$asProg = ($ext | ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperationWithProgress`2' })[0]
function Await($op, [Type]$t) { $task = $asOp.MakeGenericMethod($t).Invoke($null, @($op)); $task.Wait(-1) | Out-Null; $task.Result }
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Editing.MediaComposition,Windows.Media.Editing,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.MediaProperties.MediaEncodingProfile,Windows.Media.MediaProperties,ContentType=WindowsRuntime] | Out-Null
$SF = [Windows.Storage.StorageFile]; $MC = [Windows.Media.Editing.MediaClip]
$addClip = [System.Collections.Generic.ICollection[Windows.Media.Editing.MediaClip]].GetMethod('Add')
$addBg = [System.Collections.Generic.ICollection[Windows.Media.Editing.BackgroundAudioTrack]].GetMethod('Add')
$comp = New-Object Windows.Media.Editing.MediaComposition
$n = 0
foreach ($line in Get-Content -Encoding UTF8 $Clips) {
  $p, $d = $line.Split('|')
  $f = Await ($SF::GetFileFromPathAsync($p)) $SF
  $c = Await ($MC::CreateFromImageFileAsync($f, [TimeSpan]::FromTicks([long]([double]$d * 1e7)))) $MC
  $addClip.Invoke($comp.Clips, @($c)) | Out-Null; $n++
}
"clips: $n  duration: " + $comp.Duration
$af = Await ($SF::GetFileFromPathAsync($Audio)) $SF
$bt = Await ([Windows.Media.Editing.BackgroundAudioTrack]::CreateFromFileAsync($af)) ([Windows.Media.Editing.BackgroundAudioTrack])
$addBg.Invoke($comp.BackgroundAudioTracks, @($bt)) | Out-Null
$dir = Await ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync((Split-Path $Out))) ([Windows.Storage.StorageFolder])
$of = Await ($dir.CreateFileAsync((Split-Path $Out -Leaf), [Windows.Storage.CreationCollisionOption]::ReplaceExisting)) $SF
$prof = [Windows.Media.MediaProperties.MediaEncodingProfile]::CreateMp4([Windows.Media.MediaProperties.VideoEncodingQuality]::HD1080p)
$prof.Video.FrameRate.Numerator = 30; $prof.Video.FrameRate.Denominator = 1; $prof.Video.Bitrate = 2500000; $prof.Audio.Bitrate = 128000
$op = $comp.RenderToFileAsync($of, [Windows.Media.Editing.MediaTrimmingPreference]::Precise, $prof)
$task = $asProg.MakeGenericMethod([Windows.Media.Transcoding.TranscodeFailureReason], [double]).Invoke($null, @($op))
$task.Wait(-1) | Out-Null
"render: " + $task.Result
