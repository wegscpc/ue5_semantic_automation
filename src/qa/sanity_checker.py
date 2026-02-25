import unreal
from typing import Dict, List, Tuple
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class SanityChecker:
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
        self.issues = []
    
    def run_full_sanity_check(self, root_path: str = "/Game/") -> Dict[str, any]:
        logger.info("Starting full sanity check...")
        
        self.issues = []
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {
            "total_assets": len(all_assets),
            "assets_checked": 0,
            "issues_found": 0,
            "critical_issues": 0,
            "warnings": 0,
            "issues_by_type": {}
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    asset_issues = self._check_single_asset(asset)
                    
                    if asset_issues:
                        self.issues.extend(asset_issues)
                        stats["issues_found"] += len(asset_issues)
                        
                        for issue in asset_issues:
                            severity = issue["severity"]
                            issue_type = issue["type"]
                            
                            if severity == "critical":
                                stats["critical_issues"] += 1
                            elif severity == "warning":
                                stats["warnings"] += 1
                            
                            if issue_type not in stats["issues_by_type"]:
                                stats["issues_by_type"][issue_type] = 0
                            stats["issues_by_type"][issue_type] += 1
                    
                    stats["assets_checked"] += 1
                    
            except Exception as e:
                logger.error(f"Error checking {asset_path}: {str(e)}")
        
        logger.info(f"Sanity check complete: {stats}")
        return stats
    
    def _check_single_asset(self, asset) -> List[Dict[str, any]]:
        issues = []
        asset_class = asset.get_class().get_name()
        
        if asset_class == "Texture2D":
            issues.extend(self._check_texture(asset))
        elif asset_class == "Material" or asset_class == "MaterialInstanceConstant":
            issues.extend(self._check_material(asset))
        elif asset_class == "StaticMesh":
            issues.extend(self._check_static_mesh(asset))
        elif asset_class == "SkeletalMesh":
            issues.extend(self._check_skeletal_mesh(asset))
        
        naming_issues = self._check_naming_convention(asset)
        if naming_issues:
            issues.extend(naming_issues)
        
        return issues
    
    def _check_texture(self, texture) -> List[Dict[str, any]]:
        issues = []
        
        try:
            width = texture.blueprint_get_size_x()
            height = texture.blueprint_get_size_y()
            
            if not self._is_power_of_two(width) or not self._is_power_of_two(height):
                issues.append({
                    "asset": texture.get_name(),
                    "path": texture.get_path_name(),
                    "type": "texture_dimensions",
                    "severity": "critical",
                    "message": f"Texture dimensions are not power of 2: {width}x{height}",
                    "suggestion": f"Resize to nearest power of 2"
                })
            
            if width > 4096 or height > 4096:
                issues.append({
                    "asset": texture.get_name(),
                    "path": texture.get_path_name(),
                    "type": "texture_size",
                    "severity": "warning",
                    "message": f"Texture is very large: {width}x{height}",
                    "suggestion": "Consider using lower resolution or texture streaming"
                })
            
        except Exception as e:
            logger.error(f"Error checking texture {texture.get_name()}: {str(e)}")
        
        return issues
    
    def _check_material(self, material) -> List[Dict[str, any]]:
        issues = []
        
        try:
            material_name = material.get_name()
            
            if "Material" in material.get_class().get_name():
                pass
            
        except Exception as e:
            logger.error(f"Error checking material {material.get_name()}: {str(e)}")
        
        return issues
    
    def _check_static_mesh(self, mesh) -> List[Dict[str, any]]:
        issues = []
        
        try:
            mesh_name = mesh.get_name()
            
            if hasattr(mesh, 'get_num_lods'):
                num_lods = mesh.get_num_lods()
                if num_lods < 2:
                    issues.append({
                        "asset": mesh_name,
                        "path": mesh.get_path_name(),
                        "type": "missing_lods",
                        "severity": "warning",
                        "message": "Static mesh has no LODs",
                        "suggestion": "Add LODs for better performance"
                    })
            
        except Exception as e:
            logger.error(f"Error checking static mesh {mesh.get_name()}: {str(e)}")
        
        return issues
    
    def _check_skeletal_mesh(self, mesh) -> List[Dict[str, any]]:
        issues = []
        
        try:
            mesh_name = mesh.get_name()
            
        except Exception as e:
            logger.error(f"Error checking skeletal mesh {mesh.get_name()}: {str(e)}")
        
        return issues
    
    def _check_naming_convention(self, asset) -> List[Dict[str, any]]:
        issues = []
        
        asset_name = asset.get_name()
        asset_class = asset.get_class().get_name()
        
        prefix_mapping = {
            "StaticMesh": "SM_",
            "SkeletalMesh": "SK_",
            "Texture2D": "T_",
            "Material": "M_",
            "MaterialInstanceConstant": "MI_",
            "BlueprintGeneratedClass": "BP_",
        }
        
        expected_prefix = prefix_mapping.get(asset_class)
        
        if expected_prefix and not asset_name.startswith(expected_prefix):
            issues.append({
                "asset": asset_name,
                "path": asset.get_path_name(),
                "type": "naming_convention",
                "severity": "warning",
                "message": f"Asset missing expected prefix: {expected_prefix}",
                "suggestion": f"Rename to {expected_prefix}{asset_name}"
            })
        
        return issues
    
    def _is_power_of_two(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
    
    def export_issues_report(self, output_path: str = "/Game/Reports/sanity_check_report.json") -> bool:
        try:
            import json
            
            report = {
                "total_issues": len(self.issues),
                "issues": self.issues
            }
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Exported sanity check report to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            return False
    
    def get_critical_issues(self) -> List[Dict[str, any]]:
        return [issue for issue in self.issues if issue["severity"] == "critical"]
    
    def get_issues_by_type(self, issue_type: str) -> List[Dict[str, any]]:
        return [issue for issue in self.issues if issue["type"] == issue_type]
