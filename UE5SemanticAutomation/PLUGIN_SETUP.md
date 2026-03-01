# 🔌 UE5 Semantic Automation Plugin - Setup Guide

## 📋 Overview

This plugin provides a hybrid architecture combining:
- **C++ Plugin** - Native UE5 editor integration
- **Python Backend** - AI automation logic (your existing `src/` code)
- **TCP Bridge** - Communication layer between C++ and Python

Based on the architecture patterns from `unreal-mcp` and `Convai-UnrealEngine-SDK`.

---

## 🏗️ Architecture

```
UE5 Editor (C++)
    ↕ TCP Socket (Port 55557)
Python Bridge Server
    ↕ Python Imports
Your Automation Modules (src/)
```

---

## 🚀 Quick Start

### **Prerequisites**

1. **Unreal Engine 5.x** installed
2. **Python 3.7+** (included with UE5)
3. **Visual Studio 2019/2022** (for Windows C++ compilation)
4. **Your existing automation code** in `../src/`

### **Step 1: Build the Plugin**

```bash
# Windows
python Build.py "C:\Program Files\Epic Games\UE_5.3" -TargetPlatforms=Win64

# Mac
python Build.py "/Users/Shared/Epic Games/UE_5.3"

# Linux
python Build.py "~/UnrealEngine/UE_5.3"
```

This will:
- Compile the C++ plugin
- Package for your platform
- Copy Python files
- Create output in `Output/` directory

### **Step 2: Install the Plugin**

**Option A: Engine-wide Installation** (Recommended)

Copy `Output/UE5SemanticAutomation/` to:
```
Windows: C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace\
Mac:     /Users/Shared/Epic Games/UE_5.x/Engine/Plugins/Marketplace/
Linux:   ~/UnrealEngine/UE_5.x/Engine/Plugins/Marketplace/
```

**Option B: Project-specific Installation**

Copy `Output/UE5SemanticAutomation/` to:
```
YourProject/Plugins/UE5SemanticAutomation/
```

### **Step 3: Start Python Bridge Server**

```bash
cd Output/UE5SemanticAutomation/Python
python bridge_server.py
```

You should see:
```
Bridge server listening on 127.0.0.1:55557
```

**Keep this running** while using the plugin in UE5.

### **Step 4: Enable Plugin in UE5**

1. Open Unreal Engine
2. Go to **Edit → Plugins**
3. Search for "**UE5 Semantic Automation**"
4. Check the **Enabled** box
5. Click **Restart Now**

### **Step 5: Verify Installation**

After restart, you should see:
- **Toolbar Button**: "Semantic Automation" in the Level Editor toolbar
- **Menu Item**: Window → UE5 Semantic Automation
- **Output Log**: "Python Bridge initialized on port 55557"

---

## 🎨 Creating Editor Utility Widgets

### **Step 1: Create Widget Blueprint**

1. In Content Browser, navigate to `Plugins/UE5SemanticAutomation Content/UI/`
2. Right-click → **Editor Utilities → Editor Utility Widget**
3. Name it `WBP_AssetOrganizer`

### **Step 2: Design the UI**

Add widgets:
- **Buttons** for actions (Organize, Generate Material, etc.)
- **Text Boxes** for input (asset names, descriptions)
- **Lists** for displaying results
- **Progress Bars** for long operations

### **Step 3: Add Blueprint Logic**

In the Event Graph:

```blueprint
Event Construct
  ↓
Call Python Bridge → SendCommand
  Command: "organize_assets"
  Params: {"asset_path": "/Game/"}
  ↓
Parse Response
  ↓
Update UI
```

### **Step 4: Register Widget**

In `UE5SemanticAutomationModule.cpp`, add:

```cpp
void FUE5SemanticAutomationModule::PluginButtonClicked()
{
    // Load and open the Editor Utility Widget
    FString WidgetPath = TEXT("/UE5SemanticAutomation/UI/WBP_AssetOrganizer");
    UEditorUtilityWidgetBlueprint* Widget = LoadObject<UEditorUtilityWidgetBlueprint>(nullptr, *WidgetPath);
    
    if (Widget)
    {
        UEditorUtilitySubsystem* EditorUtilitySubsystem = GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>();
        EditorUtilitySubsystem->SpawnAndRegisterTab(Widget);
    }
}
```

---

## 🔧 Development Workflow

### **Iterating on C++ Code**

1. Make changes to `.h` or `.cpp` files
2. Rebuild: `python Build.py [UE_PATH]`
3. Copy to plugins directory
4. Restart UE5

### **Iterating on Python Code**

1. Make changes to `bridge_server.py` or `src/` modules
2. Restart `bridge_server.py`
3. No UE5 restart needed! ✨

### **Iterating on Widgets**

1. Edit widget in UE5 Editor
2. Save
3. Changes take effect immediately

---

## 📡 Python Bridge API

### **Sending Commands from C++**

```cpp
UPythonBridge* Bridge = NewObject<UPythonBridge>();
FString Response = Bridge->SendCommand(
    TEXT("organize_assets"),
    TEXT("{\"asset_path\": \"/Game/\"}")
);
```

### **Sending Commands from Blueprints**

```blueprint
Get Python Bridge
  ↓
Send Command
  Command: "suggest_name"
  Params: {"original_name": "cube_01", "asset_type": "StaticMesh"}
  ↓
Print Response
```

### **Available Commands**

| Command | Parameters | Returns |
|---------|-----------|---------|
| `ping` | - | Health check |
| `organize_assets` | `asset_path` | Organization result |
| `suggest_name` | `original_name`, `asset_type` | Suggested name |
| `generate_material` | `description` | Material parameters |
| `generate_metadata` | `asset_name`, `asset_type` | Tags, description |
| `run_sanity_check` | `root_path` | Issues found |
| `optimize_textures` | `viewing_distance` | Optimization stats |
| `generate_lods` | `mesh_path` | LOD generation result |

---

## 🐛 Troubleshooting

### **Plugin doesn't appear in UE5**

- Check plugin is in correct directory
- Verify `.uplugin` file exists
- Check UE5 version compatibility
- Look for errors in Output Log

### **Python Bridge won't connect**

- Ensure `bridge_server.py` is running
- Check port 55557 is not in use
- Verify firewall settings
- Check UE5 Output Log for connection errors

### **Build fails**

- Verify UE5 path is correct
- Check Visual Studio is installed (Windows)
- Ensure you have write permissions
- Check UE5 version matches plugin target

### **Commands fail**

- Check `bridge_server.py` console for errors
- Verify Python modules are importable
- Check command parameters are correct
- Look for exceptions in Python console

---

## 📚 Next Steps

1. **Create your first Editor Utility Widget**
   - Start with a simple asset organizer UI
   - Add buttons that call Python commands
   - Display results in the widget

2. **Extend the Python Bridge**
   - Add new commands to `bridge_server.py`
   - Implement actual logic using your `src/` modules
   - Return structured JSON responses

3. **Add Scripted Asset Actions**
   - Right-click context menu integration
   - Batch operations on selected assets
   - Custom asset validators

4. **Build Advanced Features**
   - Real-time material preview
   - Interactive QA dashboard
   - LLM evaluation results viewer

---

## 🎯 Architecture Benefits

✅ **Separation of Concerns**
- C++ handles UE5 integration
- Python handles AI/automation logic
- Clean interface between layers

✅ **Rapid Iteration**
- Python changes don't require UE5 restart
- Widget changes are immediate
- C++ only needs rebuild when changing plugin core

✅ **Reusability**
- All your existing Python code works as-is
- Can use automation from command line OR UE5
- Bridge server can be used by other tools

✅ **Scalability**
- Easy to add new commands
- Can run Python on separate machine
- Supports async operations

---

## 📖 References

- **unreal-mcp**: TCP bridge architecture pattern
- **Convai-UnrealEngine-SDK**: Plugin build system
- **UE5 Python API**: https://docs.unrealengine.com/5.0/en-US/PythonAPI/
- **Editor Utility Widgets**: https://docs.unrealengine.com/5.0/en-US/editor-utility-widgets/

---

**Happy Automating! 🚀**
