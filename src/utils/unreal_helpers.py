import unreal
from typing import List, Dict, Optional, Any
from .logger import setup_logger

logger = setup_logger(__name__)


class UnrealHelpers:
    
    @staticmethod
    def get_selected_assets() -> List[Any]:
        try:
            return unreal.EditorUtilityLibrary.get_selected_assets()
        except Exception as e:
            logger.error(f"Error getting selected assets: {e}")
            return []
    
    @staticmethod
    def get_selected_asset_paths() -> List[str]:
        assets = UnrealHelpers.get_selected_assets()
        return [asset.get_path_name() for asset in assets]
    
    @staticmethod
    def load_asset(asset_path: str) -> Optional[Any]:
        try:
            return unreal.EditorAssetLibrary.load_asset(asset_path)
        except Exception as e:
            logger.error(f"Error loading asset {asset_path}: {e}")
            return None
    
    @staticmethod
    def save_asset(asset_path: str) -> bool:
        try:
            return unreal.EditorAssetLibrary.save_asset(asset_path)
        except Exception as e:
            logger.error(f"Error saving asset {asset_path}: {e}")
            return False
    
    @staticmethod
    def delete_asset(asset_path: str) -> bool:
        try:
            return unreal.EditorAssetLibrary.delete_asset(asset_path)
        except Exception as e:
            logger.error(f"Error deleting asset {asset_path}: {e}")
            return False
    
    @staticmethod
    def rename_asset(old_path: str, new_path: str) -> bool:
        try:
            return unreal.EditorAssetLibrary.rename_asset(old_path, new_path)
        except Exception as e:
            logger.error(f"Error renaming asset {old_path} to {new_path}: {e}")
            return False
    
    @staticmethod
    def duplicate_asset(source_path: str, destination_path: str) -> Optional[Any]:
        try:
            return unreal.EditorAssetLibrary.duplicate_asset(source_path, destination_path)
        except Exception as e:
            logger.error(f"Error duplicating asset {source_path}: {e}")
            return None
    
    @staticmethod
    def does_asset_exist(asset_path: str) -> bool:
        try:
            return unreal.EditorAssetLibrary.does_asset_exist(asset_path)
        except Exception as e:
            logger.error(f"Error checking asset existence {asset_path}: {e}")
            return False
    
    @staticmethod
    def list_assets(directory_path: str, recursive: bool = True) -> List[str]:
        try:
            return unreal.EditorAssetLibrary.list_assets(directory_path, recursive=recursive)
        except Exception as e:
            logger.error(f"Error listing assets in {directory_path}: {e}")
            return []
    
    @staticmethod
    def make_directory(directory_path: str) -> bool:
        try:
            return unreal.EditorAssetLibrary.make_directory(directory_path)
        except Exception as e:
            logger.error(f"Error creating directory {directory_path}: {e}")
            return False
    
    @staticmethod
    def does_directory_exist(directory_path: str) -> bool:
        try:
            return unreal.EditorAssetLibrary.does_directory_exist(directory_path)
        except Exception as e:
            logger.error(f"Error checking directory existence {directory_path}: {e}")
            return False
    
    @staticmethod
    def get_asset_class_name(asset) -> str:
        try:
            return asset.get_class().get_name()
        except Exception as e:
            logger.error(f"Error getting asset class name: {e}")
            return "Unknown"
    
    @staticmethod
    def show_notification(text: str, duration: float = 3.0):
        try:
            unreal.EditorDialog.show_message(
                "UE5 Automation",
                text,
                unreal.AppMsgType.OK
            )
        except Exception as e:
            logger.error(f"Error showing notification: {e}")
    
    @staticmethod
    def get_content_browser_path() -> str:
        try:
            selected_paths = unreal.EditorUtilityLibrary.get_selected_folder_paths()
            if selected_paths:
                return selected_paths[0]
            return "/Game/"
        except Exception as e:
            logger.error(f"Error getting content browser path: {e}")
            return "/Game/"
    
    @staticmethod
    def consolidate_assets(asset_to_consolidate_to: str, assets_to_consolidate: List[str]) -> bool:
        try:
            unreal.EditorAssetLibrary.consolidate_assets(
                asset_to_consolidate_to,
                assets_to_consolidate
            )
            return True
        except Exception as e:
            logger.error(f"Error consolidating assets: {e}")
            return False
    
    @staticmethod
    def get_metadata_tag(asset, tag_name: str) -> Optional[str]:
        try:
            return unreal.EditorAssetLibrary.get_metadata_tag(asset, tag_name)
        except Exception as e:
            logger.error(f"Error getting metadata tag {tag_name}: {e}")
            return None
    
    @staticmethod
    def set_metadata_tag(asset, tag_name: str, tag_value: str) -> bool:
        try:
            unreal.EditorAssetLibrary.set_metadata_tag(asset, tag_name, tag_value)
            return True
        except Exception as e:
            logger.error(f"Error setting metadata tag {tag_name}: {e}")
            return False
