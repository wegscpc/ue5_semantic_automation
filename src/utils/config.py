import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class Config:
    
    DEFAULT_CONFIG = {
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "api_key": "",
            "base_url": "https://api.openai.com/v1",
            "temperature": 0.7,
            "max_tokens": 500
        },
        "organization": {
            "base_path": "/Game/Content",
            "auto_organize": True,
            "create_folders": True,
            "backup_before_rename": False
        },
        "optimization": {
            "default_viewing_distance": "medium",
            "max_texture_resolution": 2048,
            "enable_texture_streaming": True,
            "auto_generate_lods": False,
            "num_lods": 3
        },
        "qa": {
            "run_on_import": False,
            "enforce_power_of_two": True,
            "enforce_naming_convention": True,
            "max_texture_size_warning": 4096
        },
        "materials": {
            "default_master_material": "/Game/Materials/Masters/M_StandardPBR",
            "auto_assign_textures": False,
            "material_output_path": "/Game/Materials/Generated"
        },
        "logging": {
            "level": "INFO",
            "log_to_file": True,
            "log_file_path": "ue5_automation.log"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        project_root = Path(__file__).parent.parent.parent
        return str(project_root / "config" / "settings.json")
    
    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    return self._merge_configs(self.DEFAULT_CONFIG, user_config)
            except Exception as e:
                print(f"Error loading config from {self.config_path}: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        merged = default.copy()
        for key, value in user.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged
    
    def save_config(self) -> bool:
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            
            print(f"Config saved to {self.config_path}")
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> bool:
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        return True
    
    def reset_to_defaults(self):
        self.config = self.DEFAULT_CONFIG.copy()
    
    def get_llm_config(self) -> Dict[str, Any]:
        return self.config.get("llm", {})
    
    def get_organization_config(self) -> Dict[str, Any]:
        return self.config.get("organization", {})
    
    def get_optimization_config(self) -> Dict[str, Any]:
        return self.config.get("optimization", {})
    
    def get_qa_config(self) -> Dict[str, Any]:
        return self.config.get("qa", {})
    
    def get_materials_config(self) -> Dict[str, Any]:
        return self.config.get("materials", {})
