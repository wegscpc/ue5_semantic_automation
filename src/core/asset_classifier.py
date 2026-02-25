import unreal
from typing import Dict, Optional, List
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

logger = setup_logger(__name__)


class AssetClassifier:
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
        self.asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    def classify_asset_by_name(self, asset_name: str) -> Optional[str]:
        name_lower = asset_name.lower()
        
        if any(keyword in name_lower for keyword in ['mesh', 'model', 'geo', 'sm_']):
            return "StaticMesh"
        elif any(keyword in name_lower for keyword in ['texture', 'tex', 'diffuse', 'normal', 'roughness', 't_']):
            return "Texture2D"
        elif any(keyword in name_lower for keyword in ['material', 'mat', 'm_', 'mi_']):
            return "Material"
        elif any(keyword in name_lower for keyword in ['blueprint', 'bp_']):
            return "BlueprintGeneratedClass"
        elif any(keyword in name_lower for keyword in ['sound', 'audio', 's_', 'sc_']):
            return "SoundWave"
        elif any(keyword in name_lower for keyword in ['anim', 'animation', 'a_']):
            return "AnimSequence"
        elif any(keyword in name_lower for keyword in ['particle', 'fx', 'vfx', 'ps_']):
            return "ParticleSystem"
        elif any(keyword in name_lower for keyword in ['skeletal', 'sk_', 'skel']):
            return "SkeletalMesh"
        
        return None
    
    def get_asset_metadata(self, asset) -> Dict[str, any]:
        asset_data = self.asset_registry.get_asset_by_object_path(asset.get_path_name())
        
        metadata = {
            "name": asset.get_name(),
            "class": asset.get_class().get_name(),
            "path": asset.get_path_name(),
            "package_name": asset_data.package_name if asset_data else None,
        }
        
        if asset_data:
            tag_values = asset_data.get_tags_and_values()
            metadata["tags"] = {tag.key: tag.value for tag in tag_values}
        
        return metadata
    
    def analyze_asset_usage(self, asset_path: str) -> Dict[str, any]:
        referencers = self.editor_asset_lib.find_package_referencers_for_asset(asset_path)
        
        return {
            "asset_path": asset_path,
            "reference_count": len(referencers),
            "referencers": referencers,
            "is_used": len(referencers) > 0
        }
    
    def find_unused_assets(self, root_path: str = "/Game/") -> List[str]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        unused_assets = []
        
        for asset_path in all_assets:
            usage_info = self.analyze_asset_usage(asset_path)
            if not usage_info["is_used"]:
                unused_assets.append(asset_path)
        
        logger.info(f"Found {len(unused_assets)} unused assets")
        return unused_assets
    
    def categorize_assets_by_type(self, asset_paths: List[str]) -> Dict[str, List[str]]:
        categorized = {}
        
        for asset_path in asset_paths:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    asset_class = asset.get_class().get_name()
                    if asset_class not in categorized:
                        categorized[asset_class] = []
                    categorized[asset_class].append(asset_path)
            except Exception as e:
                logger.error(f"Error categorizing {asset_path}: {str(e)}")
        
        return categorized
