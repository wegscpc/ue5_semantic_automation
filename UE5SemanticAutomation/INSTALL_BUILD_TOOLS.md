# 🔧 Install Visual Studio Build Tools for UE5 Plugin

## Problem

UE 5.7 requires **MSVC v14.44+** but your system has **v14.40-14.43** (incompatible).

## Solution: Install via winget (Recommended)

This method installs **only** the C++ build tools without the full Visual Studio IDE.

---

## 📋 Prerequisites

- Windows 10/11
- PowerShell (Run as Administrator)
- `winget` installed (comes with Windows 11, or install from Microsoft Store)

---

## 🚀 Installation Steps

### **Step 1: Open PowerShell as Administrator**

1. Press `Win + X`
2. Select **"Windows PowerShell (Admin)"** or **"Terminal (Admin)"**

### **Step 2: Install Visual Studio 2022 Build Tools**

Run this command:

```powershell
winget.exe install `
  --id Microsoft.VisualStudio.2022.BuildTools `
  --override '--passive --wait `
    --add Microsoft.VisualStudio.Workload.VCTools `
    --add Microsoft.VisualStudio.Component.VC.ATL `
    --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
    --includeRecommended'
```

**What this installs:**
- ✅ MSVC v143 (latest - v14.44+)
- ✅ C++ Build Tools core features
- ✅ Windows 11 SDK
- ✅ CMake tools
- ✅ C++ ATL libraries
- ✅ Testing tools

**Installation time:** ~5-10 minutes

### **Step 3: Verify Installation**

After installation completes, verify the MSVC version:

```powershell
# Check installed MSVC versions
dir "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
```

You should see a folder like `14.44.xxxxx` or higher.

### **Step 4: Restart Your Terminal**

Close and reopen PowerShell/Terminal to refresh environment variables.

---

## ✅ Verification

Run this to confirm the toolchain is available:

```powershell
# Find vswhere (Visual Studio locator)
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -latest -property installationPath
```

Expected output:
```
C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
```

---

## 🎯 Next: Build the UE5 Plugin

Once Build Tools are installed:

```bash
cd d:\Windsurf_AI\ue5_semantic_automation\UE5SemanticAutomation
python Build.py "C:\Program Files\Epic Games\UE_5.7" -TargetPlatforms=Win64
```

**Build time:** ~5-10 minutes

---

## 🔍 Installed Paths

After installation, tools will be located at:

| Tool | Path |
|------|------|
| **MSVC** | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC\` |
| **CMake** | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\` |
| **Ninja** | `C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\IDE\CommonExtensions\Microsoft\CMake\Ninja\` |
| **Windows SDK** | `C:\Program Files (x86)\Windows Kits\10\` |

---

## 🐛 Troubleshooting

### **Issue: winget not found**

Install from Microsoft Store:
```
https://www.microsoft.com/store/productId/9NBLGGH4NNS1
```

Or use Chocolatey:
```powershell
choco install microsoft-build-tools
```

### **Issue: Installation fails**

1. Check internet connection
2. Run PowerShell as Administrator
3. Try installing Visual Studio Installer first:
   ```powershell
   winget install Microsoft.VisualStudio.2022.BuildTools
   ```

### **Issue: Still getting MSVC version error**

1. Verify installation:
   ```powershell
   dir "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC"
   ```

2. Check for multiple VS installations:
   ```powershell
   & "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" -all
   ```

3. Uninstall old versions if needed

---

## 💡 Alternative: Visual Studio Installer GUI

If you prefer a GUI:

1. Download Visual Studio Installer:
   ```
   https://visualstudio.microsoft.com/downloads/
   ```

2. Select **"Build Tools for Visual Studio 2022"**

3. In Workloads, check:
   - ✅ **Desktop development with C++**

4. In Individual Components, ensure:
   - ✅ **MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.44-17.14)**
   - ✅ **Windows 11 SDK (10.0.22621.0)**
   - ✅ **C++ CMake tools for Windows**

5. Click **Install**

---

## 📊 Disk Space Requirements

- **Build Tools Only:** ~7 GB
- **With Recommended Components:** ~10 GB

---

## 🎉 Success Criteria

After installation, you should be able to:

1. ✅ Build the UE5 plugin without MSVC errors
2. ✅ See MSVC v14.44+ in the tools directory
3. ✅ Compile C++ projects for UE5

---

**Once installed, return to `QUICKSTART.md` to continue with plugin build!**
