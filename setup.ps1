param([switch]$CheckOnly)
$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
foreach ($tool in @('node','pnpm','python','ffmpeg','ffprobe')) {
 if (-not (Get-Command $tool -ErrorAction SilentlyContinue)) { throw "Missing dependency: $tool. Install it and rerun setup." }
}
if ($CheckOnly) { Write-Host 'Dependency commands are available'; exit 0 }
pnpm --dir remotion install --frozen-lockfile
if ($LASTEXITCODE -ne 0) { throw 'Node dependency installation failed' }
python -m venv .venv
& ./.venv/Scripts/python.exe -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Python dependency installation failed' }
New-Item -ItemType Directory -Force outputs/own-framework | Out-Null
Write-Host 'Ready. Run pnpm --dir remotion dev or pnpm --dir remotion render.'
