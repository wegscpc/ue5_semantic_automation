# ⚡ UE5 Semantic Automation Plugin - Quick Start

Get up and running in 5 minutes!

---

## 📋 Prerequisites

- ✅ Unreal Engine 5.x installed
- ✅ Python 3.7+ (included with UE5)
- ✅ Visual Studio 2019/2022 (Windows only)

---

## 🚀 Installation

### **Step 1: Build the Plugin**

```bash
# Navigate to plugin directory
cd <project_root>/UE5SemanticAutomation

# Build (Windows)
python Build.py "C:\Program Files\Epic Games\UE_5.3" -TargetPlatforms=Win64

# Build (Mac)
python Build.py "/Users/Shared/Epic Games/UE_5.3"
```

**Build time:** ~5-10 minutes

### **Step 2: Install to UE5**

Copy the built plugin:

**From:** `Output/UE5SemanticAutomation/`

**To:** `C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace\`

### **Step 3: Start Python Bridge**

```bash
cd Output/UE5SemanticAutomation/Python
python bridge_server.py
```

**Keep this terminal open!** You should see:
```
Bridge server listening on 127.0.0.1:55557
```

### **Step 4: Enable in UE5**

1. Launch Unreal Engine
2. **Edit → Plugins**
3. Search: "**UE5 Semantic Automation**"
4. ✅ Check **Enabled**
5. Click **Restart Now**

---

## ✅ Verification

After restart, check for:

1. **Toolbar Button** - "Semantic Automation" in Level Editor toolbar
2. **Menu Item** - Window → UE5 Semantic Automation
3. **Output Log** - "Python Bridge initialized on port 55557"

---

## 🎨 First Use

### **Test the Connection**

1. Open **Output Log** (Window → Developer Tools → Output Log)
2. Click the **Semantic Automation** toolbar button
3. Check for: "UE5 Semantic Automation button clicked"
4. Check Python terminal for: "Client connected from..."

### **Create Your First Widget**

1. In Content Browser: **Plugins → UE5SemanticAutomation Content**
2. Create folder: **UI**
3. Right-click → **Editor Utilities → Editor Utility Widget**
4. Name: `WBP_TestWidget`
5. Open it and add a **Button**
6. In Event Graph:

```
Event Construct
  ↓
Get Python Bridge
  ↓
Send Command
  Command: "ping"
  Params: "{}"
  ↓
Print String (Response)
```

7. Save and run the widget
8. You should see: `{"success": true, "result": {"status": "ok", "message": "Bridge server is running"}}`

---

## 🎯 Next Steps

### **Option A: Use Existing Features**

The Python bridge is ready to use with these commands:
- `organize_assets` - Organize project assets
- `suggest_name` - AI naming suggestions
- `generate_material` - Create materials from descriptions
- `run_sanity_check` - QA validation

### **Option B: Create Custom UI**

Build Editor Utility Widgets for:
- Asset organization dashboard
- Material generator interface
- QA issue viewer
- Texture optimization panel

### **Option C: Extend Functionality**

Add new commands to `bridge_server.py`:
1. Add handler function
2. Register in `self.commands`
3. Restart bridge server
4. Call from UE5

---

## 🐛 Troubleshooting

### **Plugin doesn't appear**
- Check plugin is in correct directory
- Verify UE5 version matches build target
- Look for errors in Output Log

### **Bridge won't connect**
- Ensure `bridge_server.py` is running
- Check port 55557 is available
- Verify firewall settings

### **Build fails**
- Check UE5 path is correct
- Ensure Visual Studio is installed (Windows)
- Verify write permissions to Output directory

---

## 📚 Documentation

- **[PLUGIN_SETUP.md](PLUGIN_SETUP.md)** - Detailed setup guide
- **[README.md](README.md)** - Plugin overview
- **[Main Project](../README.md)** - Full documentation

---

## 🎉 You're Ready!

The plugin is installed and the Python bridge is running. Start building your automation workflows!

**Need help?** See [PLUGIN_SETUP.md](PLUGIN_SETUP.md) for detailed guides.
