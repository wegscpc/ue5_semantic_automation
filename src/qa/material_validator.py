import unreal
from typing import Dict, List, Optional
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

logger = setup_logger(__name__)


class MaterialValidator:
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
    
    def validate_material(self, material) -> Dict[str, any]:
        validation = {
            "asset": material.get_name(),
            "path": material.get_path_name(),
            "is_valid": True,
            "issues": [],
            "warnings": [],
            "info": {}
        }
        
        try:
            material_class = material.get_class().get_name()
            validation["info"]["type"] = material_class
            
            if material_class == "Material":
                self._validate_master_material(material, validation)
            elif material_class == "MaterialInstanceConstant":
                self._validate_material_instance(material, validation)
            
        except Exception as e:
            logger.error(f"Error validating material {material.get_name()}: {str(e)}")
            validation["is_valid"] = False
            validation["issues"].append(f"Validation error: {str(e)}")
        
        return validation
    
    def _validate_master_material(self, material, validation: Dict[str, any]):
        try:
            pass
            
        except Exception as e:
            logger.error(f"Error validating master material: {str(e)}")
    
    def _validate_material_instance(self, material_instance, validation: Dict[str, any]):
        try:
            if hasattr(material_instance, 'parent'):
                parent = material_instance.parent
                if parent:
                    validation["info"]["parent"] = parent.get_name()
                else:
                    validation["is_valid"] = False
                    validation["issues"].append("Material instance has no parent")
            
        except Exception as e:
            logger.error(f"Error validating material instance: {str(e)}")
    
    def check_unused_parameters(self, material) -> List[str]:
        unused_params = []
        
        try:
            pass
            
        except Exception as e:
            logger.error(f"Error checking unused parameters: {str(e)}")
        
        return unused_params
    
    def batch_validate_materials(self, root_path: str = "/Game/") -> Dict[str, any]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {
            "total_materials": 0,
            "valid_materials": 0,
            "invalid_materials": 0,
            "materials_with_warnings": 0,
            "issues": []
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    asset_class = asset.get_class().get_name()
                    if asset_class in ["Material", "MaterialInstanceConstant"]:
                        stats["total_materials"] += 1
                        
                        validation = self.validate_material(asset)
                        
                        if validation["is_valid"]:
                            stats["valid_materials"] += 1
                        else:
                            stats["invalid_materials"] += 1
                            stats["issues"].append(validation)
                        
                        if validation["warnings"]:
                            stats["materials_with_warnings"] += 1
                            
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
        
        logger.info(f"Material validation complete: {stats['valid_materials']}/{stats['total_materials']} valid")
        return stats
    
    def find_materials_without_instances(self, root_path: str = "/Game/") -> List[str]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        master_materials = []
        material_instances = []
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    asset_class = asset.get_class().get_name()
                    if asset_class == "Material":
                        master_materials.append(asset_path)
                    elif asset_class == "MaterialInstanceConstant":
                        if hasattr(asset, 'parent') and asset.parent:
                            parent_path = asset.parent.get_path_name()
                            material_instances.append(parent_path)
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
        
        unused_masters = [mat for mat in master_materials if mat not in material_instances]
        
        return unused_masters
