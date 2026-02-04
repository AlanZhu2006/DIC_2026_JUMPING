# Simple Python PATH Fix Script
# This script will fix the Python PATH issue by creating aliases

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python PATH Fix Tool" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$pythonExe = "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe"

if (-not (Test-Path $pythonExe)) {
    Write-Host "Error: Windows Store Python not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Found Python: $pythonExe" -ForegroundColor Green
$version = & $pythonExe --version
Write-Host "Version: $version" -ForegroundColor Green
Write-Host ""

# Create aliases for current session
Write-Host "Creating aliases for current session..." -ForegroundColor Yellow

function global:python {
    & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" $args
}

function global:pip {
    & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" -m pip $args
}

Write-Host "  [OK] Aliases created" -ForegroundColor Green
Write-Host ""

# Test
Write-Host "Testing..." -ForegroundColor Yellow
$testVersion = python --version 2>&1
Write-Host "  python --version: $testVersion" -ForegroundColor White

$testPip = pip --version 2>&1
Write-Host "  pip --version: $testPip" -ForegroundColor White
Write-Host ""

# Add to PowerShell profile
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $profilePath -Parent

if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$aliasCode = @"
# VisualKiwi Python Aliases (Auto-added)
function python {
    & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" `$args
}
function pip {
    & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" -m pip `$args
}
"@

Write-Host "Adding aliases to PowerShell profile..." -ForegroundColor Yellow
Write-Host "  Profile path: $profilePath" -ForegroundColor Gray

if (-not (Test-Path $profilePath)) {
    $aliasCode | Out-File $profilePath -Encoding UTF8
    Write-Host "  [OK] Profile created with aliases" -ForegroundColor Green
} else {
    $content = Get-Content $profilePath -Raw -ErrorAction SilentlyContinue
    if ($content -and $content -notlike "*VisualKiwi Python Aliases*") {
        Add-Content $profilePath "`n$aliasCode"
        Write-Host "  [OK] Aliases added to existing profile" -ForegroundColor Green
    } else {
        Write-Host "  [SKIP] Aliases already exist in profile" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fix Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current session: Aliases are active now" -ForegroundColor Green
Write-Host "Future sessions: Aliases will load automatically" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Test: python --version" -ForegroundColor White
Write-Host "  2. Create venv: python -m venv venv" -ForegroundColor White
Write-Host "  3. Activate: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
