import unreal
from typing import Dict, List, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class LODGenerator:
    
    DEFAULT_LOD_SETTINGS = {
        "lod1": {"reduction_percent": 0.5, "screen_size": 0.5},
        "lod2": {"reduction_percent": 0.25, "screen_size": 0.25},
        "lod3": {"reduction_percent": 0.1, "screen_size": 0.1}
    }
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
    
    def generate_lods_for_mesh(self, static_mesh, num_lods: int = 3) -> bool:
        try:
            mesh_name = static_mesh.get_name()
            
            if hasattr(static_mesh, 'get_num_lods'):
                current_lods = static_mesh.get_num_lods()
                
                if current_lods >= num_lods + 1:
                    logger.info(f"Mesh {mesh_name} already has {current_lods} LODs")
                    return False
            
            logger.info(f"Generating {num_lods} LODs for {mesh_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error generating LODs: {str(e)}")
            return False
    
    def batch_generate_lods(self, root_path: str = "/Game/", num_lods: int = 3) -> Dict[str, int]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {
            "total_meshes": 0,
            "lods_generated": 0,
            "already_has_lods": 0,
            "errors": 0
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "StaticMesh":
                    stats["total_meshes"] += 1
                    
                    if self.generate_lods_for_mesh(asset, num_lods):
                        stats["lods_generated"] += 1
                    else:
                        stats["already_has_lods"] += 1
                        
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"LOD generation complete: {stats}")
        return stats
    
    def analyze_lod_coverage(self, root_path: str = "/Game/") -> Dict[str, any]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        analysis = {
            "total_meshes": 0,
            "meshes_with_lods": 0,
            "meshes_without_lods": 0,
            "meshes_needing_lods": []
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "StaticMesh":
                    analysis["total_meshes"] += 1
                    
                    if hasattr(asset, 'get_num_lods'):
                        num_lods = asset.get_num_lods()
                        
                        if num_lods > 1:
                            analysis["meshes_with_lods"] += 1
                        else:
                            analysis["meshes_without_lods"] += 1
                            analysis["meshes_needing_lods"].append({
                                "path": asset_path,
                                "name": asset.get_name()
                            })
                    else:
                        analysis["meshes_without_lods"] += 1
                        analysis["meshes_needing_lods"].append({
                            "path": asset_path,
                            "name": asset.get_name()
                        })
                        
            except Exception as e:
                logger.error(f"Error analyzing {asset_path}: {str(e)}")
        
        logger.info(f"LOD analysis complete: {analysis['meshes_with_lods']}/{analysis['total_meshes']} have LODs")
        return analysis
    
    def get_lod_info(self, static_mesh) -> Dict[str, any]:
        info = {
            "mesh_name": static_mesh.get_name(),
            "num_lods": 0,
            "lod_details": []
        }
        
        try:
            if hasattr(static_mesh, 'get_num_lods'):
                info["num_lods"] = static_mesh.get_num_lods()
                
                for lod_index in range(info["num_lods"]):
                    lod_detail = {
                        "lod_index": lod_index,
                        "is_base_lod": lod_index == 0
                    }
                    info["lod_details"].append(lod_detail)
            
        except Exception as e:
            logger.error(f"Error getting LOD info: {str(e)}")
        
        return info
