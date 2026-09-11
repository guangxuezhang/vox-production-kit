param([switch]$InstallMissing)
$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
$packages=@{node='OpenJS.NodeJS.LTS';python='Python.Python.3.12';ffmpeg='Gyan.FFmpeg'}
foreach($command in $packages.Keys){
 if(-not(Get-Command $command -ErrorAction SilentlyContinue)){
  if(-not $InstallMissing){throw "Missing $command. Rerun ./bootstrap.ps1 -InstallMissing to install via winget."}
  if(-not(Get-Command winget -ErrorAction SilentlyContinue)){throw 'Install Windows App Installer (winget) first.'}
  winget install --id $packages[$command] --exact --source winget
  if($LASTEXITCODE -ne 0){throw "Installation failed: $command"}
 }
}
$env:Path=[Environment]::GetEnvironmentVariable('Path','Machine')+';'+[Environment]::GetEnvironmentVariable('Path','User')
if(-not(Get-Command pnpm -ErrorAction SilentlyContinue)){
 if(-not $InstallMissing){throw 'Missing pnpm. Rerun with -InstallMissing.'}
 npm install --global pnpm@10
 if($LASTEXITCODE -ne 0){throw 'pnpm installation failed'}
}
& ./setup.ps1
