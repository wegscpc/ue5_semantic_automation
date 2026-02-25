import unreal
from typing import Dict, List, Optional, Tuple
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class TextureOptimizer:
    
    VIEWING_DISTANCE_THRESHOLDS = {
        "close": (0, 500),
        "medium": (500, 2000),
        "far": (2000, 10000),
        "very_far": (10000, float('inf'))
    }
    
    RECOMMENDED_RESOLUTION_BY_DISTANCE = {
        "close": 2048,
        "medium": 1024,
        "far": 512,
        "very_far": 256
    }
    
    COMPRESSION_SETTINGS = {
        "diffuse": unreal.TextureCompressionSettings.TC_DEFAULT,
        "normal": unreal.TextureCompressionSettings.TC_NORMALMAP,
        "mask": unreal.TextureCompressionSettings.TC_MASKS,
        "grayscale": unreal.TextureCompressionSettings.TC_GRAYSCALE,
        "hdr": unreal.TextureCompressionSettings.TC_HDR,
    }
    
    def __init__(self):
        self.editor_asset_lib = unreal.EditorAssetLibrary
        self.texture_factory = unreal.TextureFactory()
    
    def optimize_texture_for_distance(self, texture, viewing_distance: str = "medium") -> bool:
        try:
            current_width = texture.blueprint_get_size_x()
            current_height = texture.blueprint_get_size_y()
            
            target_resolution = self.RECOMMENDED_RESOLUTION_BY_DISTANCE.get(viewing_distance, 1024)
            
            if current_width > target_resolution or current_height > target_resolution:
                logger.info(f"Optimizing {texture.get_name()} from {current_width}x{current_height} to max {target_resolution}")
                
                scale_factor = target_resolution / max(current_width, current_height)
                new_width = int(current_width * scale_factor)
                new_height = int(current_height * scale_factor)
                
                new_width = self._nearest_power_of_two(new_width)
                new_height = self._nearest_power_of_two(new_height)
                
                logger.info(f"Suggested resize: {new_width}x{new_height}")
                
                return True
            else:
                logger.info(f"Texture {texture.get_name()} is already optimized for {viewing_distance} viewing")
                return False
                
        except Exception as e:
            logger.error(f"Error optimizing texture: {str(e)}")
            return False
    
    def apply_optimal_compression(self, texture, texture_type: str = "diffuse") -> bool:
        try:
            compression_setting = self.COMPRESSION_SETTINGS.get(texture_type, unreal.TextureCompressionSettings.TC_DEFAULT)
            
            if hasattr(texture, 'compression_settings'):
                current_compression = texture.compression_settings
                
                if current_compression != compression_setting:
                    texture.compression_settings = compression_setting
                    texture.modify(True)
                    
                    logger.info(f"Applied {texture_type} compression to {texture.get_name()}")
                    return True
                else:
                    logger.info(f"Texture {texture.get_name()} already has optimal compression")
                    return False
            
        except Exception as e:
            logger.error(f"Error applying compression: {str(e)}")
            return False
    
    def enable_texture_streaming(self, texture) -> bool:
        try:
            if hasattr(texture, 'never_stream'):
                if texture.never_stream:
                    texture.never_stream = False
                    texture.modify(True)
                    logger.info(f"Enabled streaming for {texture.get_name()}")
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error enabling streaming: {str(e)}")
            return False
    
    def batch_optimize_textures(self, root_path: str = "/Game/", viewing_distance: str = "medium") -> Dict[str, int]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        stats = {
            "total_textures": 0,
            "optimized": 0,
            "already_optimal": 0,
            "errors": 0
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "Texture2D":
                    stats["total_textures"] += 1
                    
                    if self.optimize_texture_for_distance(asset, viewing_distance):
                        stats["optimized"] += 1
                    else:
                        stats["already_optimal"] += 1
                        
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"Batch optimization complete: {stats}")
        return stats
    
    def detect_over_resolution_textures(self, root_path: str = "/Game/", max_resolution: int = 2048) -> List[Dict[str, any]]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        over_resolution = []
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "Texture2D":
                    width = asset.blueprint_get_size_x()
                    height = asset.blueprint_get_size_y()
                    
                    if width > max_resolution or height > max_resolution:
                        memory_estimate = self._estimate_texture_memory(width, height)
                        
                        over_resolution.append({
                            "path": asset_path,
                            "name": asset.get_name(),
                            "size": f"{width}x{height}",
                            "memory_mb": memory_estimate
                        })
            except Exception as e:
                logger.error(f"Error checking {asset_path}: {str(e)}")
        
        logger.info(f"Found {len(over_resolution)} over-resolution textures")
        return over_resolution
    
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
    
    def _estimate_texture_memory(self, width: int, height: int, bytes_per_pixel: int = 4) -> float:
        total_bytes = width * height * bytes_per_pixel
        
        mip_chain_multiplier = 1.33
        total_bytes *= mip_chain_multiplier
        
        memory_mb = total_bytes / (1024 * 1024)
        return round(memory_mb, 2)
    
    def generate_optimization_report(self, root_path: str = "/Game/") -> Dict[str, any]:
        all_assets = self.editor_asset_lib.list_assets(root_path, recursive=True)
        
        report = {
            "total_textures": 0,
            "total_memory_mb": 0,
            "potential_savings_mb": 0,
            "textures_by_size": {
                "small": 0,
                "medium": 0,
                "large": 0,
                "very_large": 0
            },
            "optimization_opportunities": []
        }
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset and asset.get_class().get_name() == "Texture2D":
                    report["total_textures"] += 1
                    
                    width = asset.blueprint_get_size_x()
                    height = asset.blueprint_get_size_y()
                    memory = self._estimate_texture_memory(width, height)
                    
                    report["total_memory_mb"] += memory
                    
                    if max(width, height) <= 512:
                        report["textures_by_size"]["small"] += 1
                    elif max(width, height) <= 1024:
                        report["textures_by_size"]["medium"] += 1
                    elif max(width, height) <= 2048:
                        report["textures_by_size"]["large"] += 1
                    else:
                        report["textures_by_size"]["very_large"] += 1
                        
                        optimized_memory = self._estimate_texture_memory(2048, 2048)
                        savings = memory - optimized_memory
                        
                        if savings > 0:
                            report["potential_savings_mb"] += savings
                            report["optimization_opportunities"].append({
                                "path": asset_path,
                                "current_size": f"{width}x{height}",
                                "current_memory_mb": memory,
                                "potential_savings_mb": savings
                            })
                    
            except Exception as e:
                logger.error(f"Error analyzing {asset_path}: {str(e)}")
        
        report["total_memory_mb"] = round(report["total_memory_mb"], 2)
        report["potential_savings_mb"] = round(report["potential_savings_mb"], 2)
        
        logger.info(f"Optimization report generated: {report['total_textures']} textures analyzed")
        return report
