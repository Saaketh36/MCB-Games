# Tunes each narration to land inside the 11-15s window by adjusting the SAPI
# speech rate only. Story text is never modified, so the questions that are
# derived from each passage stay valid.
#
#   powershell -ExecutionPolicy Bypass -File tools\tune_audio.ps1
#
param(
    [double]$Low  = 11.0,
    [double]$High = 15.0,
    [double]$Aim  = 13.0
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
Add-Type -AssemblyName System.Speech

$stories = Get-Content -Raw -LiteralPath "tools\stories.json" | ConvertFrom-Json
$indexPath = "audio\index.json"
$index = Get-Content -Raw -LiteralPath $indexPath | ConvertFrom-Json

$voice = New-Object System.Speech.Synthesis.SpeechSynthesizer
$wanted = @("Microsoft David Desktop", "Microsoft Hazel Desktop", "Microsoft Zira Desktop")
$available = @($voice.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name })
$chosen = $null
foreach ($w in $wanted) { if ($available -contains $w) { $chosen = $w; break } }
if ($chosen) { $voice.SelectVoice($chosen) } else { $chosen = $available[0] }
Write-Host "voice: $chosen"

function Measure-Wav([string]$path) {
    $bytes = (Get-Item -LiteralPath $path).Length
    return ($bytes - 44) / 88200.0
}

$changed = 0
foreach ($slug in @($index.stories.PSObject.Properties.Name)) {
    $meta = $index.stories.$slug
    $cur = [double]$meta.seconds
    if ($cur -ge $Low -and $cur -le $High) { continue }

    $story = $null
    foreach ($p in $stories.PSObject.Properties) {
        if ($p.Name.ToLowerInvariant() -replace '[^a-z0-9]+', '-' -replace '^-+|-+$', '' -eq $slug) {
            $story = [string]$p.Value.story; break
        }
    }
    if (-not $story) { Write-Host "no text for $slug"; continue }

    $final = "audio\$slug.wav"
    $tmp = "audio\_tune_$slug.wav"
    $rate = if ($meta.PSObject.Properties.Name -contains 'rate') { [int]$meta.rate } else { -1 }

    # Walk the rate away from the current one until the clip fits the window.
    $bestRate = $null; $bestSec = $null
    for ($step = 0; $step -lt 7; $step++) {
        if ($cur -lt $Low) { $rate-- } else { $rate++ }
        $voice.Rate = $rate
        $voice.SetOutputToWaveFile((Join-Path (Get-Location) $tmp))
        $voice.Speak($story)
        $voice.SetOutputToNull()
        $sec = Measure-Wav $tmp
        Write-Host ("  {0,-34} rate {1,3} -> {2,6:N2}s" -f $slug, $rate, $sec)
        if ($sec -ge $Low -and $sec -le $High) { $bestRate = $rate; $bestSec = $sec; break }
        if ($null -eq $bestSec -or [Math]::Abs($sec - $Aim) -lt [Math]::Abs($bestSec - $Aim)) {
            $bestRate = $rate; $bestSec = $sec
        }
    }

    if ($null -ne $bestRate) {
        $voice.Rate = $bestRate
        $voice.SetOutputToWaveFile((Join-Path (Get-Location) $final))
        $voice.Speak($story)
        $voice.SetOutputToNull()
        $meta | Add-Member -NotePropertyName rate -NotePropertyValue $bestRate -Force
        $meta.seconds = [math]::Round((Measure-Wav $final), 2)
        $changed++
        Write-Host ("  -> kept {0} at rate {1}, {2}s" -f $slug, $bestRate, $meta.seconds)
    }
    if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
}

$enc = New-Object System.Text.UTF8Encoding $false
$json = $index | ConvertTo-Json -Depth 6
[System.IO.File]::WriteAllText((Join-Path (Get-Location) $indexPath), $json, $enc)
Write-Host ""
Write-Host "retuned $changed narration file(s)"