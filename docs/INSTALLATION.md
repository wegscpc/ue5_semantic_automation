# Installation Guide

## Prerequisites

Before installing the UE5 Semantic Asset Organizer, ensure you have:

1. **Unreal Engine 5.x** installed
2. **Python 3.7+** (comes bundled with UE5)
3. **Git** for version control
4. **OpenAI API Key** (optional, for AI features)

## Step-by-Step Installation

### 1. Clone the Repository

Navigate to your Unreal Engine project directory and clone the repository:

```bash
cd /path/to/YourUE5Project
git clone https://github.com/yourusername/ue5_semantic_automation.git
```

Or download as ZIP and extract to your project folder.

### 2. Install Python Dependencies

The tool requires several Python packages. Install them using pip:

```bash
# Navigate to the project directory
cd ue5_semantic_automation

# Install dependencies
pip install -r requirements.txt
```

**Note**: If you're using Unreal Engine's bundled Python, you may need to use the full path:

```bash
# Windows
"C:\Program Files\Epic Games\UE_5.x\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" -m pip install -r requirements.txt

# macOS
/Users/Shared/Epic\ Games/UE_5.x/Engine/Binaries/ThirdParty/Python3/Mac/bin/python3 -m pip install -r requirements.txt

# Linux
/home/user/UnrealEngine/Engine/Binaries/ThirdParty/Python3/Linux/bin/python3 -m pip install -r requirements.txt
```

### 3. Enable Python Plugin in Unreal Engine

1. Open your Unreal Engine project
2. Go to **Edit** → **Plugins**
3. Search for "Python Editor Script Plugin"
4. Check the box to enable it
5. Restart Unreal Engine

### 4. Configure the Tool

**Option A: Environment Variable (Recommended)**

Run the setup script to securely configure your Claude API key:

```powershell
# Windows
.\setup_env.ps1
```

```bash
# Linux/macOS
./setup_env.sh
```

**Option B: Manual Configuration**

Edit `config/settings.json`:

```json
{
  "llm": {
    "provider": "anthropic",
    "model": "claude-sonnet-4-6",
    "api_key": "",
    ...
  }
}
```

Leave `api_key` empty to use the environment variable `OPENAI_API_KEY`.

**Available Claude Models:**
- `claude-sonnet-4-6` - Latest Sonnet (Recommended)
- `claude-opus-4-6` - Most powerful
- `claude-haiku-4-5-20251001` - Fastest/cheapest

See `docs/ENV_SETUP.md` for detailed API key setup instructions.

**Security Note**: Never commit your API key to version control. Consider using environment variables:

```bash
# Set environment variable
export OPENAI_API_KEY="your-api-key-here"
```

### 5. Verify Installation

Open the Unreal Engine Python console (**Window** → **Developer Tools** → **Output Log**, then select "Python"):

```python
import sys
sys.path.append('path/to/ue5_semantic_automation/src')

from main import UE5AutomationTool

# Initialize the tool
tool = UE5AutomationTool()
print("Installation successful!")
```

If no errors appear, the installation is complete!

## Optional: Set Up as Scripted Asset Action

To make the tool available from the Content Browser context menu:

1. Create a new Python script in your project's `Content/Python` folder
2. Add the following code:

```python
import unreal
import sys

# Add the tool to Python path
sys.path.append('path/to/ue5_semantic_automation/src')

from main import organize_assets, run_sanity_check, optimize_textures

# Register as scripted actions
@unreal.uclass()
class UE5AutomationActions(unreal.AssetActionUtility):
    @unreal.ufunction(meta=dict(CallInEditor="true"))
    def organize_selected(self):
        organize_assets()
    
    @unreal.ufunction(meta=dict(CallInEditor="true"))
    def run_qa_check(self):
        run_sanity_check()
    
    @unreal.ufunction(meta=dict(CallInEditor="true"))
    def optimize_selected_textures(self):
        optimize_textures()
```

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Ensure the src directory is in your Python path:
```python
import sys
sys.path.append('full/absolute/path/to/ue5_semantic_automation/src')
```

### Issue: "OpenAI API error"

**Solution**: 
1. Verify your API key is correct
2. Check your internet connection
3. Ensure you have API credits available

### Issue: "Permission denied" when installing packages

**Solution**: Run pip with administrator/sudo privileges:
```bash
# Windows (run as Administrator)
pip install -r requirements.txt

# macOS/Linux
sudo pip install -r requirements.txt
```

### Issue: Unreal Engine crashes when running scripts

**Solution**:
1. Ensure you're using compatible Unreal Engine version (5.x)
2. Check the Output Log for specific error messages
3. Try running with smaller batches of assets

## Next Steps

After installation, proceed to:
- [Usage Guide](USAGE.md) - Learn how to use the tool
- [API Reference](API.md) - Explore available functions
- [Configuration Guide](CONFIGURATION.md) - Customize behavior

## Support

If you encounter issues not covered here:
1. Check the [GitHub Issues](https://github.com/yourusername/ue5_semantic_automation/issues)
2. Review the [FAQ](FAQ.md)
3. Open a new issue with detailed error information
