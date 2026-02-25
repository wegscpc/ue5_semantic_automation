# Quick Start Guide

Get up and running with UE5 Semantic Asset Organizer in 5 minutes!

## Installation

```bash
# 1. Clone the repository
cd YourUE5Project
git clone https://github.com/yourusername/ue5_semantic_automation.git

# 2. Install dependencies
pip install -r ue5_semantic_automation/requirements.txt

# 3. Configure (optional - for AI features)
# Edit config/settings.json and add your OpenAI API key
```

## Enable in Unreal Engine

1. Open Unreal Engine 5
2. **Edit** → **Plugins** → Search "Python"
3. Enable **Python Editor Script Plugin**
4. Restart Unreal Engine

## First Use

Open the **Output Log** (Window → Developer Tools → Output Log), select **Python**, and run:

```python
import sys
sys.path.append('d:/Windsurf_AI/ue5_semantic_automation/src')  # Adjust path

from main import UE5AutomationTool

# Initialize
tool = UE5AutomationTool()

# Organize selected assets
tool.organize_selected_assets()
```

## Common Tasks

### Organize Assets
```python
# Select assets in Content Browser, then:
tool.organize_selected_assets()
```

### Quality Check
```python
# Check entire project for issues
tool.run_sanity_check()
```

### Optimize Textures
```python
# Optimize for performance
tool.optimize_textures(viewing_distance="medium")
```

### Generate Material
```python
# Create material from description
tool.generate_material_from_description("wet stone with moss")
```

## Next Steps

- Read [USAGE.md](docs/USAGE.md) for detailed examples
- Check [INSTALLATION.md](docs/INSTALLATION.md) for advanced setup
- Explore [examples/](examples/) for more use cases

## Need Help?

- Check the [FAQ](docs/FAQ.md)
- Open an [issue](https://github.com/yourusername/ue5_semantic_automation/issues)
- Read the full [README.md](README.md)
