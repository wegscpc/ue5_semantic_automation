import unreal
from typing import List, Dict, Optional
import sys
import os

# Add parent directory to path for imports
if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger
from core.asset_classifier import AssetClassifier

logger = setup_logger(__name__)


class AssetOrganizer:
    
    ASSET_PREFIX_MAPPING = {
        "StaticMesh": "SM_",
        "SkeletalMesh": "SK_",
        "Texture2D": "T_",
        "Material": "M_",
        "MaterialInstanceConstant": "MI_",
        "MaterialFunction": "MF_",
        "BlueprintGeneratedClass": "BP_",
        "ParticleSystem": "PS_",
        "SoundWave": "S_",
        "SoundCue": "SC_",
        "AnimSequence": "A_",
        "AnimBlueprint": "ABP_",
        "WidgetBlueprint": "WBP_",
        "PhysicsAsset": "PHYS_",
    }
    
    FOLDER_STRUCTURE = {
        "SM_": "Meshes/StaticMeshes",
        "SK_": "Meshes/SkeletalMeshes",
        "T_": "Textures",
        "M_": "Materials",
        "MI_": "Materials/Instances",
        "MF_": "Materials/Functions",
        "BP_": "Blueprints",
        "PS_": "FX/Particles",
        "S_": "Audio/Sounds",
        "SC_": "Audio/Cues",
        "A_": "Animations/Sequences",
        "ABP_": "Animations/Blueprints",
        "WBP_": "UI/Widgets",
        "PHYS_": "Physics",
    }
    
    def __init__(self):
        self.editor_util = unreal.EditorUtilityLibrary
        self.editor_asset_lib = unreal.EditorAssetLibrary
        self.asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    def organize_selected_assets(self) -> Dict[str, int]:
        selected_assets = self.editor_util.get_selected_assets()
        
        if not selected_assets:
            logger.warning("No assets selected for organization")
            return {"renamed": 0, "moved": 0, "errors": 0}
        
        stats = {"renamed": 0, "moved": 0, "errors": 0}
        
        for asset in selected_assets:
            try:
                if self._organize_single_asset(asset):
                    stats["renamed"] += 1
                    stats["moved"] += 1
            except Exception as e:
                logger.error(f"Error organizing asset {asset.get_name()}: {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"Organization complete: {stats}")
        return stats
    
    def _organize_single_asset(self, asset) -> bool:
        asset_name = asset.get_name()
        asset_class = asset.get_class().get_name()
        asset_path = asset.get_path_name()
        
        prefix = self.ASSET_PREFIX_MAPPING.get(asset_class, "")
        
        if not prefix:
            logger.warning(f"No prefix mapping for asset class: {asset_class}")
            return False
        
        new_name = asset_name
        if not asset_name.startswith(prefix):
            new_name = f"{prefix}{asset_name}"
        
        target_folder = self._get_target_folder(prefix)
        current_folder = asset_path.rsplit('/', 1)[0]
        
        if target_folder not in current_folder or new_name != asset_name:
            new_path = f"{target_folder}/{new_name}"
            
            if self.editor_asset_lib.does_asset_exist(new_path):
                logger.warning(f"Asset already exists at {new_path}")
                return False
            
            success = self.editor_asset_lib.rename_asset(asset_path, new_path)
            
            if success:
                logger.info(f"Successfully organized: {asset_name} -> {new_path}")
                return True
            else:
                logger.error(f"Failed to rename/move asset: {asset_name}")
                return False
        
        return False
    
    def _get_target_folder(self, prefix: str) -> str:
        base_path = "/Game/Content"
        subfolder = self.FOLDER_STRUCTURE.get(prefix, "Misc")
        return f"{base_path}/{subfolder}"
    
    def organize_entire_content_folder(self, root_path: str = "/Game/") -> Dict[str, int]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {"renamed": 0, "moved": 0, "errors": 0, "total": len(all_assets)}
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and self._organize_single_asset(asset):
                    stats["renamed"] += 1
                    stats["moved"] += 1
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"Bulk organization complete: {stats}")
        return stats
    
    def create_folder_structure(self, base_path: str = "/Game/Content"):
        for folder in set(self.FOLDER_STRUCTURE.values()):
            full_path = f"{base_path}/{folder}"
            if not self.editor_asset_lib.does_directory_exist(full_path):
                self.editor_asset_lib.make_directory(full_path)
                logger.info(f"Created folder: {full_path}")
