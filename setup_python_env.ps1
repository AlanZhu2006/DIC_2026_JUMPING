# VisualKiwi/Code2Video Python Environment Setup Script
# This script will help you set up the correct Python environment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python Environment Diagnosis and Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Check available Python installations
Write-Host "[1/5] Checking Python environment..." -ForegroundColor Yellow

$pythonPaths = @()
$msys2Python = "C:\msys64\mingw64\bin\python.exe"
$windowsStorePython = "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe"

if (Test-Path $windowsStorePython) {
    $version = & $windowsStorePython --version 2>&1
    Write-Host "  Found Windows Store Python: $version" -ForegroundColor Green
    $pythonPaths += @{
        Path = $windowsStorePython
        Type = "Windows Store"
        Version = $version
    }
}

if (Test-Path $msys2Python) {
    $version = & $msys2Python --version 2>&1
    Write-Host "  Found MSYS2 Python: $version (no pip, not recommended for projects)" -ForegroundColor Yellow
    $pythonPaths += @{
        Path = $msys2Python
        Type = "MSYS2"
        Version = $version
        HasPip = $false
    }
}

# Check current default Python
Write-Host ""
Write-Host "Current default Python:" -ForegroundColor Yellow
$currentPython = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($currentPython) {
    Write-Host "  $currentPython" -ForegroundColor White
    if ($currentPython -like "*msys64*") {
        Write-Host "  Warning: Current default Python is MSYS2 version, no pip!" -ForegroundColor Red
    }
} else {
    Write-Host "  python command not found" -ForegroundColor Red
}

Write-Host ""

# 2. Select recommended Python
Write-Host "[2/5] Selecting Python environment..." -ForegroundColor Yellow

$recommendedPython = $null
foreach ($py in $pythonPaths) {
    if ($py.Type -eq "Windows Store" -and (Test-Path $py.Path)) {
        # Check if pip is available
        try {
            $pipCheck = & $py.Path -m pip --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $recommendedPython = $py.Path
                Write-Host "  Recommended: $($py.Path) ($($py.Version))" -ForegroundColor Green
                break
            }
        } catch {
            Write-Host "  $($py.Path) has no pip" -ForegroundColor Yellow
        }
    }
}

if (-not $recommendedPython) {
    Write-Host "  No available Python (with pip) found" -ForegroundColor Red
    Write-Host "  Please install Python 3.11 or 3.12: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 3. Check virtual environment
Write-Host ""
Write-Host "[3/5] Checking virtual environment..." -ForegroundColor Yellow

$venvPath = Join-Path $PSScriptRoot "venv"
if (Test-Path $venvPath) {
    Write-Host "  Found existing virtual environment: $venvPath" -ForegroundColor Green
    $createVenv = Read-Host "  Recreate virtual environment? (y/N)"
    if ($createVenv -eq "y" -or $createVenv -eq "Y") {
        Remove-Item $venvPath -Recurse -Force
        Write-Host "  Deleted old virtual environment" -ForegroundColor Green
        $shouldCreateVenv = $true
    } else {
        $shouldCreateVenv = $false
    }
} else {
    Write-Host "  No virtual environment found, will create new one" -ForegroundColor Cyan
    $shouldCreateVenv = $true
}

# 4. Create virtual environment
if ($shouldCreateVenv) {
    Write-Host ""
    Write-Host "[4/5] Creating virtual environment..." -ForegroundColor Yellow
    Write-Host "  Using Python: $recommendedPython" -ForegroundColor White
    
    try {
        & $recommendedPython -m venv $venvPath
        Write-Host "  Virtual environment created successfully!" -ForegroundColor Green
    } catch {
        Write-Host "  Failed to create virtual environment: $_" -ForegroundColor Red
        exit 1
    }
}

# 5. Activate and install dependencies
Write-Host ""
Write-Host "[5/5] Installing project dependencies..." -ForegroundColor Yellow

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "  Virtual environment activation script not found" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
. $activateScript

# Upgrade pip
Write-Host "  Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# Install dependencies
Write-Host "  Installing project dependencies (this may take a few minutes)..." -ForegroundColor Cyan
$requirementsPath = Join-Path $PSScriptRoot "src\requirements.txt"
if (Test-Path $requirementsPath) {
    pip install -r $requirementsPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "  Errors occurred during dependency installation, please check output" -ForegroundColor Yellow
    }
} else {
    Write-Host "  requirements.txt not found: $requirementsPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  1. Activate virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Run project: cd src; python agent.py ..." -ForegroundColor White
Write-Host "  3. Deactivate virtual environment: deactivate" -ForegroundColor White
Write-Host ""
