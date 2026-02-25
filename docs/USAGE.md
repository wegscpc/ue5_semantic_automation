# Usage Guide

## Table of Contents
- [Getting Started](#getting-started)
- [Asset Organization](#asset-organization)
- [Quality Assurance](#quality-assurance)
- [Texture Optimization](#texture-optimization)
- [Material Generation](#material-generation)
- [Advanced Usage](#advanced-usage)

## Getting Started

### Initializing the Tool

```python
import sys
sys.path.append('path/to/ue5_semantic_automation/src')

from main import UE5AutomationTool

# Create tool instance
tool = UE5AutomationTool()
```

## Asset Organization

### Organize Selected Assets

Select assets in the Content Browser, then run:

```python
# Organize selected assets
stats = tool.organize_selected_assets()
print(f"Organized {stats['renamed']} assets")
```

### Organize Entire Project

```python
# Create standard folder structure
tool.organizer.create_folder_structure()

# Organize all assets in /Game/
stats = tool.organizer.organize_entire_content_folder()
```

### Custom Organization

```python
from core.asset_organizer import AssetOrganizer

organizer = AssetOrganizer()

# Organize specific folder
stats = organizer.organize_entire_content_folder(root_path="/Game/MyFolder")
```

## Quality Assurance

### Run Sanity Check

```python
# Full sanity check
stats = tool.run_sanity_check()

print(f"Total issues: {stats['issues_found']}")
print(f"Critical: {stats['critical_issues']}")
print(f"Warnings: {stats['warnings']}")
```

### Get Specific Issues

```python
# Get critical issues only
critical = tool.sanity_checker.get_critical_issues()

for issue in critical:
    print(f"{issue['asset']}: {issue['message']}")
```

### Validate Textures

```python
from qa.texture_validator import TextureValidator

validator = TextureValidator()

# Validate specific texture
texture = unreal.EditorAssetLibrary.load_asset("/Game/Textures/T_MyTexture")
validation = validator.validate_texture(texture)

if not validation['is_valid']:
    print(f"Issues: {validation['issues']}")
```

### Find Problematic Assets

```python
# Find oversized textures
oversized = validator.get_oversized_textures(max_size=2048)

for tex in oversized:
    print(f"{tex['path']}: {tex['size']}")
```

## Texture Optimization

### Optimize for Viewing Distance

```python
# Optimize for different viewing distances
tool.optimize_textures(viewing_distance="close")    # High quality
tool.optimize_textures(viewing_distance="medium")   # Balanced
tool.optimize_textures(viewing_distance="far")      # Performance
tool.optimize_textures(viewing_distance="very_far") # Maximum performance
```

### Generate Optimization Report

```python
from optimization.texture_optimizer import TextureOptimizer

optimizer = TextureOptimizer()

# Get detailed report
report = optimizer.generate_optimization_report()

print(f"Total memory: {report['total_memory_mb']} MB")
print(f"Potential savings: {report['potential_savings_mb']} MB")

# Show optimization opportunities
for opp in report['optimization_opportunities']:
    print(f"{opp['path']}: Save {opp['potential_savings_mb']} MB")
```

### Apply Compression

```python
# Apply optimal compression to textures
texture = unreal.EditorAssetLibrary.load_asset("/Game/Textures/T_Diffuse")

optimizer.apply_optimal_compression(texture, texture_type="diffuse")
# Options: diffuse, normal, mask, grayscale, hdr
```

## Material Generation

### Generate from Natural Language

```python
# Simple material generation
material = tool.generate_material_from_description(
    "wet stone with moss and puddles"
)

print(f"Created: {material}")
```

### Batch Material Generation

```python
from materials.material_generator import MaterialGenerator

generator = MaterialGenerator()

prompts = [
    "shiny metal with scratches",
    "old weathered wood",
    "polished marble floor",
    "glowing neon sign"
]

stats = generator.batch_generate_materials(prompts)
print(f"Created {stats['materials_created']} materials")
```

### Use Specific Master Material

```python
# Generate with specific master material
material = generator.generate_material_from_prompt(
    "wet stone with moss",
    master_material_path="/Game/Materials/Masters/M_StandardPBR"
)
```

### Get Texture Suggestions

```python
# Get AI suggestions for required textures
textures = generator.suggest_textures_for_material(
    "rusty metal with scratches"
)

print(f"Suggested textures: {textures}")
# Output: ['diffuse', 'normal', 'roughness', 'metallic', 'ao']
```

## Advanced Usage

### AI Asset Naming

```python
from ai.asset_naming import AIAssetNaming

ai_naming = AIAssetNaming()

# Rename unclear assets
stats = ai_naming.batch_rename_unclear_assets()
print(f"Renamed {stats['renamed']} assets")
```

### Metadata Generation

```python
from ai.metadata_generator import MetadataGenerator

metadata_gen = MetadataGenerator()

# Generate tags for selected assets
selected = unreal.EditorUtilityLibrary.get_selected_assets()

for asset in selected:
    tags = metadata_gen.generate_asset_tags(asset)
    description = metadata_gen.generate_ai_description(asset)
    
    metadata_gen.apply_metadata_to_asset(asset, tags, description)
```

### LOD Analysis

```python
from optimization.lod_generator import LODGenerator

lod_gen = LODGenerator()

# Analyze LOD coverage
analysis = lod_gen.analyze_lod_coverage()

print(f"Meshes with LODs: {analysis['meshes_with_lods']}")
print(f"Meshes needing LODs: {analysis['meshes_without_lods']}")

# Generate LODs for meshes without them
lod_gen.batch_generate_lods(num_lods=3)
```

### Master Material Management

```python
from materials.master_material_manager import MasterMaterialManager

manager = MasterMaterialManager()

# List available master materials
masters = manager.list_available_master_materials()

# Get usage statistics
analysis = manager.analyze_master_material_usage()

for stat in analysis['usage_stats']:
    print(f"{stat['master_material']}: {stat['instance_count']} instances")
```

### Custom Configuration

```python
from utils.config import Config

config = Config()

# Modify settings
config.set("optimization.max_texture_resolution", 4096)
config.set("qa.enforce_power_of_two", True)

# Save configuration
config.save_config()

# Get specific settings
llm_config = config.get_llm_config()
```

## Workflow Examples

### Complete Project Setup

```python
# 1. Create folder structure
tool.organizer.create_folder_structure()

# 2. Organize all assets
tool.organizer.organize_entire_content_folder()

# 3. Run QA check
stats = tool.run_sanity_check()

# 4. Fix critical issues manually, then optimize
tool.optimize_textures(viewing_distance="medium")

# 5. Generate metadata for searchability
tool.generate_metadata_for_assets()
```

### Daily Asset Cleanup

```python
# 1. Organize new assets
tool.organize_selected_assets()

# 2. Validate textures
validator = TextureValidator()
stats = validator.batch_validate_textures()

# 3. Check for issues
critical = tool.sanity_checker.get_critical_issues()

if critical:
    print("⚠️ Critical issues found!")
    for issue in critical:
        print(f"  - {issue['asset']}: {issue['message']}")
```

### Material Creation Pipeline

```python
# 1. Get AI recommendation for master material
manager = MasterMaterialManager()
master = manager.recommend_master_material("wet stone")

# 2. Generate material
generator = MaterialGenerator()
material = generator.generate_material_from_prompt(
    "wet stone with moss",
    master_material_path=master
)

# 3. Get texture suggestions
textures = generator.suggest_textures_for_material("wet stone with moss")
print(f"You'll need these textures: {textures}")
```

## Tips and Best Practices

1. **Always backup** before running batch operations
2. **Start small** - test on a few assets before running on entire project
3. **Review AI suggestions** before applying to production assets
4. **Run QA checks regularly** to catch issues early
5. **Use viewing distance optimization** based on actual use case
6. **Generate metadata** for better team collaboration
7. **Monitor memory usage** with optimization reports

## Troubleshooting

### Assets not organizing correctly
- Check naming conventions in `AssetOrganizer.ASSET_PREFIX_MAPPING`
- Verify folder structure exists
- Check permissions on target folders

### AI features not working
- Verify API key is set in config
- Check internet connection
- Ensure you have API credits

### Performance issues
- Process assets in smaller batches
- Disable logging for large operations
- Use specific paths instead of entire project

## Next Steps

- Explore [API Reference](API.md) for detailed function documentation
- Check [Configuration Guide](CONFIGURATION.md) for customization options
- Review [Examples](../examples/) for more use cases
