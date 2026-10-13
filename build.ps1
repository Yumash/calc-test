$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
    py -3.11 -m venv (Join-Path $projectRoot ".venv")
}

& $python -m pip install --disable-pip-version-check -e "${projectRoot}[dev]"
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }

& $python -m pytest
if ($LASTEXITCODE -ne 0) { throw "Tests failed." }

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name Calculator `
    --paths (Join-Path $projectRoot "src") `
    (Join-Path $projectRoot "src\calculator\app.py")
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

$artifact = Join-Path $projectRoot "dist\Calculator.exe"
if (-not (Test-Path -LiteralPath $artifact)) { throw "Build artifact was not created." }
Write-Host "Built: $artifact"
