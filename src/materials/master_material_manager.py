import unreal
from typing import Dict, List, Optional
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

logger = setup_logger(__name__)


class MasterMaterialManager:
    
    COMMON_MASTER_MATERIALS = {
        "standard_pbr": "/Game/Materials/Masters/M_StandardPBR",
        "foliage": "/Game/Materials/Masters/M_Foliage",
        "water": "/Game/Materials/Masters/M_Water",
        "glass": "/Game/Materials/Masters/M_Glass",
        "emissive": "/Game/Materials/Masters/M_Emissive",
        "terrain": "/Game/Materials/Masters/M_Terrain"
    }
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
    
    def get_master_material(self, material_type: str) -> Optional[str]:
        material_path = self.COMMON_MASTER_MATERIALS.get(material_type)
        
        if material_path and self.editor_asset_lib.does_asset_exist(material_path):
            return material_path
        
        logger.warning(f"Master material not found for type: {material_type}")
        return None
    
    def list_available_master_materials(self, root_path: str = "/Game/Materials/Masters") -> List[str]:
        if not self.editor_asset_lib.does_directory_exist(root_path):
            logger.warning(f"Master materials directory not found: {root_path}")
            return []
        
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        master_materials = []
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "Material":
                    master_materials.append(asset_path)
            except Exception as e:
                logger.error(f"Error loading {asset_path}: {str(e)}")
        
        return master_materials
    
    def create_master_material_template(self, material_name: str, material_type: str = "standard_pbr") -> Optional[str]:
        try:
            material_path = f"/Game/Materials/Masters/{material_name}"
            
            if self.editor_asset_lib.does_asset_exist(material_path):
                logger.warning(f"Master material already exists: {material_path}")
                return material_path
            
            factory = unreal.MaterialFactoryNew()
            
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            material = asset_tools.create_asset(
                material_name,
                "/Game/Materials/Masters",
                unreal.Material,
                factory
            )
            
            if material:
                logger.info(f"Created master material template: {material_name}")
                
                self.editor_asset_lib.save_asset(material.get_path_name())
                
                return material.get_path_name()
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating master material: {str(e)}")
            return None
    
    def get_material_instances(self, master_material_path: str) -> List[str]:
        if not self.editor_asset_lib.does_asset_exist(master_material_path):
            logger.error(f"Master material not found: {master_material_path}")
            return []
        
        all_assets = self.editor_asset_lib.list_assets("/Game/", recursive=True)
        instances = []
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "MaterialInstanceConstant":
                    if hasattr(asset, 'parent') and asset.parent:
                        parent_path = asset.parent.get_path_name()
                        if parent_path == master_material_path:
                            instances.append(asset_path)
            except Exception as e:
                logger.error(f"Error checking {asset_path}: {str(e)}")
        
        logger.info(f"Found {len(instances)} instances of {master_material_path}")
        return instances
    
    def analyze_master_material_usage(self, root_path: str = "/Game/Materials/Masters") -> Dict[str, any]:
        master_materials = self.list_available_master_materials(root_path)
        
        analysis = {
            "total_master_materials": len(master_materials),
            "usage_stats": []
        }
        
        for master_path in master_materials:
            instances = self.get_material_instances(master_path)
            
            master_name = master_path.split('/')[-1]
            
            analysis["usage_stats"].append({
                "master_material": master_name,
                "path": master_path,
                "instance_count": len(instances),
                "instances": instances
            })
        
        logger.info(f"Master material usage analysis complete")
        return analysis
    
    def recommend_master_material(self, description: str) -> Optional[str]:
        description_lower = description.lower()
        
        if any(keyword in description_lower for keyword in ['water', 'liquid', 'ocean', 'river']):
            return self.get_master_material("water")
        elif any(keyword in description_lower for keyword in ['glass', 'transparent', 'window']):
            return self.get_master_material("glass")
        elif any(keyword in description_lower for keyword in ['foliage', 'leaf', 'plant', 'tree']):
            return self.get_master_material("foliage")
        elif any(keyword in description_lower for keyword in ['glow', 'light', 'emissive', 'neon']):
            return self.get_master_material("emissive")
        elif any(keyword in description_lower for keyword in ['terrain', 'ground', 'landscape']):
            return self.get_master_material("terrain")
        else:
            return self.get_master_material("standard_pbr")
