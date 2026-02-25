# UE5 Quick Commands Reference

Copy and paste these commands into the UE5 Python console.

## Setup (Run Once Per Session)

```python
import sys
# Replace with your actual project path
sys.path.append('/path/to/your/ue5_semantic_automation/src')
```

---

## 1. Asset Organization

**Select assets in Content Browser first**, then run:

```python
from core.asset_organizer import AssetOrganizer
import unreal

selected = unreal.EditorUtilityLibrary.get_selected_assets()

if len(selected) == 0:
    print("⚠ No assets selected. Please select some assets in Content Browser.")
else:
    organizer = AssetOrganizer()
    print(f"Organizing {len(selected)} assets...")
    
    # Use the organize_selected_assets method
    stats = organizer.organize_selected_assets()
    
    print(f"\n✓ Organization complete!")
    print(f"  Renamed: {stats['renamed']}")
    print(f"  Moved: {stats['moved']}")
    print(f"  Errors: {stats['errors']}")
```

---

## 2. QA Sanity Checks

**Select assets in Content Browser first**, then run:

```python
from qa.sanity_checker import SanityChecker
import unreal

selected = unreal.EditorUtilityLibrary.get_selected_assets()

if len(selected) == 0:
    print("⚠ No assets selected. Please select some assets in Content Browser.")
else:
    checker = SanityChecker()
    print(f"Running QA checks on {len(selected)} assets...\n")
    
    for asset in selected:
        issues = checker.check_asset(asset)
        
        if issues:
            print(f"{asset.get_name()}:")
            for issue in issues:
                print(f"  {issue['severity']}: {issue['message']}")
        else:
            print(f"✓ {asset.get_name()} - No issues found")
```

---

## 3. AI Asset Naming (Requires Claude API)

**Select assets in Content Browser first**, then run:

```python
from ai.asset_naming import AIAssetNaming
import unreal

selected = unreal.EditorUtilityLibrary.get_selected_assets()

if len(selected) == 0:
    print("⚠ No assets selected. Please select some assets in Content Browser.")
else:
    naming = AIAssetNaming()
    
    for asset in selected:
        current_name = asset.get_name()
        print(f"\nAsset: {current_name}")
        print("Asking Claude for suggestion...")
        
        # This only suggests names for unclear/poorly named assets
        suggestion = naming.suggest_name_for_unclear_asset(asset)
        
        if suggestion:
            print(f"✓ Suggested name: {suggestion}")
        else:
            print("⚠ Asset name is clear, no suggestion needed")
```

---

## 4. Generate Material from Description (Requires Claude API)

```python
import sys
# Replace with your actual project path
sys.path.append('/path/to/your/ue5_semantic_automation/src')

from materials.material_generator import MaterialGenerator

generator = MaterialGenerator()

# Customize the description
description = "shiny blue metal with scratches"

print(f"Generating material: {description}")
print("Asking Claude to generate material parameters...")

material_path = generator.generate_material_from_prompt(description)

if material_path:
    print(f"✓ Material created successfully!")
    print(f"  Path: {material_path}")
else:
    print("✗ Failed to create material")
```

---

## 5. Texture Optimization

**Select texture assets in Content Browser first**, then run:

```python
import sys
# Replace with your actual project path
sys.path.append('/path/to/your/ue5_semantic_automation/src')

from optimization.texture_optimizer import TextureOptimizer
import unreal

selected = unreal.EditorUtilityLibrary.get_selected_assets()

if len(selected) == 0:
    print("⚠ No assets selected. Please select some texture assets.")
else:
    optimizer = TextureOptimizer()
    
    for asset in selected:
        if asset.get_class().get_name() == "Texture2D":
            print(f"\nAnalyzing texture: {asset.get_name()}")
            
            # Get current size
            width = asset.blueprint_get_size_x()
            height = asset.blueprint_get_size_y()
            print(f"  Current size: {width}x{height}")
            
            # Test different viewing distances
            for distance in ["close", "medium", "far"]:
                print(f"\n  Viewing distance: {distance}")
                needs_optimization = optimizer.optimize_texture_for_distance(asset, viewing_distance=distance)
                
                if needs_optimization:
                    print(f"    ✓ Optimization recommended")
                else:
                    print(f"    ✓ Already optimized")
        else:
            print(f"⚠ {asset.get_name()} is not a texture, skipping")
```

---

## 6. Check Configuration

```python
from utils.config import Config

config = Config()

print("Current Configuration:")
print(f"  Provider: {config.get('llm.provider')}")
print(f"  Model: {config.get('llm.model')}")
print(f"  Temperature: {config.get('llm.temperature')}")
print(f"  Max Tokens: {config.get('llm.max_tokens')}")
```

---

## 7. List All Assets in a Folder

```python
import unreal

# Change this path to your folder
folder_path = "/Game/Content"

asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = asset_registry.get_assets_by_path(folder_path, recursive=True)

print(f"Found {len(assets)} assets in {folder_path}:\n")

for asset_data in assets[:20]:  # Show first 20
    asset_name = asset_data.asset_name
    asset_class = asset_data.asset_class_path.asset_name
    print(f"  - {asset_name} ({asset_class})")

if len(assets) > 20:
    print(f"\n... and {len(assets) - 20} more")
```

---

## Tips

1. **Always select assets first** in the Content Browser before running organization/QA commands
2. **AI features require Claude API credits** - make sure your API key is configured
3. **Use the Output Log** (Window → Developer Tools → Output Log) and select "Python" to see results
4. **Run setup command** (`sys.path.append(...)`) once per UE5 session
5. **Check logs** in your project's `Saved/Logs/` folder for detailed errors

---

## Troubleshooting

**Import Error**: Restart UE5 to clear Python module cache

**API Error**: Check that `OPENAI_API_KEY` environment variable is set and has credits

**No Assets Selected**: Select assets in Content Browser before running commands
