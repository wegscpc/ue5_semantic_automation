import unreal
from typing import Dict, List, Optional
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logger import setup_logger

logger = setup_logger(__name__)


class TextureValidator:
    
    RECOMMENDED_SIZES = {
        "ui": (512, 1024),
        "character": (2048, 4096),
        "environment": (1024, 2048),
        "prop": (512, 1024),
        "vfx": (256, 512)
    }
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
    
    def validate_texture(self, texture) -> Dict[str, any]:
        validation = {
            "asset": texture.get_name(),
            "path": texture.get_path_name(),
            "is_valid": True,
            "issues": [],
            "warnings": [],
            "info": {}
        }
        
        try:
            width = texture.blueprint_get_size_x()
            height = texture.blueprint_get_size_y()
            
            validation["info"]["width"] = width
            validation["info"]["height"] = height
            validation["info"]["aspect_ratio"] = width / height if height > 0 else 0
            
            if not self._is_power_of_two(width):
                validation["is_valid"] = False
                validation["issues"].append(f"Width {width} is not power of 2")
            
            if not self._is_power_of_two(height):
                validation["is_valid"] = False
                validation["issues"].append(f"Height {height} is not power of 2")
            
            if width > 8192 or height > 8192:
                validation["warnings"].append(f"Texture is extremely large: {width}x{height}")
            
            if width != height and width > 2 * height or height > 2 * width:
                validation["warnings"].append(f"Unusual aspect ratio: {width}x{height}")
            
            compression = self._get_texture_compression(texture)
            validation["info"]["compression"] = compression
            
            if compression == "TC_Default":
                validation["warnings"].append("Using default compression - consider optimizing")
            
        except Exception as e:
            logger.error(f"Error validating texture {texture.get_name()}: {str(e)}")
            validation["is_valid"] = False
            validation["issues"].append(f"Validation error: {str(e)}")
        
        return validation
    
    def _is_power_of_two(self, n: int) -> bool:
        return n > 0 and (n & (n - 1)) == 0
    
    def _get_texture_compression(self, texture) -> str:
        try:
            if hasattr(texture, 'compression_settings'):
                return str(texture.compression_settings)
            return "Unknown"
        except:
            return "Unknown"
    
    def suggest_optimal_size(self, texture, usage_context: str = "prop") -> Tuple[int, int]:
        try:
            width = texture.blueprint_get_size_x()
            height = texture.blueprint_get_size_y()
            
            min_size, max_size = self.RECOMMENDED_SIZES.get(usage_context, (512, 1024))
            
            optimal_width = self._nearest_power_of_two(width)
            optimal_height = self._nearest_power_of_two(height)
            
            optimal_width = max(min_size, min(optimal_width, max_size))
            optimal_height = max(min_size, min(optimal_height, max_size))
            
            return (optimal_width, optimal_height)
            
        except Exception as e:
            logger.error(f"Error suggesting size: {str(e)}")
            return (1024, 1024)
    
    def _nearest_power_of_two(self, n: int) -> int:
        if n <= 0:
            return 1
        
        import math
        power = math.log2(n)
        lower = 2 ** math.floor(power)
        upper = 2 ** math.ceil(power)
        
        if n - lower < upper - n:
            return int(lower)
        else:
            return int(upper)
    
    def batch_validate_textures(self, root_path: str = "/Game/") -> Dict[str, any]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {
            "total_textures": 0,
            "valid_textures": 0,
            "invalid_textures": 0,
            "textures_with_warnings": 0,
            "issues": []
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "Texture2D":
                    stats["total_textures"] += 1
                    
                    validation = self.validate_texture(asset)
                    
                    if validation["is_valid"]:
                        stats["valid_textures"] += 1
                    else:
                        stats["invalid_textures"] += 1
                        stats["issues"].append(validation)
                    
                    if validation["warnings"]:
                        stats["textures_with_warnings"] += 1
                        
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
        
        logger.info(f"Texture validation complete: {stats['valid_textures']}/{stats['total_textures']} valid")
        return stats
    
    def get_oversized_textures(self, root_path: str = "/Game/", max_size: int = 2048) -> List[str]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        oversized = []
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "Texture2D":
                    width = asset.blueprint_get_size_x()
                    height = asset.blueprint_get_size_y()
                    
                    if width > max_size or height > max_size:
                        oversized.append({
                            "path": asset_path,
                            "size": f"{width}x{height}"
                        })
            except Exception as e:
                logger.error(f"Error checking {asset_path}: {str(e)}")
        
        return oversized
