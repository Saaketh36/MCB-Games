# Batch SAPI narration for the listening stories.
# Reads tools\stories.json, writes audio\<slug>.wav plus audio\index.json.
param(
    [string]$StoriesPath = "tools\stories.json",
    [string]$OutDir      = "audio"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Speech -ErrorAction SilentlyContinue

if (-not (Test-Path -LiteralPath $StoriesPath)) { throw "missing $StoriesPath" }
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

$data = Get-Content -Raw -LiteralPath $StoriesPath | ConvertFrom-Json

# Preferred reading voices, first available wins.
$wanted = @("Microsoft David Desktop", "Microsoft Hazel Desktop", "Microsoft Zira Desktop", "Microsoft Aria", "Microsoft Mark")
$voice = $null
try { $voice = New-Object System.Speech.Synthesis.SpeechSynthesizer } catch { $null }
if (-not $voice) { throw "SpeechSynthesizer unavailable" }
$available = @($voice.GetInstalledVoices() | ForEach-Object { $_.VoiceInfo.Name })
$chosen = $null
foreach ($w in $wanted) { if ($available -contains $w) { $chosen = $w; break } }
if ($chosen) { $voice.SelectVoice($chosen) } else { $chosen = $available[0] }
Write-Host "voice: $chosen"
$voice.Rate = -1

function Get-Slug([string]$text) {
    $s = $text.ToLowerInvariant() -replace '[^a-z0-9]+', '-'
    return $s.Trim('-')
}

$index = @{}

foreach ($prop in $data.PSObject.Properties) {
    $title = $prop.Name
    $story = [string]$prop.Value.story
    $slug  = Get-Slug $title
    $wav   = Join-Path $OutDir "$slug.wav"
    $out   = Join-Path (Get-Location) $wav

    if (Test-Path -LiteralPath $wav) {
        Write-Host "skip  $title"
    } else {
        $voice.SetOutputToWaveFile($out)
        $voice.Speak($story)
        $voice.SetOutputToNull()
        Write-Host "wrote $wav"
    }

    # WAV header: 44 bytes, 16-bit mono PCM -> bytes/sec = 44100 * 2 = 88200
    $bytes = (Get-Item -LiteralPath $wav).Length
    $seconds = [math]::Round(($bytes - 44) / 88200.0, 2)

    $index[$slug] = @{
        title    = $title
        file     = ("audio/" + $slug + ".wav")
        words    = ($story -split '\s+').Count
        seconds  = $seconds
        voice    = $chosen
    }
}

$meta = [ordered]@{
    generated = (Get-Date).ToString("s")
    voice     = $chosen
    stories   = $index
}
$json = $meta | ConvertTo-Json -Depth 6
$enc = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText((Join-Path (Get-Location) (Join-Path $OutDir "index.json")), $json, $enc)

$total = 0
foreach ($k in $index.Keys) { $total += [double]$index[$k]["seconds"] }
Write-Host ("done: {0} files, {1:N0}s total narration" -f $index.Count, $total)
