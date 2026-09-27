# Recreates a fresh, machine-local virtual environment for this assignment.
# Run this any time you switch computers (PC <-> laptop) and hit
# "No Python at ..." errors - a .venv folder is tied to the machine that
# created it and does not survive being synced by OneDrive.
#
# IMPORTANT: run this from a FRESH PowerShell window (not one where a
# broken .venv is already activated), so PATH isn't polluted by it.

$ErrorActionPreference = "Stop"

if ($env:VIRTUAL_ENV) {
    deactivate
}

if (Test-Path ".venv") {
    Remove-Item -Recurse -Force ".venv"
    Write-Host "Removed old .venv"
}

# Find a real, working Python on THIS machine.
# Prefer the py launcher; fall back to whatever 'python' resolves to.
$pythonCmd = $null

if (Get-Command py -ErrorAction SilentlyContinue) {
    $v = & py --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "py -3"
        Write-Host "Using py launcher: $v"
    }
}

if (-not $pythonCmd -and (Get-Command python -ErrorAction SilentlyContinue)) {
    $v = & python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "python"
        Write-Host "Using python: $v"
    }
}

if (-not $pythonCmd) {
    Write-Host "No working Python found on this machine."
    Write-Host "Install it from https://www.python.org/downloads/windows/"
    Write-Host "During install, check both 'Add python.exe to PATH' and 'Install launcher for all users'."
    Write-Host "Then open a NEW PowerShell window and re-run this script."
    exit 1
}

Invoke-Expression "$pythonCmd -m venv .venv"
Write-Host "Created new .venv"

. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requires.txt

Write-Host "Done. Venv is ready on this machine."
