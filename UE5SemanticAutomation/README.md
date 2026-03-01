# 🔌 UE5 Semantic Automation Plugin

**AI-powered asset organization, quality assurance, and material generation for Unreal Engine 5**

---

## 📦 What's Included

This plugin provides a complete Editor UI for the UE5 Semantic Automation toolkit with:

- ✅ **C++ Editor Plugin** - Native UE5 integration
- ✅ **Python Bridge Server** - TCP communication layer
- ✅ **Editor Utility Widgets** - Visual UI for all features
- ✅ **Scripted Asset Actions** - Right-click context menu integration
- ✅ **Toolbar Integration** - Quick access from Level Editor

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│     Unreal Engine 5 Editor          │
│  ┌──────────────────────────────┐   │
│  │  Editor Utility Widgets      │   │
│  │  (Blueprint UI)              │   │
│  └────────────┬─────────────────┘   │
│               │                     │
│  ┌────────────▼─────────────────┐   │
│  │  C++ Plugin Module           │   │
│  │  - Python Bridge (TCP)       │   │
│  │  - Asset Actions             │   │
│  │  - Editor Commands           │   │
│  └────────────┬─────────────────┘   │
└───────────────┼─────────────────────┘
                │ TCP Socket
                │ Port 55557
┌───────────────▼─────────────────────┐
│   Python Bridge Server              │
│   - Command Router                  │
│   - Module Loader                   │
│   - Response Handler                │
└───────────────┬─────────────────────┘
                │ Python Imports
┌───────────────▼─────────────────────┐
│   Automation Modules (../src/)      │
│   - Asset Organizer                 │
│   - AI Naming                       │
│   - Material Generator              │
│   - QA Checker                      │
│   - Texture Optimizer               │
│   - LOD Generator                   │
│   - Metadata Generator              │
│   - LLM Evaluator                   │
└─────────────────────────────────────┘
```

---

## 🚀 Quick Start

### **1. Build the Plugin**

```bash
python Build.py "C:\Program Files\Epic Games\UE_5.3" -TargetPlatforms=Win64
```

### **2. Install**

Copy `Output/UE5SemanticAutomation/` to:
```
C:\Program Files\Epic Games\UE_5.x\Engine\Plugins\Marketplace\
```

### **3. Start Python Bridge**

```bash
cd Output/UE5SemanticAutomation/Python
python bridge_server.py
```

### **4. Enable in UE5**

1. Edit → Plugins
2. Search "UE5 Semantic Automation"
3. Enable and restart

---

## 📁 Directory Structure

```
UE5SemanticAutomation/
├── UE5SemanticAutomation.uplugin    # Plugin descriptor
├── Resources/
│   └── Icon128.png                  # Plugin icon
├── Source/
│   └── UE5SemanticAutomation/
│       ├── Public/
│       │   ├── UE5SemanticAutomationModule.h
│       │   └── PythonBridge.h       # TCP bridge header
│       ├── Private/
│       │   ├── UE5SemanticAutomationModule.cpp
│       │   └── PythonBridge.cpp     # TCP bridge implementation
│       └── UE5SemanticAutomation.Build.cs
├── Content/
│   └── UI/                          # Editor Utility Widgets (create in UE5)
│       ├── WBP_MainToolbar.uasset
│       ├── WBP_AssetOrganizer.uasset
│       ├── WBP_MaterialGenerator.uasset
│       └── WBP_QAChecker.uasset
├── Python/
│   ├── bridge_server.py             # TCP server
│   └── requirements.txt
├── Config/
│   └── FilterPlugin.ini
├── Build.py                         # Build automation script
├── PLUGIN_SETUP.md                  # Detailed setup guide
└── README.md                        # This file
```

---

## 🎨 Features

### **Editor Utility Widgets** (To be created in UE5)

1. **Main Toolbar** - Central hub for all automation tools
2. **Asset Organizer** - Drag-drop organization with AI naming
3. **Material Generator** - Prompt-based material creation
4. **QA Dashboard** - Visual issue reporting and fixing
5. **Texture Optimizer** - Batch texture optimization
6. **LOD Generator** - Automatic LOD creation
7. **Evaluation Dashboard** - LLM evaluation results viewer

### **Python Bridge Commands**

| Command | Description |
|---------|-------------|
| `ping` | Health check |
| `organize_assets` | Organize assets by type |
| `suggest_name` | AI-powered naming suggestions |
| `generate_material` | Generate material from description |
| `generate_metadata` | Create tags and descriptions |
| `run_sanity_check` | QA validation |
| `optimize_textures` | Texture optimization |
| `generate_lods` | LOD generation |

---

## 🔧 Development

### **Adding New Commands**

1. **Add handler to `bridge_server.py`**:
```python
def handle_my_command(self, params: Dict[str, Any]) -> Dict[str, Any]:
    # Your logic here
    return {'result': 'success'}

# Register in __init__
self.commands['my_command'] = self.handle_my_command
```

2. **Call from C++/Blueprint**:
```cpp
Bridge->SendCommand("my_command", "{\"param\": \"value\"}");
```

### **Creating Editor Widgets**

1. Create Editor Utility Widget in UE5
2. Add UI elements (buttons, text boxes, lists)
3. Call Python Bridge in Blueprint Event Graph
4. Parse JSON responses and update UI

### **Rebuilding**

```bash
# After C++ changes
python Build.py [UE_PATH]

# After Python changes
# Just restart bridge_server.py - no rebuild needed!
```

---

## 📖 Documentation

- **[PLUGIN_SETUP.md](PLUGIN_SETUP.md)** - Detailed setup and development guide
- **[Main Project README](../README.md)** - Full project documentation
- **[Evaluation Guide](../docs/EVALUATION_GUIDE.md)** - LLM evaluation framework

---

## 🎯 Roadmap

### **Phase 1: Core Plugin** ✅
- [x] C++ plugin structure
- [x] Python bridge server
- [x] TCP communication
- [x] Build system

### **Phase 2: UI Development** 🚧
- [ ] Main toolbar widget
- [ ] Asset organizer widget
- [ ] Material generator widget
- [ ] QA dashboard widget

### **Phase 3: Integration** 📋
- [ ] Scripted asset actions
- [ ] Context menu integration
- [ ] Batch operations
- [ ] Progress indicators

### **Phase 4: Advanced Features** 📋
- [ ] Real-time material preview
- [ ] Interactive evaluation dashboard
- [ ] Async operation support
- [ ] Multi-user collaboration

---

## 🤝 Contributing

This plugin is part of the **UE5 Semantic Automation** project.

See main repository: https://github.com/wegscpc/ue5_semantic_automation

---

## 📄 License

MIT License - See main project LICENSE file

---

## 👤 Author

**Walter Gomis** - Technical Artist | QA Strategist

- GitHub: [@wegscpc](https://github.com/wegscpc)
- LinkedIn: [Walter Gomis](https://linkedin.com/in/walter-gomis-schlick-13719737)

---

**Built with ❤️ for the Unreal Engine community**
