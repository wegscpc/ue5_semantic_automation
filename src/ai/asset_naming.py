import unreal
from typing import Optional, Dict, List
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.llm_client import LLMClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


class AIAssetNaming:
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
        self.editor_asset_lib = unreal.EditorAssetLibrary
    
    def suggest_name_for_unclear_asset(self, asset) -> Optional[str]:
        asset_name = asset.get_name()
        
        if self._is_name_unclear(asset_name):
            asset_metadata = {
                'name': asset_name,
                'class': asset.get_class().get_name(),
                'path': asset.get_path_name()
            }
            
            suggested_name = self.llm_client.suggest_asset_name(asset_metadata)
            
            if suggested_name:
                logger.info(f"AI suggested name: {asset_name} -> {suggested_name}")
                return suggested_name
        
        return None
    
    def _is_name_unclear(self, asset_name: str) -> bool:
        unclear_patterns = [
            'asset_',
            'untitled',
            'new',
            'temp',
            'test',
            lambda name: name.isdigit(),
            lambda name: len(name) < 3,
            lambda name: name.count('_') > 5,
        ]
        
        name_lower = asset_name.lower()
        
        for pattern in unclear_patterns:
            if callable(pattern):
                if pattern(name_lower):
                    return True
            elif pattern in name_lower:
                return True
        
        return False
    
    def batch_rename_unclear_assets(self, root_path: str = "/Game/") -> Dict[str, int]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {"analyzed": 0, "renamed": 0, "skipped": 0, "errors": 0}
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    stats["analyzed"] += 1
                    
                    suggested_name = self.suggest_name_for_unclear_asset(asset)
                    
                    if suggested_name:
                        current_path = asset.get_path_name()
                        folder = current_path.rsplit('/', 1)[0]
                        new_path = f"{folder}/{suggested_name}"
                        
                        if not self.editor_asset_lib.does_asset_exist(new_path):
                            if self.editor_asset_lib.rename_asset(current_path, new_path):
                                stats["renamed"] += 1
                                logger.info(f"Renamed: {asset.get_name()} -> {suggested_name}")
                            else:
                                stats["errors"] += 1
                        else:
                            stats["skipped"] += 1
                            logger.warning(f"Asset already exists: {new_path}")
                    else:
                        stats["skipped"] += 1
                        
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"AI naming complete: {stats}")
        return stats
    
    def validate_naming_convention(self, asset_name: str, asset_class: str) -> Dict[str, any]:
        prefix_mapping = {
            "StaticMesh": "SM_",
            "SkeletalMesh": "SK_",
            "Texture2D": "T_",
            "Material": "M_",
            "MaterialInstanceConstant": "MI_",
            "BlueprintGeneratedClass": "BP_",
        }
        
        expected_prefix = prefix_mapping.get(asset_class, "")
        
        validation = {
            "is_valid": True,
            "issues": [],
            "suggestions": []
        }
        
        if expected_prefix and not asset_name.startswith(expected_prefix):
            validation["is_valid"] = False
            validation["issues"].append(f"Missing expected prefix: {expected_prefix}")
            validation["suggestions"].append(f"{expected_prefix}{asset_name}")
        
        if len(asset_name) > 64:
            validation["is_valid"] = False
            validation["issues"].append("Name too long (max 64 characters)")
        
        if ' ' in asset_name:
            validation["is_valid"] = False
            validation["issues"].append("Name contains spaces")
            validation["suggestions"].append(asset_name.replace(' ', '_'))
        
        if self._is_name_unclear(asset_name):
            validation["is_valid"] = False
            validation["issues"].append("Name is unclear or generic")
        
        return validation
