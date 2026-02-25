"""
Unit tests for AssetOrganizer
"""

import pytest
from unittest.mock import Mock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.asset_organizer import AssetOrganizer


class TestAssetOrganizer:
    
    @pytest.fixture
    def organizer(self):
        with patch('core.asset_organizer.unreal'):
            return AssetOrganizer()
    
    def test_asset_prefix_mapping(self, organizer):
        assert "StaticMesh" in organizer.ASSET_PREFIX_MAPPING
        assert organizer.ASSET_PREFIX_MAPPING["StaticMesh"] == "SM_"
        assert organizer.ASSET_PREFIX_MAPPING["Texture2D"] == "T_"
        assert organizer.ASSET_PREFIX_MAPPING["Material"] == "M_"
    
    def test_folder_structure(self, organizer):
        assert "SM_" in organizer.FOLDER_STRUCTURE
        assert organizer.FOLDER_STRUCTURE["SM_"] == "Meshes/StaticMeshes"
        assert organizer.FOLDER_STRUCTURE["T_"] == "Textures"
    
    def test_get_target_folder(self, organizer):
        folder = organizer._get_target_folder("SM_")
        assert folder == "/Game/Content/Meshes/StaticMeshes"
        
        folder = organizer._get_target_folder("T_")
        assert folder == "/Game/Content/Textures"


class TestAssetClassifier:
    
    @pytest.fixture
    def classifier(self):
        with patch('core.asset_classifier.unreal'):
            from core.asset_classifier import AssetClassifier
            return AssetClassifier()
    
    def test_classify_by_name(self, classifier):
        assert classifier.classify_asset_by_name("my_mesh") == "StaticMesh"
        assert classifier.classify_asset_by_name("texture_diffuse") == "Texture2D"
        assert classifier.classify_asset_by_name("M_Material") == "Material"
        assert classifier.classify_asset_by_name("BP_Character") == "BlueprintGeneratedClass"


if __name__ == "__main__":
    pytest.main([__file__])
