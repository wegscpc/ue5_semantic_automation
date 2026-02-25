"""
Basic usage examples for UE5 Semantic Asset Organizer
"""

import unreal
import sys

sys.path.append('path/to/ue5_semantic_automation/src')

from main import UE5AutomationTool


def example_organize_assets():
    """Example: Organize selected assets"""
    tool = UE5AutomationTool()
    
    stats = tool.organize_selected_assets()
    
    print(f"✓ Organized {stats['renamed']} assets")
    print(f"✗ {stats['errors']} errors")


def example_quality_check():
    """Example: Run quality assurance check"""
    tool = UE5AutomationTool()
    
    stats = tool.run_sanity_check()
    
    print(f"Total assets checked: {stats['assets_checked']}")
    print(f"Issues found: {stats['issues_found']}")
    print(f"Critical issues: {stats['critical_issues']}")
    
    critical = tool.sanity_checker.get_critical_issues()
    for issue in critical:
        print(f"  ⚠️ {issue['asset']}: {issue['message']}")


def example_optimize_textures():
    """Example: Optimize textures for performance"""
    tool = UE5AutomationTool()
    
    report = tool.texture_optimizer.generate_optimization_report()
    
    print(f"Total texture memory: {report['total_memory_mb']} MB")
    print(f"Potential savings: {report['potential_savings_mb']} MB")
    
    tool.optimize_textures(viewing_distance="medium")


def example_generate_material():
    """Example: Generate material from description"""
    tool = UE5AutomationTool()
    
    descriptions = [
        "wet stone with moss",
        "shiny metal with scratches",
        "old weathered wood"
    ]
    
    for desc in descriptions:
        material = tool.generate_material_from_description(desc)
        print(f"Created: {material}")


def example_ai_naming():
    """Example: Use AI to rename unclear assets"""
    tool = UE5AutomationTool()
    
    stats = tool.auto_name_unclear_assets()
    
    print(f"Analyzed: {stats['analyzed']} assets")
    print(f"Renamed: {stats['renamed']} assets")
    print(f"Skipped: {stats['skipped']} assets")


if __name__ == "__main__":
    print("UE5 Semantic Asset Organizer - Examples")
    print("=" * 50)
    
    print("\n1. Organize Assets")
    example_organize_assets()
    
    print("\n2. Quality Check")
    example_quality_check()
    
    print("\n3. Optimize Textures")
    example_optimize_textures()
    
    print("\n4. Generate Materials")
    example_generate_material()
    
    print("\n5. AI Naming")
    example_ai_naming()
