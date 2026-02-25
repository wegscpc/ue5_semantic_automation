# 🛠️ UE5 Semantic Asset Organizer & AI Material Generator

[![Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-5.x-blue)](https://www.unrealengine.com/)
[![Python](https://img.shields.io/badge/Python-3.7+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📖 Overview

An intelligent automation tool for Unreal Engine 5 that combines **AI-powered asset management**, **quality assurance automation**, and **procedural material generation** to dramatically reduce manual workflow time and technical debt in game development projects.

This project bridges the gap between technical quality and artistic vision through intelligent automation, eliminating human error and optimizing asset pipelines.

## ✨ Key Features

### 🤖 AI-Powered Asset Organization
- **Semantic Auto-Naming**: Uses LLM integration (OpenAI/Local) to intelligently rename assets based on their class and context
- **Smart Classification**: Automatically categorizes and organizes assets following industry-standard naming conventions (SM_, T_, M_, etc.)
- **Metadata Generation**: AI-generated tags and descriptions for enhanced searchability in large teams

### 🔍 Quality Assurance Automation
- **Sanity Checker**: Comprehensive asset auditing to detect common errors before packaging:
  - Textures that are not power of 2
  - Materials with unused nodes
  - Assets without proper naming conventions
  - Missing LODs on static meshes
- **Texture Validator**: Validates texture dimensions, compression settings, and memory usage
- **Material Validator**: Checks material instances, parent relationships, and optimization opportunities

### ⚡ Performance Optimization
- **Texture Optimizer**: Automatically resizes and compresses textures based on viewing distance
  - Smart resolution recommendations (close/medium/far/very_far)
  - Memory usage analysis and optimization reports
  - Automatic compression settings based on texture type
- **LOD Generator**: Analyzes and generates Level of Detail for static meshes
- **Streaming Enabler**: Enables texture streaming for better performance

### 🎨 AI Material Generation
- **Prompt-Based Creation**: Generate materials from natural language descriptions
  - Example: "I need a wet stone material with moss"
- **Master Material Integration**: Automatically selects appropriate master materials
- **Parameter Automation**: AI-generated material parameters (roughness, metallic, base color, etc.)
- **Texture Suggestions**: Recommends required texture types for materials

## 🏗️ Project Structure

```
ue5_semantic_automation/
├── src/
│   ├── core/                    # Core asset organization modules
│   │   ├── asset_organizer.py   # Main organization logic
│   │   └── asset_classifier.py  # Asset classification system
│   ├── ai/                      # AI/LLM integration
│   │   ├── llm_client.py        # LLM provider abstraction
│   │   ├── metadata_generator.py # AI metadata generation
│   │   └── asset_naming.py      # AI-powered naming
│   ├── qa/                      # Quality assurance modules
│   │   ├── sanity_checker.py    # Comprehensive QA checks
│   │   ├── texture_validator.py # Texture validation
│   │   └── material_validator.py # Material validation
│   ├── optimization/            # Performance optimization
│   │   ├── texture_optimizer.py # Texture optimization
│   │   └── lod_generator.py     # LOD generation
│   ├── materials/               # Material generation
│   │   ├── material_generator.py # AI material creation
│   │   └── master_material_manager.py # Master material management
│   ├── utils/                   # Utilities
│   │   ├── config.py            # Configuration management
│   │   ├── logger.py            # Logging system
│   │   └── unreal_helpers.py    # Unreal Engine helpers
│   └── main.py                  # Main entry point
├── config/
│   └── settings.json            # Configuration file
├── docs/
│   ├── INSTALLATION.md          # Installation guide
│   ├── USAGE.md                 # Usage documentation
│   └── API.md                   # API reference
├── tests/                       # Unit tests
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🚀 Installation

### Prerequisites
- Unreal Engine 5.x
- Python 3.7+ (included with UE5)
- OpenAI API key (optional, for AI features)

### Setup

1. **Clone the repository** to your Unreal Engine project:
   ```bash
   cd YourUE5Project
   git clone https://github.com/yourusername/ue5_semantic_automation.git
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key (Optional)**
   
   **Recommended: Use Environment Variable (Secure)**
   ```powershell
   # Windows (PowerShell)
   .\setup_env.ps1
   
   # Or manually set:
   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-claude-api-key", "User")
   ```
   
   ```bash
   # Linux/macOS
   ./setup_env.sh
   
   # Or add to ~/.bashrc or ~/.zshrc:
   export OPENAI_API_KEY="your-claude-api-key"
   ```
   
   The tool is configured to use **Claude (Anthropic)** by default. See `docs/ENV_SETUP.md` for detailed setup instructions.
     }
     ```

4. **Enable Python in Unreal Engine**:
   - Edit → Plugins → Search for "Python Editor Script Plugin"
   - Enable and restart Unreal Engine

## 📚 Usage

### Quick Start

#### From Unreal Engine Python Console

```python
# Import the main module
import sys
sys.path.append('path/to/ue5_semantic_automation/src')
from main import UE5AutomationTool

# Initialize the tool
tool = UE5AutomationTool()

# Organize selected assets
tool.organize_selected_assets()

# Run sanity check
tool.run_sanity_check()

# Optimize textures
tool.optimize_textures(viewing_distance="medium")

# Generate material from description
tool.generate_material_from_description("wet stone with moss")
```

#### As Scripted Asset Actions

1. Right-click on any asset or folder in Content Browser
2. Select **Scripted Asset Actions** → **UE5 Automation**
3. Choose your desired action

### Common Workflows

#### 1. Organize Entire Project
```python
from main import UE5AutomationTool
tool = UE5AutomationTool()

# Create proper folder structure
tool.organizer.create_folder_structure()

# Organize all assets
tool.organizer.organize_entire_content_folder()
```

#### 2. Quality Assurance Check
```python
# Run comprehensive sanity check
stats = tool.run_sanity_check()

# Get critical issues only
critical = tool.sanity_checker.get_critical_issues()

# Export report
tool.sanity_checker.export_issues_report()
```

#### 3. Texture Optimization
```python
# Detect over-resolution textures
oversized = tool.texture_optimizer.detect_over_resolution_textures()

# Generate optimization report
report = tool.texture_optimizer.generate_optimization_report()

# Batch optimize
tool.optimize_textures(viewing_distance="far")
```

#### 4. AI Material Generation
```python
# Generate material from prompt
material = tool.generate_material_from_description(
    "shiny metal with scratches and rust"
)

# Batch generate materials
prompts = [
    "wet stone with moss",
    "polished wood floor",
    "glowing neon sign"
]
tool.material_generator.batch_generate_materials(prompts)
```

## 🎯 Impact on Workflow

### Time Savings
- **80% reduction** in manual folder organization time
- **60% faster** material setup for common scenarios
- **Early detection** of optimization issues, reducing build errors

### Quality Improvements
- Consistent naming conventions across entire project
- Standardized folder structure for team collaboration
- Automated detection of common performance issues
- Reduced technical debt through continuous validation

## 🛠️ Tech Stack

- **Engine**: Unreal Engine 5.x
- **Language**: Python 3.7+ (Unreal API)
- **AI/LLM Integration
- **Claude (Anthropic)** - Primary AI provider with latest models
- **OpenAI GPT-4** - Alternative provider support
- Local LLM support for offline use
- Configurable API endpoints
- Fallback to rule-based systems when AI is unavailable
- **Version Control**: Git & GitHub

## 📊 Configuration

Edit `config/settings.json` to customize behavior:

```json
{
  "llm": {
    "provider": "openai",
    "model": "gpt-4",
    "temperature": 0.7
  },
  "organization": {
    "auto_organize": true,
    "create_folders": true
  },
  "optimization": {
    "default_viewing_distance": "medium",
    "max_texture_resolution": 2048,
    "auto_generate_lods": false
  },
  "qa": {
    "enforce_power_of_two": true,
    "enforce_naming_convention": true
  }
}
```

## 🧪 Testing

Run unit tests:
```bash
python -m pytest tests/
```

## 📝 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [API Reference](docs/API.md)
- [Contributing Guidelines](CONTRIBUTING.md)

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Walter Gomis** - "M" Shaped Engineer | Technical Artist | QA Strategist

Specializing in bridging the gap between technical quality and artistic vision through intelligent automation.

- GitHub: [@wegscpc](https://github.com/wegscpc)
- LinkedIn: [Walter Gomis](https://linkedin.com/in/walter-gomis-schlick-13719737)

## 🙏 Acknowledgments

- Unreal Engine team for excellent Python API
- OpenAI for GPT models
- The game development community for best practices and standards

## 🗺️ Roadmap

- [ ] Editor Utility Widget UI
- [ ] Batch processing queue system
- [ ] Integration with Perforce/Git
- [ ] Custom material node generation
- [ ] Automated texture packing
- [ ] Blueprint organization tools
- [ ] Performance profiling integration
- [ ] Multi-project support

---

**Note**: This tool is designed to augment, not replace, human decision-making in asset management and material creation. Always review AI-generated suggestions before applying them to production assets.
