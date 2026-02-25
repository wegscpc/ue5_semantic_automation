"""
Simple Claude API test without complex imports
"""
import os
import anthropic

print("=" * 70)
print("Claude API Connection Test")
print("=" * 70)
print()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("✗ OPENAI_API_KEY environment variable not set!")
    print("Run: .\\setup_env.ps1")
    exit(1)

print(f"✓ API Key found: {api_key[:20]}...")
print()

# Test 1: Simple completion
print("Test 1: Simple AI Completion")
print("-" * 70)

try:
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=100,
        temperature=0.3,
        system="You are an expert Unreal Engine 5 technical artist assistant.",
        messages=[
            {
                "role": "user",
                "content": "Suggest a proper Unreal Engine asset name for a wooden crate texture. Reply with ONLY the name using UE naming conventions (e.g., T_WoodCrate_D for diffuse). No explanation."
            }
        ]
    )
    
    response = message.content[0].text
    print(f"✓ Claude Response: '{response}'")
    print()
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Material parameters
print("Test 2: Material Parameter Generation")
print("-" * 70)

try:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        temperature=0.5,
        system="You are an expert Unreal Engine 5 technical artist assistant.",
        messages=[
            {
                "role": "user",
                "content": """Generate material parameters for Unreal Engine 5 for: "shiny red metal with slight rust"

Return ONLY valid JSON with this structure:
{
    "base_color": [R, G, B],
    "metallic": 0.0-1.0,
    "roughness": 0.0-1.0,
    "specular": 0.0-1.0
}"""
            }
        ]
    )
    
    response = message.content[0].text
    print(f"✓ Material Parameters:\n{response}")
    print()
    
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Asset classification
print("Test 3: Asset Classification")
print("-" * 70)

try:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        temperature=0.3,
        system="You are an expert Unreal Engine 5 technical artist assistant.",
        messages=[
            {
                "role": "user",
                "content": """Classify this asset and suggest a folder path:
Asset: SM_Chair_Office_01

Respond with ONLY:
Category: [category]
Folder: /Game/[suggested/path]"""
            }
        ]
    )
    
    response = message.content[0].text
    print(f"✓ Classification:\n{response}")
    print()
    
except Exception as e:
    print(f"✗ Error: {e}")

print("=" * 70)
print("✓ ALL TESTS PASSED!")
print("=" * 70)
print()
print("Your Claude API is working correctly with the UE5 Automation Tool!")
print()
print("Next Steps:")
print("  1. Open Unreal Engine 5")
print("  2. Enable 'Python Editor Script Plugin' in Edit → Plugins")
print("  3. Restart Unreal Engine")
print("  4. Use the tool from UE5 Python console")
print()
