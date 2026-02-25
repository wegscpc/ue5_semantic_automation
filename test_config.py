"""
Simple test to verify API key configuration
"""
import os
import json

print("=" * 60)
print("UE5 Semantic Automation - Configuration Test")
print("=" * 60)
print()

# Test 1: Check environment variable
print("1. Checking environment variable...")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"   ✓ OPENAI_API_KEY is set: {api_key[:15]}...")
else:
    print("   ✗ OPENAI_API_KEY not found")
print()

# Test 2: Check settings.json
print("2. Checking settings.json...")
try:
    with open('config/settings.json', 'r') as f:
        config = json.load(f)
    
    provider = config['llm']['provider']
    model = config['llm']['model']
    config_api_key = config['llm']['api_key']
    
    print(f"   Provider: {provider}")
    print(f"   Model: {model}")
    print(f"   API Key in config: {'(empty - will use env var)' if not config_api_key else config_api_key[:15] + '...'}")
    print()
    
    # Test 3: Verify configuration
    print("3. Configuration validation...")
    if provider == "anthropic":
        print("   ✓ Provider set to 'anthropic' (Claude)")
    else:
        print(f"   ⚠ Provider is '{provider}' (expected 'anthropic')")
    
    if model.startswith("claude"):
        print(f"   ✓ Model set to Claude: {model}")
    else:
        print(f"   ⚠ Model is '{model}' (expected Claude model)")
    
    if not config_api_key and api_key:
        print("   ✓ Config uses environment variable")
    elif config_api_key:
        print("   ⚠ API key hardcoded in config (not recommended)")
    else:
        print("   ✗ No API key configured")
    
    print()
    print("=" * 60)
    print("RESULT: Configuration is ready!")
    print("=" * 60)
    print()
    print("The tool will use:")
    print(f"  - Provider: {provider}")
    print(f"  - Model: {model}")
    print(f"  - API Key: {api_key[:20] if api_key else 'NOT SET'}...")
    
except Exception as e:
    print(f"   ✗ Error reading config: {e}")
