# 修复 Python PATH 环境变量问题
# 将 Windows Store Python 路径移到 MSYS2 路径之前

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python PATH 环境变量修复工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查当前权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

Write-Host "当前问题:" -ForegroundColor Yellow
Write-Host "  MSYS2 路径在 Windows Store Python 之前" -ForegroundColor White
Write-Host "  导致 'python' 命令指向 MSYS2 的 Python（没有 pip）" -ForegroundColor White
Write-Host ""

# 获取当前 PATH
$machinePath = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
$userPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')

Write-Host "当前 PATH 中的相关路径:" -ForegroundColor Yellow
$allPaths = ($machinePath + ';' + $userPath) -split ';' | Where-Object { $_ }
$msysPaths = @()
$pythonPaths = @()

for ($i = 0; $i -lt $allPaths.Length; $i++) {
    $path = $allPaths[$i]
    if ($path -like '*msys*' -or $path -like '*mingw*') {
        $msysPaths += @{Index = $i; Path = $path}
        Write-Host "  [$i] $path (MSYS2)" -ForegroundColor Red
    }
    if ($path -like '*WindowsApps*' -or ($path -like '*Python*' -and $path -notlike '*msys*' -and $path -notlike '*mingw*')) {
        $pythonPaths += @{Index = $i; Path = $path}
        Write-Host "  [$i] $path (Python)" -ForegroundColor Green
    }
}

Write-Host ""

# 方案 1: 修改用户级 PATH（推荐，不需要管理员权限）
Write-Host "方案 1: 修改用户级 PATH（推荐）" -ForegroundColor Cyan
Write-Host "  优点: 不需要管理员权限，只影响当前用户" -ForegroundColor White
Write-Host "  缺点: 需要重新打开终端才能生效" -ForegroundColor White
Write-Host ""

# 方案 2: 创建别名/函数
Write-Host "方案 2: 创建 PowerShell 别名（临时方案）" -ForegroundColor Cyan
Write-Host "  优点: 立即生效，不需要修改系统设置" -ForegroundColor White
Write-Host "  缺点: 只在当前 PowerShell 会话有效" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请选择方案 (1=修改PATH, 2=创建别名, 3=仅查看, 其他=取消)"

if ($choice -eq "1") {
    # 修改用户级 PATH
    Write-Host ""
    Write-Host "正在修改用户级 PATH..." -ForegroundColor Yellow
    
    $userPathArray = $userPath -split ';' | Where-Object { $_ }
    $msysInUser = $userPathArray | Where-Object { $_ -like '*msys*' -or $_ -like '*mingw*' }
    $pythonInUser = $userPathArray | Where-Object { $_ -like '*WindowsApps*' }
    
    # 移除 MSYS2 路径
    $newUserPath = $userPathArray | Where-Object { $_ -notlike '*msys*' -and $_ -notlike '*mingw*' }
    
    # 将 Python 路径移到最前面
    if ($pythonInUser) {
        $newUserPath = @($pythonInUser) + ($newUserPath | Where-Object { $_ -notlike '*WindowsApps*' })
    }
    
    # 将 MSYS2 路径移到后面
    if ($msysInUser) {
        $newUserPath = $newUserPath + $msysInUser
    }
    
    $newUserPathString = $newUserPath -join ';'
    
    try {
        [System.Environment]::SetEnvironmentVariable('Path', $newUserPathString, 'User')
        Write-Host "  ✓ 用户级 PATH 已更新" -ForegroundColor Green
        Write-Host ""
        Write-Host "  重要: 请关闭并重新打开 PowerShell 终端，使更改生效！" -ForegroundColor Yellow
        Write-Host "  或者运行: refreshenv" -ForegroundColor Yellow
    } catch {
        Write-Host "  ❌ 修改失败: $_" -ForegroundColor Red
    }
    
} elseif ($choice -eq "2") {
    # 创建 PowerShell 别名
    Write-Host ""
    Write-Host "创建 PowerShell 别名..." -ForegroundColor Yellow
    
    $pythonExe = "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe"
    
    if (Test-Path $pythonExe) {
        # 创建函数来覆盖 python 命令
        function global:python {
            & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" $args
        }
        
        # 也覆盖 pip（如果存在）
        $pipExe = "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\pip.exe"
        if (Test-Path $pipExe) {
            function global:pip {
                & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\pip.exe" $args
            }
        }
        
        Write-Host "  ✓ 别名已创建（仅在当前会话有效）" -ForegroundColor Green
        Write-Host ""
        Write-Host "  测试: python --version" -ForegroundColor Yellow
        python --version
        
        # 保存到 PowerShell 配置文件
        $profilePath = $PROFILE.CurrentUserAllHosts
        $profileDir = Split-Path $profilePath -Parent
        if (-not (Test-Path $profileDir)) {
            New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
        }
        
        $aliasCode = @"
# VisualKiwi Python 别名（自动添加）
function python {
    & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" `$args
}
function pip {
    & "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" -m pip `$args
}
"@
        
        $addToProfile = Read-Host "是否将别名添加到 PowerShell 配置文件以永久生效？(Y/n)"
        if ($addToProfile -ne "n" -and $addToProfile -ne "N") {
            if (-not (Test-Path $profilePath)) {
                $aliasCode | Out-File $profilePath -Encoding UTF8
            } else {
                $content = Get-Content $profilePath -Raw
                if ($content -notlike "*VisualKiwi Python 别名*") {
                    Add-Content $profilePath "`n$aliasCode"
                }
            }
            Write-Host "  ✓ 已添加到 PowerShell 配置文件: $profilePath" -ForegroundColor Green
            Write-Host "  重新打开 PowerShell 后会自动加载" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ❌ 未找到 Windows Store Python" -ForegroundColor Red
    }
    
} elseif ($choice -eq "3") {
    Write-Host ""
    Write-Host "PATH 分析完成" -ForegroundColor Green
} else {
    Write-Host "已取消" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "提示: 推荐使用虚拟环境来避免 PATH 冲突" -ForegroundColor Yellow
Write-Host "  运行: .\setup_python_env.ps1" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
