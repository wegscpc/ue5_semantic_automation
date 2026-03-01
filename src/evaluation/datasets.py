"""
Test Datasets for LLM Evaluation

This module contains test cases for evaluating AI features.
"""

from typing import Dict, List


class EvaluationDataset:
    """Test datasets for LLM evaluation"""
    
    # ==================== Asset Naming Tests ====================
    
    ASSET_NAMING_TESTS = [
        {
            'input': {
                'name': 'cube_01',
                'type': 'StaticMesh'
            },
            'expected': {
                'name': 'SM_Cube_01'
            },
            'description': 'Basic static mesh naming - should add SM_ prefix'
        },
        {
            'input': {
                'name': 'metal_texture',
                'type': 'Texture2D'
            },
            'expected': {
                'name': 'T_Metal'
            },
            'description': 'Texture naming convention - should add T_ prefix'
        },
        {
            'input': {
                'name': 'shiny_material',
                'type': 'Material'
            },
            'expected': {
                'name': 'M_Shiny'
            },
            'description': 'Material naming convention - should add M_ prefix'
        },
        {
            'input': {
                'name': 'player_blueprint',
                'type': 'Blueprint'
            },
            'expected': {
                'name': 'BP_Player'
            },
            'description': 'Blueprint naming convention - should add BP_ prefix'
        },
        {
            'input': {
                'name': 'M_Glow',
                'type': 'Material'
            },
            'expected': {
                'name': 'M_Glow'
            },
            'description': 'Already well-named material - should keep as is'
        }
    ]
    
    # ==================== Material Generation Tests ====================
    
    MATERIAL_GENERATION_TESTS = [
        {
            'input': {
                'prompt': 'shiny red metal'
            },
            'expected': {
                'BaseColor': [0.6, 0.1, 0.1],  # Reddish
                'Metallic': 0.9,  # High metallic
                'Roughness': 0.2,  # Low roughness (shiny)
                'Specular': 0.5
            },
            'description': 'Metallic material with color - high metallic, low roughness',
            'tolerance': 0.3  # Allow 30% deviation from expected values
        },
        {
            'input': {
                'prompt': 'rough concrete'
            },
            'expected': {
                'BaseColor': [0.5, 0.5, 0.5],  # Gray
                'Metallic': 0.0,  # Non-metallic
                'Roughness': 0.9,  # High roughness
                'Specular': 0.5
            },
            'description': 'Non-metallic rough surface - zero metallic, high roughness',
            'tolerance': 0.3
        },
        {
            'input': {
                'prompt': 'glossy blue plastic'
            },
            'expected': {
                'BaseColor': [0.1, 0.3, 0.9],  # Blue
                'Metallic': 0.0,  # Non-metallic
                'Roughness': 0.1,  # Low roughness (glossy)
                'Specular': 0.5
            },
            'description': 'Plastic material - non-metallic, low roughness',
            'tolerance': 0.3
        },
        {
            'input': {
                'prompt': 'rusty iron'
            },
            'expected': {
                'BaseColor': [0.4, 0.2, 0.1],  # Brownish-red
                'Metallic': 0.7,  # Partially metallic (rust reduces it)
                'Roughness': 0.7,  # Rough surface
                'Specular': 0.5
            },
            'description': 'Weathered metal - medium metallic, high roughness',
            'tolerance': 0.3
        },
        {
            'input': {
                'prompt': 'polished gold'
            },
            'expected': {
                'BaseColor': [1.0, 0.84, 0.0],  # Gold color
                'Metallic': 1.0,  # Fully metallic
                'Roughness': 0.05,  # Very smooth (polished)
                'Specular': 0.5
            },
            'description': 'Precious metal - full metallic, very low roughness',
            'tolerance': 0.3
        }
    ]
    
    # ==================== Metadata Generation Tests ====================
    
    METADATA_GENERATION_TESTS = [
        {
            'input': {
                'name': 'SM_Chair',
                'type': 'StaticMesh'
            },
            'expected': {
                'description': 'Static mesh of a chair for furniture placement',
                'tags': ['furniture', 'chair', 'prop', 'StaticMesh']
            },
            'description': 'Furniture asset metadata - should identify as furniture'
        },
        {
            'input': {
                'name': 'T_Brick_D',
                'type': 'Texture2D'
            },
            'expected': {
                'description': 'Diffuse texture for brick material',
                'tags': ['texture', 'brick', 'material', 'Texture2D']
            },
            'description': 'Texture metadata - should identify texture type and material'
        },
        {
            'input': {
                'name': 'M_Metal_Rusty',
                'type': 'Material'
            },
            'expected': {
                'description': 'Material for rusty metal surfaces',
                'tags': ['material', 'metal', 'rusty', 'Material']
            },
            'description': 'Material metadata - should identify material properties'
        },
        {
            'input': {
                'name': 'SM_Tree_Oak',
                'type': 'StaticMesh'
            },
            'expected': {
                'description': 'Static mesh of an oak tree for environment decoration',
                'tags': ['environment', 'natural', 'vegetation', 'tree', 'StaticMesh']
            },
            'description': 'Environment asset - should identify as vegetation'
        }
    ]
    
    # ==================== Helper Methods ====================
    
    @classmethod
    def get_all_tests(cls) -> Dict[str, List[Dict]]:
        """Get all test datasets"""
        return {
            'asset_naming': cls.ASSET_NAMING_TESTS,
            'material_generation': cls.MATERIAL_GENERATION_TESTS,
            'metadata_generation': cls.METADATA_GENERATION_TESTS
        }
    
    @classmethod
    def get_test_count(cls) -> Dict[str, int]:
        """Get count of tests per feature"""
        return {
            'asset_naming': len(cls.ASSET_NAMING_TESTS),
            'material_generation': len(cls.MATERIAL_GENERATION_TESTS),
            'metadata_generation': len(cls.METADATA_GENERATION_TESTS),
            'total': len(cls.ASSET_NAMING_TESTS) + len(cls.MATERIAL_GENERATION_TESTS) + len(cls.METADATA_GENERATION_TESTS)
        }
