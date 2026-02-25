import unreal
from typing import Dict, List, Optional
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.llm_client import LLMClient, LLMProvider
from utils.logger import setup_logger

logger = setup_logger(__name__)


class MetadataGenerator:
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
        self.editor_asset_lib = unreal.EditorAssetLibrary
    
    def generate_asset_tags(self, asset) -> List[str]:
        asset_name = asset.get_name()
        asset_class = asset.get_class().get_name()
        
        tags = []
        
        tags.append(asset_class)
        
        name_lower = asset_name.lower()
        
        if any(keyword in name_lower for keyword in ['rock', 'stone', 'boulder']):
            tags.extend(['environment', 'natural', 'rock'])
        elif any(keyword in name_lower for keyword in ['wood', 'plank', 'timber']):
            tags.extend(['environment', 'natural', 'wood'])
        elif any(keyword in name_lower for keyword in ['metal', 'steel', 'iron']):
            tags.extend(['material', 'metal', 'industrial'])
        elif any(keyword in name_lower for keyword in ['grass', 'foliage', 'plant', 'tree']):
            tags.extend(['environment', 'natural', 'vegetation'])
        elif any(keyword in name_lower for keyword in ['wall', 'floor', 'ceiling']):
            tags.extend(['architecture', 'structural'])
        elif any(keyword in name_lower for keyword in ['character', 'player', 'npc']):
            tags.extend(['character', 'animated'])
        elif any(keyword in name_lower for keyword in ['ui', 'hud', 'menu']):
            tags.extend(['ui', 'interface'])
        elif any(keyword in name_lower for keyword in ['fx', 'particle', 'effect']):
            tags.extend(['vfx', 'effects'])
        
        return list(set(tags))
    
    def generate_ai_description(self, asset) -> Optional[str]:
        asset_metadata = {
            'name': asset.get_name(),
            'class': asset.get_class().get_name(),
            'path': asset.get_path_name()
        }
        
        prompt = f"""
        Generate a concise description (max 50 words) for this Unreal Engine asset:
        
        Name: {asset_metadata['name']}
        Type: {asset_metadata['class']}
        
        Focus on what the asset is and its potential use in a game project.
        """
        
        description = self.llm_client.generate_completion(prompt, max_tokens=100, temperature=0.6)
        
        if description:
            logger.info(f"Generated description for {asset_metadata['name']}")
        
        return description
    
    def apply_metadata_to_asset(self, asset, tags: List[str], description: Optional[str] = None) -> bool:
        try:
            asset_path = asset.get_path_name()
            
            metadata_object = unreal.EditorAssetLibrary.get_metadata_tag(asset, "Tags")
            
            tag_string = ", ".join(tags)
            unreal.EditorAssetLibrary.set_metadata_tag(asset, "Tags", tag_string)
            
            if description:
                unreal.EditorAssetLibrary.set_metadata_tag(asset, "Description", description)
            
            logger.info(f"Applied metadata to {asset.get_name()}: {len(tags)} tags")
            return True
            
        except Exception as e:
            logger.error(f"Error applying metadata: {str(e)}")
            return False
    
    def batch_generate_metadata(self, asset_paths: List[str]) -> Dict[str, int]:
        stats = {"processed": 0, "tagged": 0, "errors": 0}
        
        for asset_path in asset_paths:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    tags = self.generate_asset_tags(asset)
                    
                    if self.apply_metadata_to_asset(asset, tags):
                        stats["tagged"] += 1
                    
                    stats["processed"] += 1
            except Exception as e:
                logger.error(f"Error processing {asset_path}: {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"Metadata generation complete: {stats}")
        return stats
    
    def search_assets_by_metadata(self, search_tags: List[str]) -> List[str]:
        all_assets = self.editor_asset_lib.list_assets("/Game/", recursive=True)
        matching_assets = []
        
        for asset_path in all_assets:
            try:
                asset = self.editor_asset_lib.load_asset(asset_path)
                if asset:
                    asset_tags_str = unreal.EditorAssetLibrary.get_metadata_tag(asset, "Tags")
                    if asset_tags_str:
                        asset_tags = [tag.strip() for tag in asset_tags_str.split(",")]
                        if any(tag in asset_tags for tag in search_tags):
                            matching_assets.append(asset_path)
            except Exception as e:
                logger.error(f"Error searching {asset_path}: {str(e)}")
        
        return matching_assets
