import unreal

def organize_assets():
    # 1. Get all selected assets in the Content Browser
    selected_assets = unreal.EditorUtilityLibrary.get_selected_assets()
    
    if not selected_assets:
        unreal.log_warning("No assets are selected to organize.`")
        return

    # 2. Dictionary of standard prefixes (Best Practices)
    mapping = {
        "StaticMesh": "SM_",
        "Texture2D": "T_",
        "Material": "M_",
        "MaterialInstanceConstant": "MI_",
        "BlueprintGeneratedClass": "BP_"
    }

    for asset in selected_assets:
        asset_name = asset.get_name()
        asset_class = asset.get_class().get_name()
        
        # 3. Determine the correct prefix
        prefix = mapping.get(asset_class, "")
        
        if prefix and not asset_name.startswith(prefix):
            new_name = f"{prefix}{asset_name}"
            asset_path = asset.get_path_name()
            new_path = asset_path.replace(asset_name, new_name)
            
            # 4. Rename and move (Automation logic)
            unreal.EditorAssetLibrary.rename_asset(asset_path, new_path)
            unreal.log(f"Asset renamed successfully: {new_name}")

# Run the function
organize_assets()