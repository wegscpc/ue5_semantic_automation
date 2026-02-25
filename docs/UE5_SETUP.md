# Unreal Engine 5 Setup Guide

This guide walks you through setting up the UE5 Semantic Asset Organizer & AI Material Generator in your Unreal Engine 5 project.

## Prerequisites

- Unreal Engine 5.0 or later
- Python 3.8+ installed on your system
- Claude API key (optional, for AI features)

## Step 1: Enable Python in Unreal Engine

1. **Open your UE5 project**

2. **Enable the Python Editor Script Plugin**:
   - Go to **Edit** → **Plugins**
   - Search for "Python Editor Script Plugin"
   - Check the box to enable it
   - Click **Restart Now**

3. **Verify Python is enabled**:
   - After restart, go to **Window** → **Developer Tools** → **Output Log**
   - In the dropdown, you should see "Python" as an option

## Step 2: Install the Tool

1. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/UE5Project
   ```

2. **Clone or copy the tool**:
   ```bash
   git clone https://github.com/yourusername/ue5_semantic_automation.git
   ```

3. **Install Python dependencies**:
   ```bash
   cd ue5_semantic_automation
   pip install -r requirements.txt
   ```

## Step 3: Configure API Key (Optional)

For AI-powered features, configure your Claude API key:

**Windows (PowerShell)**:
```powershell
.\setup_env.ps1
```

**Linux/macOS**:
```bash
./setup_env.sh
```

Or manually set the environment variable:
```powershell
# Windows
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-api-key", "User")
```

```bash
# Linux/macOS
export OPENAI_API_KEY="your-api-key"
echo 'export OPENAI_API_KEY="your-api-key"' >> ~/.bashrc
```

**Important**: Restart Unreal Engine after setting the environment variable!

## Step 4: Test the Installation

1. **Open the Python console** in Unreal Engine:
   - **Window** → **Developer Tools** → **Output Log**
   - Select "Python" from the dropdown

2. **Run a test command**:
   ```python
   import sys
   sys.path.append('D:/path/to/ue5_semantic_automation/src')  # Adjust path
   
   from utils.config import Config
   config = Config()
   print("✓ Tool loaded successfully!")
   print(f"Provider: {config.get('llm.provider')}")
   print(f"Model: {config.get('llm.model')}")
   ```

## Step 5: Basic Usage

### Organize Selected Assets

```python
import sys
sys.path.append('D:/path/to/ue5_semantic_automation/src')

from core.asset_organizer import AssetOrganizer
import unreal

# Get selected assets
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

# Initialize organizer
organizer = AssetOrganizer()

# Organize assets
for asset in selected_assets:
    organizer.organize_asset(asset)

print(f"✓ Organized {len(selected_assets)} assets")
```

### Run QA Checks

```python
import sys
sys.path.append('D:/path/to/ue5_semantic_automation/src')

from qa.sanity_checker import SanityChecker
import unreal

# Get selected assets
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

# Run sanity checks
checker = SanityChecker()
issues = checker.run_all_checks(selected_assets)

# Print results
for issue in issues:
    print(f"{issue['severity']}: {issue['message']}")
```

### AI Asset Naming

```python
import sys
sys.path.append('D:/path/to/ue5_semantic_automation/src')

from ai.asset_naming import AIAssetNaming
import unreal

# Get selected assets
selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()

# Initialize AI naming
naming = AIAssetNaming()

# Suggest names
for asset in selected_assets:
    suggestion = naming.suggest_name(asset)
    print(f"Asset: {asset.get_name()}")
    print(f"Suggested: {suggestion}")
```

## Step 6: Create Editor Utility Widget (Optional)

For a GUI interface:

1. **Create a new Editor Utility Widget**:
   - Right-click in Content Browser
   - **Editor Utilities** → **Editor Utility Widget**
   - Name it "UE5_AutomationTool_UI"

2. **Add buttons for common operations**:
   - Organize Selected Assets
   - Run QA Checks
   - Generate AI Names
   - Optimize Textures

3. **Bind Python scripts to buttons**:
   ```python
   # In the button's OnClicked event
   import sys
   sys.path.append('D:/path/to/ue5_semantic_automation/src')
   from main import UE5AutomationTool
   
   tool = UE5AutomationTool()
   tool.organize_selected_assets()
   ```

## Troubleshooting

### Python Module Not Found

**Issue**: `ModuleNotFoundError: No module named 'anthropic'`

**Solution**: 
```bash
pip install -r requirements.txt
```

### API Key Not Found

**Issue**: `WARNING: anthropic API key not found`

**Solution**:
1. Set the environment variable (see Step 3)
2. Restart Unreal Engine
3. Verify: `echo $env:OPENAI_API_KEY` (Windows) or `echo $OPENAI_API_KEY` (Linux/macOS)

### Relative Import Errors

**Issue**: `ImportError: attempted relative import beyond top-level package`

**Solution**: Make sure you're adding the `src` directory to `sys.path`:
```python
import sys
sys.path.append('D:/full/path/to/ue5_semantic_automation/src')
```

### Unreal Module Not Found (Outside UE5)

**Issue**: Running tests outside UE5 fails with `ModuleNotFoundError: No module named 'unreal'`

**Solution**: This is expected. The `unreal` module is only available inside Unreal Engine's Python environment. Use the standalone test scripts for testing outside UE5.

## Performance Tips

1. **Batch Operations**: Process multiple assets at once for better performance
2. **Use Async**: For AI operations, consider using async/await patterns
3. **Cache Results**: The tool caches AI responses to avoid redundant API calls
4. **Limit Scope**: Start with a small subset of assets to test workflows

## Next Steps

- Review `docs/USAGE.md` for detailed feature documentation
- Check `examples/basic_usage.py` for more code examples
- Customize `config/settings.json` for your project needs
- Create custom workflows for your team

## Support

For issues or questions:
- GitHub Issues: [Your Repository URL]
- Documentation: `docs/` folder
- Examples: `examples/` folder
