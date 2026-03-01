# Environment Variable Setup Guide

This guide explains how to configure API keys using environment variables for secure credential management.

## Why Use Environment Variables?

- **Security**: API keys are not stored in code or config files
- **Version Control**: No risk of accidentally committing secrets
- **Flexibility**: Easy to change without modifying code
- **Best Practice**: Industry-standard approach for credential management

## Setup Methods

### Method 1: Automated Setup (Recommended)

#### Windows (PowerShell)
```powershell
cd <project_root>
.\setup_env.ps1
```

#### macOS/Linux (Bash)
```bash
cd /path/to/ue5_semantic_automation
chmod +x setup_env.sh
./setup_env.sh
```

### Method 2: Manual Setup

#### Windows

**Option A: User Environment Variable (Persistent)**
1. Press `Win + X` → System
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `OPENAI_API_KEY`
6. Variable value: Your API key
7. Click OK

**Option B: PowerShell (Current Session)**
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

**Option C: PowerShell (Persistent)**
```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-api-key-here", "User")
```

#### macOS/Linux

**Option A: Bash/Zsh (Persistent)**

Add to `~/.bashrc` or `~/.zshrc`:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Then reload:
```bash
source ~/.bashrc  # or ~/.zshrc
```

**Option B: Current Session Only**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Verification

### Check if Variable is Set

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY
```

**macOS/Linux:**
```bash
echo $OPENAI_API_KEY
```

### Test in Python

```python
import os

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"✓ API key found: {api_key[:10]}...")
else:
    print("✗ API key not found")
```

### Test with UE5 Automation Tool

```python
import sys
# Replace with your actual project path
sys.path.append('/path/to/your/ue5_semantic_automation/src')

from utils.config import Config

config = Config()
api_key = config.get("llm.api_key")

if api_key:
    print(f"✓ API key configured: {api_key[:10]}...")
else:
    print("✗ API key not configured")
```

## Using Windsurf/Cascade API

If you're using Windsurf/Cascade instead of OpenAI:

1. Set the environment variable as shown above
2. The tool will automatically use it
3. No code changes needed!

The `LLMClient` class automatically reads from `OPENAI_API_KEY` environment variable if not specified in config.

## Alternative: Using .env File (Development Only)

For development, you can use a `.env` file:

1. Create `.env` in project root:
```bash
OPENAI_API_KEY=your-api-key-here
```

2. Add to `.gitignore`:
```
.env
```

3. Load in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

**Note**: Install python-dotenv: `pip install python-dotenv`

## Troubleshooting

### Variable Not Found After Setting

**Windows:**
- Restart PowerShell/Command Prompt
- Restart Unreal Engine
- Log out and log back in (for system-wide changes)

**macOS/Linux:**
- Run `source ~/.bashrc` (or `~/.zshrc`)
- Restart terminal
- Restart any running applications

### API Key Not Working

1. Verify the key is correct
2. Check for extra spaces or quotes
3. Ensure you have API credits/access
4. Test with a simple API call

### Permission Denied (Linux/macOS)

```bash
chmod +x setup_env.sh
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use different keys** for development/production
3. **Rotate keys regularly**
4. **Limit key permissions** to only what's needed
5. **Monitor API usage** for unexpected activity

## Multiple API Keys

If you need different keys for different purposes:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic (Claude)
export ANTHROPIC_API_KEY="sk-ant-..."

# Local LLM
export LLM_BASE_URL="http://localhost:8000"
```

Update `config/settings.json` to specify which to use:
```json
{
  "llm": {
    "provider": "openai",
    "api_key": ""  // Leave empty to use environment variable
  }
}
```

## Next Steps

After setting up the environment variable:

1. Restart your terminal/IDE/Unreal Engine
2. Verify the variable is set
3. Test the AI features:
   ```python
   from main import UE5AutomationTool
   tool = UE5AutomationTool()
   tool.generate_material_from_description("test material")
   ```

## Support

If you encounter issues:
- Check [INSTALLATION.md](INSTALLATION.md)
- Review [Troubleshooting](#troubleshooting) section
- Open an issue on GitHub
