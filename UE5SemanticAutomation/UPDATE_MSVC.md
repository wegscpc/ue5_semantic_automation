# 🔧 Update MSVC Toolchain to v14.44+

## Current Situation

- **VS Installation:** Visual Studio Community 2022 (v17.10)
- **Current MSVC:** v14.40.33807 ❌ (incompatible with UE 5.7)
- **Required MSVC:** v14.44+ ✅

---

## ✅ Solution: Update via Visual Studio Installer

### **Method 1: GUI (Recommended)**

1. **Open Visual Studio Installer**
   - Press `Win + S`
   - Search: "Visual Studio Installer"
   - Open it

2. **Modify Visual Studio 2022 Community**
   - Click **"Modify"** button next to VS 2022 Community

3. **Update Individual Components**
   - Click **"Individual components"** tab
   - Search: "MSVC v143"
   - Check the **latest version** (should be v14.44 or higher):
     - ✅ **MSVC v143 - VS 2022 C++ x64/x86 build tools (Latest)**
     - Or specifically: **MSVC v143 - VS 2022 C++ x64/x86 build tools (v14.44-17.14)**

4. **Install**
   - Click **"Modify"** button at bottom right
   - Wait for installation (~5-10 minutes)

5. **Verify**
   ```powershell
   dir "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC"
   ```
   - Should show folder: `14.44.xxxxx` or higher

---

### **Method 2: Command Line**

Run PowerShell as Administrator:

```powershell
# Update to latest MSVC toolchain
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vs_installer.exe" modify `
  --installPath "C:\Program Files\Microsoft Visual Studio\2022\Community" `
  --add Microsoft.VisualStudio.Component.VC.14.44.17.14.x86.x64 `
  --passive --norestart

# Wait for completion, then verify
Start-Sleep -Seconds 60
dir "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC"
```

---

### **Method 3: Update Visual Studio Completely**

Sometimes the easiest approach is to update VS to the latest version:

1. **Open Visual Studio Installer**
2. Click **"Update"** button (if available)
3. Let it update to the latest version (17.14+)
4. This will automatically include MSVC v14.44+

---

## 🔍 Verification Commands

After installation, run these to verify:

```powershell
# Check MSVC versions installed
dir "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC"

# Check VS version
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" `
  -all -products * -property installationVersion

# Check if correct component is installed
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe" `
  -all -requires Microsoft.VisualStudio.Component.VC.14.44.17.14.x86.x64
```

**Expected output:**
```
Directory: C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         [date]                             14.40.33807
d-----         [date]                             14.44.xxxxx  ← This should appear
```

---

## 🎯 After MSVC Update

Once you see `14.44.xxxxx` folder, proceed with plugin build:

```bash
cd d:\Windsurf_AI\ue5_semantic_automation\UE5SemanticAutomation
python Build.py "C:\Program Files\Epic Games\UE_5.7" -TargetPlatforms=Win64
```

---

## 🐛 Troubleshooting

### **Issue: Update button not available**

Update VS manually:
```powershell
# Download latest VS installer
winget upgrade Microsoft.VisualStudio.2022.Community
```

### **Issue: Component not found**

The component ID might be different. List all available MSVC components:

```powershell
& "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vs_installer.exe" export `
  --installPath "C:\Program Files\Microsoft Visual Studio\2022\Community" `
  --config vs_config.json

# Open vs_config.json to see installed components
```

### **Issue: Multiple MSVC versions**

UE5 will automatically use the latest version. Having multiple versions is fine.

---

## 💡 Why This Happened

The `winget` command installed Build Tools components to your **existing** VS Community installation rather than creating a separate BuildTools installation. This is normal behavior when VS Community is already installed.

---

## ⏱️ Timeline

- **GUI Method:** ~10 minutes (including download)
- **Command Line:** ~10 minutes (background installation)
- **Full VS Update:** ~15-20 minutes

---

**Once MSVC v14.44+ is installed, you're ready to build the UE5 plugin!**
