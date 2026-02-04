# VisualKiwi/Code2Video Python 环境设置脚本
# 此脚本将帮助您设置正确的 Python 环境

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python 环境诊断和设置" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查可用的 Python
Write-Host "[1/5] 检查 Python 环境..." -ForegroundColor Yellow

$pythonPaths = @()
$msys2Python = "C:\msys64\mingw64\bin\python.exe"
$windowsStorePython = "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe"

if (Test-Path $windowsStorePython) {
    $version = & $windowsStorePython --version 2>&1
    Write-Host "  ✓ 找到 Windows Store Python: $version" -ForegroundColor Green
    $pythonPaths += @{
        Path = $windowsStorePython
        Type = "Windows Store"
        Version = $version
    }
}

if (Test-Path $msys2Python) {
    $version = & $msys2Python --version 2>&1
    Write-Host "  ⚠ 找到 MSYS2 Python: $version (没有 pip，不推荐用于项目)" -ForegroundColor Yellow
    $pythonPaths += @{
        Path = $msys2Python
        Type = "MSYS2"
        Version = $version
        HasPip = $false
    }
}

# 检查当前默认 Python
Write-Host ""
Write-Host "当前默认 Python:" -ForegroundColor Yellow
$currentPython = (Get-Command python -ErrorAction SilentlyContinue).Source
if ($currentPython) {
    Write-Host "  $currentPython" -ForegroundColor White
    if ($currentPython -like "*msys64*") {
        Write-Host "  ⚠ 警告: 当前默认 Python 是 MSYS2 版本，没有 pip！" -ForegroundColor Red
    }
} else {
    Write-Host "  未找到 python 命令" -ForegroundColor Red
}

Write-Host ""

# 2. 选择推荐的 Python
Write-Host "[2/5] 选择 Python 环境..." -ForegroundColor Yellow

$recommendedPython = $null
foreach ($py in $pythonPaths) {
    if ($py.Type -eq "Windows Store" -and (Test-Path $py.Path)) {
        # 检查是否有 pip
        try {
            $pipCheck = & $py.Path -m pip --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                $recommendedPython = $py.Path
                Write-Host "  ✓ 推荐使用: $($py.Path) ($($py.Version))" -ForegroundColor Green
                break
            }
        } catch {
            Write-Host "  ⚠ $($py.Path) 没有 pip" -ForegroundColor Yellow
        }
    }
}

if (-not $recommendedPython) {
    Write-Host "  ❌ 未找到可用的 Python（带 pip）" -ForegroundColor Red
    Write-Host "  请先安装 Python 3.11 或 3.12: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 3. 检查虚拟环境
Write-Host ""
Write-Host "[3/5] 检查虚拟环境..." -ForegroundColor Yellow

$venvPath = Join-Path $PSScriptRoot "venv"
if (Test-Path $venvPath) {
    Write-Host "  ✓ 找到现有虚拟环境: $venvPath" -ForegroundColor Green
    $createVenv = Read-Host "  是否重新创建虚拟环境？(y/N)"
    if ($createVenv -eq "y" -or $createVenv -eq "Y") {
        Remove-Item $venvPath -Recurse -Force
        Write-Host "  ✓ 已删除旧虚拟环境" -ForegroundColor Green
        $shouldCreateVenv = $true
    } else {
        $shouldCreateVenv = $false
    }
} else {
    Write-Host "  ℹ 未找到虚拟环境，将创建新的" -ForegroundColor Cyan
    $shouldCreateVenv = $true
}

# 4. 创建虚拟环境
if ($shouldCreateVenv) {
    Write-Host ""
    Write-Host "[4/5] 创建虚拟环境..." -ForegroundColor Yellow
    Write-Host "  使用 Python: $recommendedPython" -ForegroundColor White
    
    try {
        & $recommendedPython -m venv $venvPath
        Write-Host "  ✓ 虚拟环境创建成功！" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ 创建虚拟环境失败: $_" -ForegroundColor Red
        exit 1
    }
}

# 5. 激活并安装依赖
Write-Host ""
Write-Host "[5/5] 安装项目依赖..." -ForegroundColor Yellow

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Host "  ❌ 虚拟环境激活脚本不存在" -ForegroundColor Red
    exit 1
}

# 激活虚拟环境
. $activateScript

# 升级 pip
Write-Host "  升级 pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip --quiet

# 安装依赖
Write-Host "  安装项目依赖（这可能需要几分钟）..." -ForegroundColor Cyan
$requirementsPath = Join-Path $PSScriptRoot "src\requirements.txt"
if (Test-Path $requirementsPath) {
    pip install -r $requirementsPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ 依赖安装成功！" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ 依赖安装过程中出现错误，请检查输出" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠ 未找到 requirements.txt: $requirementsPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "设置完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "使用方法:" -ForegroundColor Yellow
Write-Host "  1. 激活虚拟环境: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. 运行项目: cd src; python agent.py ..." -ForegroundColor White
Write-Host "  3. 退出虚拟环境: deactivate" -ForegroundColor White
Write-Host ""
