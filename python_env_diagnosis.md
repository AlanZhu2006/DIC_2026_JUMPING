# Python 环境诊断报告

## 🔍 当前问题

### 1. Python 环境冲突
- **当前默认 Python**: `C:\msys64\mingw64\bin\python.exe` (MSYS2 环境)
- **Python 版本**: 3.14.2
- **问题**: 这个 Python **没有安装 pip 模块**

### 2. 环境混乱
- 之前安装 `python-docx` 时使用的是另一个 Python 环境（可能是 Windows Store 的 Python）
- 不同命令可能指向不同的 Python 环境
- 没有项目专用的虚拟环境

### 3. 项目依赖问题
- Code2Video 项目需要大量依赖（manim, openai, numpy, scipy 等）
- 这些依赖需要正确安装到正确的 Python 环境中

---

## ✅ 解决方案

### 方案 1：使用 Windows Store Python（推荐）

如果您有 Windows Store 的 Python 安装：

```powershell
# 1. 找到 Windows Store Python 的路径
# 通常在：C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe

# 2. 使用完整路径创建虚拟环境
cd C:\Users\zhuya\Desktop\Code2Video
C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe -m venv venv

# 3. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 4. 安装依赖
cd src
pip install -r requirements.txt
```

### 方案 2：安装标准 Python（最推荐）

1. **下载并安装 Python 3.11 或 3.12**
   - 访问：https://www.python.org/downloads/
   - 下载 Windows installer
   - **重要**：安装时勾选 "Add Python to PATH"

2. **验证安装**
   ```powershell
   python --version
   pip --version
   ```

3. **创建虚拟环境**
   ```powershell
   cd C:\Users\zhuya\Desktop\Code2Video
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **安装项目依赖**
   ```powershell
   cd src
   pip install -r requirements.txt
   ```

### 方案 3：修复 MSYS2 Python（不推荐）

如果您想继续使用 MSYS2 的 Python：

```bash
# 在 MSYS2 终端中运行
pacman -S python-pip
```

但**不推荐**这个方案，因为：
- MSYS2 环境主要用于 Unix 工具，不适合 Python 项目开发
- 可能与 Windows 原生工具冲突

---

## 🔧 快速修复步骤（推荐）

### 步骤 1：检查是否有其他 Python

```powershell
# 检查 Windows Store Python
Test-Path "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe"

# 检查标准安装
Get-ChildItem "C:\Program Files\Python*" -ErrorAction SilentlyContinue
Get-ChildItem "C:\Users\zhuya\AppData\Local\Programs\Python" -ErrorAction SilentlyContinue
```

### 步骤 2：创建虚拟环境（使用找到的 Python）

```powershell
# 如果找到 Windows Store Python
& "C:\Users\zhuya\AppData\Local\Microsoft\WindowsApps\python.exe" -m venv venv

# 或者如果安装了标准 Python（确保在 PATH 中）
python -m venv venv
```

### 步骤 3：激活并安装

```powershell
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 升级 pip
python -m pip install --upgrade pip

# 安装项目依赖
cd src
pip install -r requirements.txt
```

### 步骤 4：验证安装

```powershell
python -c "import manim; print('Manim installed successfully')"
python -c "import openai; print('OpenAI installed successfully')"
```

---

## 📝 环境变量检查

检查 PATH 环境变量中 Python 的顺序：

```powershell
$env:PATH -split ';' | Where-Object { $_ -like '*python*' -or $_ -like '*Python*' }
```

**建议**：将标准 Python 安装路径放在 MSYS2 路径之前。

---

## 🎯 最佳实践建议

1. **使用虚拟环境**：为每个项目创建独立的虚拟环境
2. **使用标准 Python**：安装官方 Python，而不是依赖 MSYS2
3. **固定 Python 版本**：使用 Python 3.11 或 3.12（与 Manim 兼容性最好）
4. **使用 requirements.txt**：确保依赖版本一致

---

## ⚠️ 注意事项

- **Manim 要求**：Manim Community v0.19.0 需要特定的系统依赖（FFmpeg, LaTeX 等）
- **权限问题**：如果遇到权限错误，可能需要以管理员身份运行
- **PATH 冲突**：确保 PATH 中标准 Python 在 MSYS2 Python 之前

---

## 🆘 如果仍有问题

1. 检查 Python 安装是否完整
2. 检查防火墙/杀毒软件是否阻止 pip
3. 尝试使用 `python -m pip` 而不是直接使用 `pip`
4. 检查网络连接（pip 需要下载包）
