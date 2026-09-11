param([switch]$Install)
$ErrorActionPreference='Stop'
Write-Host 'Checking VOX production dependencies...'
foreach ($cmd in @('node','pnpm','python','ffmpeg')) { if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) { Write-Warning "$cmd is missing" } else { & $cmd --version | Select-Object -First 1 } }
if ($Install -and (Test-Path 'remotion\package.json')) { pnpm --dir remotion install }
Write-Host 'Create .env from .env.example and set credentials locally. Keys are never committed.'
