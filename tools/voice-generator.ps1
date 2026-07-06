# ElevenLabs Voice Generator — Small Chunks Version
param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptPath,
    [string]$VoiceId = "JBFqnCBsd6RMkjVDRZzb",
    [double]$Speed = 1.0,
    [string]$OutputName = "voiceover.mp3"
)

$apiKey = "sk_2cc29084a821a5050700ec626a7d579d6ef9f71ae7efaeb2"

if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found: $ScriptPath" -ForegroundColor Red
    exit 1
}

# Read script as UTF-8
$text = [System.IO.File]::ReadAllText((Resolve-Path $ScriptPath).Path, [System.Text.Encoding]::UTF8)
$charCount = $text.Length

Write-Host "Script: $ScriptPath" -ForegroundColor Cyan
Write-Host "Characters: $charCount" -ForegroundColor Cyan
Write-Host "Credits needed: ~$charCount" -ForegroundColor Yellow
Write-Host ""

# Split into small chunks (max 150 chars to be safe)
$maxChars = 150
$chunks = @()

# Split by paragraphs first, then by sentences if needed
$paragraphs = $text -split "`n`n"
foreach ($para in $paragraphs) {
    if ($para.Length -le $maxChars) {
        $chunks += $para.Trim()
    } else {
        # Split long paragraphs by sentences
        $sentences = $para -split '(?<=[.!?])\s+'
        $current = ""
        foreach ($sentence in $sentences) {
            if (($current.Length + $sentence.Length) -gt $maxChars -and $current.Length -gt 0) {
                $chunks += $current.Trim()
                $current = $sentence
            } else {
                $current += " " + $sentence
            }
        }
        if ($current.Trim().Length -gt 0) {
            $chunks += $current.Trim()
        }
    }
}

Write-Host "Split into $($chunks.Count) chunks (max $maxChars chars each)" -ForegroundColor Yellow
Write-Host ""

# Generate audio
$outputDir = Split-Path $ScriptPath
$allChunks = @()
$totalCredits = 0

for ($i = 0; $i -lt $chunks.Count; $i++) {
    $chunk = $chunks[$i]
    $chunkFile = Join-Path $outputDir "temp_chunk_$i.mp3"
    
    Write-Host "Chunk $($i+1)/$($chunks.Count) ($($chunk.Length) chars)..." -ForegroundColor Green -NoNewline
    
    # Build JSON as bytes
    $jsonPrefix = [System.Text.Encoding]::UTF8.GetBytes('{"text":"')
    $escapedText = $chunk -replace '\\', '\\\\' -replace '"', '\"' -replace "`n", '\n' -replace "`r", '\r'
    $textBytes = [System.Text.Encoding]::UTF8.GetBytes($escapedText)
    $jsonSuffix = [System.Text.Encoding]::UTF8.GetBytes('","model_id":"eleven_v3","voice_settings":{"stability":0.5,"similarity_boost":0.75,"speed":' + $Speed.ToString() + '}}')
    
    $bodyBytes = New-Object byte[] ($jsonPrefix.Length + $textBytes.Length + $jsonSuffix.Length)
    [System.Buffer]::BlockCopy($jsonPrefix, 0, $bodyBytes, 0, $jsonPrefix.Length)
    [System.Buffer]::BlockCopy($textBytes, 0, $bodyBytes, $jsonPrefix.Length, $textBytes.Length)
    [System.Buffer]::BlockCopy($jsonSuffix, 0, $bodyBytes, $jsonPrefix.Length + $textBytes.Length, $jsonSuffix.Length)
    
    try {
        $request = [System.Net.HttpWebRequest]::Create("https://api.elevenlabs.io/v1/text-to-speech/$VoiceId")
        $request.Method = "POST"
        $request.ContentType = "application/json; charset=utf-8"
        $request.Accept = "audio/mpeg"
        $request.Headers.Add("xi-api-key", $apiKey)
        
        $stream = $request.GetRequestStream()
        $stream.Write($bodyBytes, 0, $bodyBytes.Length)
        $stream.Close()
        
        $response = $request.GetResponse()
        $responseStream = $response.GetResponseStream()
        
        $fileStream = [System.IO.File]::Create($chunkFile)
        $responseStream.CopyTo($fileStream)
        $fileStream.Close()
        $responseStream.Close()
        $response.Close()
        
        $allChunks += $chunkFile
        $totalCredits += $chunk.Length
        Write-Host " OK" -ForegroundColor Green
    } catch {
        Write-Host " ERROR" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Yellow
        exit 1
    }
    
    Start-Sleep -Milliseconds 500
}

# Combine chunks
$outputPath = Join-Path $outputDir $OutputName
Write-Host ""
Write-Host "Combining $($allChunks.Count) chunks..." -ForegroundColor Cyan

$finalStream = [System.IO.File]::Create($outputPath)
foreach ($chunkFile in $allChunks) {
    $chunkBytes = [System.IO.File]::ReadAllBytes($chunkFile)
    $finalStream.Write($chunkBytes, 0, $chunkBytes.Length)
}
$finalStream.Close()

# Clean up
foreach ($chunkFile in $allChunks) {
    Remove-Item $chunkFile -Force
}

$fileSize = (Get-Item $outputPath).Length / 1KB
$estMinutes = [math]::Round($charCount / 150, 1)

Write-Host ""
Write-Host "SUCCESS!" -ForegroundColor Green
Write-Host "Saved to: $outputPath" -ForegroundColor Green
Write-Host "File size: $([math]::Round($fileSize, 1)) KB" -ForegroundColor Cyan
Write-Host "Credits used: ~$totalCredits" -ForegroundColor Cyan
Write-Host "Estimated duration: ~$estMinutes minutes" -ForegroundColor Cyan
Write-Host ""
Write-Host "NEXT STEP: Import this MP3 into CapCut" -ForegroundColor Yellow
