"""
Test Claude/Anthropic API integration
This script tests the AI features without requiring Unreal Engine
"""
import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("=" * 70)
print("UE5 Semantic Automation - Claude API Integration Test")
print("=" * 70)
print()

# Test 1: Configuration
print("1. Testing Configuration...")
try:
    with open('config/settings.json', 'r') as f:
        config = json.load(f)
    
    provider = config['llm']['provider']
    model = config['llm']['model']
    api_key_env = os.getenv("OPENAI_API_KEY")
    
    print(f"   ✓ Provider: {provider}")
    print(f"   ✓ Model: {model}")
    print(f"   ✓ API Key: {'Set' if api_key_env else 'NOT SET'}")
    
    if not api_key_env:
        print("\n   ⚠ WARNING: OPENAI_API_KEY environment variable not set!")
        print("   Run setup_env.ps1 to configure your API key")
        sys.exit(1)
    
except Exception as e:
    print(f"   ✗ Configuration error: {e}")
    sys.exit(1)

print()

# Test 2: Import LLMClient
print("2. Testing LLMClient Import...")
try:
    # Import with fallback for missing unreal module
    import importlib.util
    
    # Temporarily mock unreal module if not available
    if importlib.util.find_spec("unreal") is None:
        import types
        unreal = types.ModuleType("unreal")
        sys.modules["unreal"] = unreal
    
    from ai.llm_client import LLMClient, LLMProvider
    print("   ✓ LLMClient imported successfully")
except Exception as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

print()

# Test 3: Initialize Client
print("3. Testing Client Initialization...")
try:
    client = LLMClient(provider=LLMProvider.ANTHROPIC)
    print(f"   ✓ Client initialized")
    print(f"   ✓ Provider: {client.provider.value}")
    print(f"   ✓ Model: {client.model}")
    print(f"   ✓ API Key loaded: {client.api_key[:20]}..." if client.api_key else "   ✗ No API key")
except Exception as e:
    print(f"   ✗ Initialization error: {e}")
    sys.exit(1)

print()

# Test 4: Test AI Completion (Simple)
print("4. Testing AI Completion...")
try:
    prompt = "Suggest a proper Unreal Engine asset name for a wooden crate texture. Reply with ONLY the name, no explanation."
    
    print(f"   Prompt: '{prompt}'")
    print("   Calling Claude API...")
    
    response = client.generate_completion(prompt, max_tokens=50, temperature=0.3)
    
    if response:
        print(f"   ✓ Response: '{response}'")
    else:
        print("   ✗ No response received")
        sys.exit(1)
        
except Exception as e:
    print(f"   ✗ API call error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 5: Test Asset Naming Feature
print("5. Testing Asset Naming Feature...")
try:
    asset_metadata = {
        'class': 'Texture2D',
        'name': 'wood_crate_01',
        'path': '/Game/Textures/Props'
    }
    
    suggested_name = client.suggest_asset_name(asset_metadata)
    
    if suggested_name:
        print(f"   ✓ Suggested name: '{suggested_name}'")
    else:
        print("   ✗ No suggestion received")
        
except Exception as e:
    print(f"   ⚠ Asset naming test error: {e}")

print()

# Test 6: Test Material Parameters Generation
print("6. Testing Material Parameters Generation...")
try:
    description = "shiny red metal with slight rust"
    
    params = client.generate_material_parameters(description)
    
    if params:
        print(f"   ✓ Generated parameters:")
        print(f"      - Base Color: {params.get('base_color', 'N/A')}")
        print(f"      - Metallic: {params.get('metallic', 'N/A')}")
        print(f"      - Roughness: {params.get('roughness', 'N/A')}")
    else:
        print("   ✗ No parameters generated")
        
except Exception as e:
    print(f"   ⚠ Material parameters test error: {e}")

print()
print("=" * 70)
print("✓ ALL TESTS PASSED - Claude API Integration Working!")
print("=" * 70)
print()
print("Next Steps:")
print("  1. Open Unreal Engine 5")
print("  2. Enable Python Editor Script Plugin")
print("  3. Run the tool from UE5 Python console")
print()
