# UE5 Semantic Automation - Setup Checklist

Use this checklist to ensure your installation is complete and working.

## ✅ Installation Checklist

### 1. System Requirements
- [ ] Unreal Engine 5.0+ installed
- [ ] Python 3.8+ installed
- [ ] Git installed (optional)

### 2. Python Dependencies
- [ ] Run `pip install -r requirements.txt`
- [ ] Verify anthropic installed: `pip show anthropic`
- [ ] Verify openai installed: `pip show openai`

### 3. API Configuration
- [ ] Get Claude API key from https://console.anthropic.com
- [ ] Add credits to Claude account (required for AI features)
- [ ] Run `setup_env.ps1` (Windows) or `setup_env.sh` (Linux/macOS)
- [ ] Verify environment variable: `echo $env:OPENAI_API_KEY` (Windows)
- [ ] Test API connection: `python test_claude_simple.py`

### 4. Configuration File
- [ ] Review `config/settings.json`
- [ ] Verify provider is set to "anthropic"
- [ ] Verify model is set to "claude-sonnet-4-6"
- [ ] Verify api_key is empty (uses environment variable)

### 5. Unreal Engine Setup
- [ ] Open your UE5 project
- [ ] Enable "Python Editor Script Plugin" in Edit → Plugins
- [ ] Restart Unreal Engine
- [ ] Verify Python console available (Window → Developer Tools → Output Log)

### 6. Test in Unreal Engine
- [ ] Open Python console in UE5
- [ ] Add tool to sys.path
- [ ] Import a module (e.g., `from utils.config import Config`)
- [ ] Run a simple command

### 7. Documentation Review
- [ ] Read `README.md` for project overview
- [ ] Read `docs/INSTALLATION.md` for detailed setup
- [ ] Read `docs/UE5_SETUP.md` for UE5-specific setup
- [ ] Read `docs/USAGE.md` for feature documentation
- [ ] Read `docs/ENV_SETUP.md` for API key setup

## 🧪 Testing Checklist

### Configuration Tests
- [ ] Run `python test_config.py` - Should show all ✓
- [ ] Verify API key is loaded
- [ ] Verify provider is "anthropic"
- [ ] Verify model is "claude-sonnet-4-6"

### API Tests (Requires Credits)
- [ ] Run `python test_claude_simple.py`
- [ ] Test 1: Simple completion - Should return asset name
- [ ] Test 2: Material parameters - Should return JSON
- [ ] Test 3: Asset classification - Should return category/folder

### Unreal Engine Tests
- [ ] Import Config module in UE5 Python console
- [ ] Get selected assets
- [ ] Run basic asset organization
- [ ] Run QA checks on an asset

## 🚨 Common Issues

### Issue: "Your credit balance is too low"
**Solution**: Add credits at https://console.anthropic.com/settings/billing

### Issue: "OPENAI_API_KEY not found"
**Solution**: 
1. Run setup script again
2. Restart terminal/UE5
3. Verify with `echo $env:OPENAI_API_KEY`

### Issue: "ModuleNotFoundError: No module named 'anthropic'"
**Solution**: `pip install -r requirements.txt`

### Issue: "ImportError: attempted relative import"
**Solution**: Add src to sys.path: `sys.path.append('path/to/src')`

### Issue: Python console not available in UE5
**Solution**: 
1. Edit → Plugins
2. Enable "Python Editor Script Plugin"
3. Restart UE5

## 📊 Configuration Summary

After completing setup, your configuration should be:

```json
{
  "llm": {
    "provider": "anthropic",
    "model": "claude-sonnet-4-6",
    "api_key": "",
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
```

Environment Variable:
```
OPENAI_API_KEY = sk-ant-api03-[your-key-here]
```

## ✨ Ready to Use!

Once all checkboxes are complete, you're ready to:
- Organize assets automatically
- Generate AI-powered asset names
- Create materials from descriptions
- Run QA validation checks
- Optimize textures and LODs

Refer to `docs/USAGE.md` for detailed feature documentation.
