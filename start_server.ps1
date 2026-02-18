# Code2Video API Server Startup Script
# Automatically clears port and starts the server

param(
    [int]$Port = 8000
)

Write-Host "==========================================="
Write-Host "  Code2Video API Server Launcher"
Write-Host "==========================================="
Write-Host ""

# Clear processes using the port
Write-Host "[1/3] Clearing port $Port ..." -ForegroundColor Yellow

$connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($connections) {
    $pids = $connections.OwningProcess | Sort-Object -Unique
    foreach ($pid in $pids) {
        $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "  Terminating process: $($process.ProcessName) (PID: $pid)" -ForegroundColor Red
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
    Start-Sleep -Seconds 2
    Write-Host "  Port cleared successfully" -ForegroundColor Green
} else {
    Write-Host "  Port $Port is not in use" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[2/3] Activating virtual environment..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
& "$scriptDir\venv\Scripts\Activate.ps1"
Write-Host "  Virtual environment activated" -ForegroundColor Green

# Start server
Write-Host ""
Write-Host "[3/3] Starting API server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "==========================================="
Write-Host "  Server URL: http://localhost:$Port"
Write-Host "  API Docs:   http://localhost:$Port/docs"
Write-Host "  Press Ctrl+C to stop the server"
Write-Host "==========================================="
Write-Host ""

Set-Location "$scriptDir\src"
python -m uvicorn api_server:app --host 0.0.0.0 --port $Port
