param()

$ErrorActionPreference = 'Stop'
$taskRepo = Split-Path -Parent $PSScriptRoot
$taskQuartoCommand = Get-Command quarto -ErrorAction SilentlyContinue
$taskQuarto = if ($taskQuartoCommand) { $taskQuartoCommand.Source } else {
    Join-Path $env:LOCALAPPDATA 'Programs\Quarto\bin\quarto.exe'
}
if (-not (Test-Path -LiteralPath $taskQuarto)) {
    throw 'Quarto was not found. Install Quarto or add it to PATH.'
}

# Keep Sass/Quarto cache outside Dropbox and writable in a restricted session.
$taskOriginalLocalAppData = $env:LOCALAPPDATA
$taskCache = Join-Path $env:TEMP 'automated-test-canext-quarto'
New-Item -ItemType Directory -Path $taskCache -Force | Out-Null
Push-Location $taskRepo
try {
    $env:LOCALAPPDATA = $taskCache
    & $taskQuarto render training_materials
    if ($LASTEXITCODE -ne 0) { throw "Quarto render failed ($LASTEXITCODE)." }
} finally {
    $env:LOCALAPPDATA = $taskOriginalLocalAppData
    Pop-Location
}
