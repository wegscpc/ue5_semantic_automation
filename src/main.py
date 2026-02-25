"""
Main entry point for UE5 Semantic Asset Organizer & AI Material Generator
This script can be run directly from Unreal Engine's Python console or as a scripted action
"""

import unreal
from typing import List, Optional
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.asset_organizer import AssetOrganizer
from ai.asset_naming import AIAssetNaming
from qa.sanity_checker import SanityChecker
from optimization.texture_optimizer import TextureOptimizer
from materials.material_generator import MaterialGenerator
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class UE5AutomationTool:
    
    def __init__(self):
        self.config = Config()
        self.organizer = AssetOrganizer()
        self.ai_naming = AIAssetNaming()
        self.sanity_checker = SanityChecker()
        self.texture_optimizer = TextureOptimizer()
        self.material_generator = MaterialGenerator()
        
        logger.info("UE5 Automation Tool initialized")
    
    def organize_selected_assets(self):
        logger.info("Organizing selected assets...")
        stats = self.organizer.organize_selected_assets()
        UnrealHelpers.show_notification(
            f"Organization complete: {stats['renamed']} assets organized, {stats['errors']} errors"
        )
        return stats
    
    def run_sanity_check(self, root_path: str = "/Game/"):
        logger.info("Running sanity check...")
        stats = self.sanity_checker.run_full_sanity_check(root_path)
        UnrealHelpers.show_notification(
            f"Sanity check complete: {stats['issues_found']} issues found ({stats['critical_issues']} critical)"
        )
        return stats
    
    def optimize_textures(self, viewing_distance: str = "medium"):
        logger.info("Optimizing textures...")
        stats = self.texture_optimizer.batch_optimize_textures(viewing_distance=viewing_distance)
        UnrealHelpers.show_notification(
            f"Texture optimization complete: {stats['optimized']} textures optimized"
        )
        return stats
    
    def generate_material_from_description(self, description: str):
        logger.info(f"Generating material: {description}")
        
        master_material = self.master_material_manager.recommend_master_material(description)
        
        material_path = self.material_generator.generate_material_from_prompt(
            description,
            master_material
        )
        
        if material_path:
            UnrealHelpers.show_notification(f"Material created: {material_path}")
        else:
            UnrealHelpers.show_notification("Failed to create material")
        
        return material_path
    
    def auto_name_unclear_assets(self):
        logger.info("Running AI asset naming...")
        stats = self.ai_naming.batch_rename_unclear_assets()
        UnrealHelpers.show_notification(
            f"AI naming complete: {stats['renamed']} assets renamed"
        )
        return stats
    
    def generate_metadata_for_assets(self, root_path: str = "/Game/"):
        logger.info("Generating metadata...")
        asset_paths = UnrealHelpers.list_assets(root_path, recursive=True)
        stats = self.metadata_gen.batch_generate_metadata(asset_paths)
        UnrealHelpers.show_notification(
            f"Metadata generation complete: {stats['tagged']} assets tagged"
        )
        return stats


def organize_assets():
    tool = UE5AutomationTool()
    return tool.organize_selected_assets()


def run_sanity_check():
    tool = UE5AutomationTool()
    return tool.run_sanity_check()


def optimize_textures():
    tool = UE5AutomationTool()
    return tool.optimize_textures()


def generate_material(description: str):
    tool = UE5AutomationTool()
    return tool.generate_material_from_description(description)


if __name__ == "__main__":
    logger.info("UE5 Semantic Asset Organizer & AI Material Generator")
    logger.info("Run specific functions from Unreal Engine Python console:")
    logger.info("  - organize_assets()")
    logger.info("  - run_sanity_check()")
    logger.info("  - optimize_textures()")
    logger.info("  - generate_material('wet stone with moss')")
