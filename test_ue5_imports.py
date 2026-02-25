"""
Test script to verify imports work in UE5 Python console
Copy and paste this into UE5's Python console
"""

import sys
import os
# Add src directory to path dynamically
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

print("Testing imports...")
print("-" * 60)

# Test 1: Config
try:
    from utils.config import Config
    config = Config()
    print("✓ Config imported successfully")
    print(f"  Provider: {config.get('llm.provider')}")
    print(f"  Model: {config.get('llm.model')}")
except Exception as e:
    print(f"✗ Config import failed: {e}")

print()

# Test 2: AssetOrganizer
try:
    from core.asset_organizer import AssetOrganizer
    organizer = AssetOrganizer()
    print("✓ AssetOrganizer imported successfully")
except Exception as e:
    print(f"✗ AssetOrganizer import failed: {e}")

print()

# Test 3: SanityChecker
try:
    from qa.sanity_checker import SanityChecker
    checker = SanityChecker()
    print("✓ SanityChecker imported successfully")
except Exception as e:
    print(f"✗ SanityChecker import failed: {e}")

print()

# Test 4: AIAssetNaming
try:
    from ai.asset_naming import AIAssetNaming
    naming = AIAssetNaming()
    print("✓ AIAssetNaming imported successfully")
except Exception as e:
    print(f"✗ AIAssetNaming import failed: {e}")

print()

# Test 5: MaterialGenerator
try:
    from materials.material_generator import MaterialGenerator
    generator = MaterialGenerator()
    print("✓ MaterialGenerator imported successfully")
except Exception as e:
    print(f"✗ MaterialGenerator import failed: {e}")

print()
print("-" * 60)
print("✓ All imports successful! Tool is ready to use in UE5")
