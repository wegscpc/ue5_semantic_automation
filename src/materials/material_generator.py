import unreal
from typing import Dict, List, Optional
from ..ai.llm_client import LLMClient
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class MaterialGenerator:
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
        self.editor_asset_lib = unreal.EditorAssetLibrary
        self.material_editing_lib = unreal.MaterialEditingLibrary
    
    def generate_material_from_prompt(self, prompt: str, master_material_path: Optional[str] = None) -> Optional[str]:
        try:
            logger.info(f"Generating material from prompt: {prompt}")
            
            material_params = self.llm_client.generate_material_parameters(prompt)
            
            if not material_params:
                logger.error("Failed to generate material parameters from LLM")
                return None
            
            logger.info(f"Generated parameters: {material_params}")
            
            material_name = self._generate_material_name(prompt)
            
            if master_material_path:
                material_instance = self._create_material_instance(
                    master_material_path,
                    material_name,
                    material_params
                )
                
                if material_instance:
                    logger.info(f"Created material instance: {material_instance}")
                    return material_instance
            else:
                material = self._create_basic_material(material_name, material_params)
                
                if material:
                    logger.info(f"Created material: {material}")
                    return material
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating material: {str(e)}")
            return None
    
    def _generate_material_name(self, prompt: str) -> str:
        words = prompt.lower().split()[:3]
        name = "_".join(words)
        name = "".join(c if c.isalnum() or c == "_" else "" for c in name)
        return f"MI_{name}"
    
    def _create_material_instance(self, master_material_path: str, instance_name: str, params: Dict[str, any]) -> Optional[str]:
        try:
            if not self.editor_asset_lib.does_asset_exist(master_material_path):
                logger.error(f"Master material not found: {master_material_path}")
                return None
            
            master_material = self.editor_asset_lib.load_asset(master_material_path)
            
            instance_path = f"/Game/Materials/Instances/{instance_name}"
            
            if self.editor_asset_lib.does_asset_exist(instance_path):
                logger.warning(f"Material instance already exists: {instance_path}")
                instance_path = f"{instance_path}_01"
            
            factory = unreal.MaterialInstanceConstantFactoryNew()
            factory.initial_parent = master_material
            
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            material_instance = asset_tools.create_asset(
                instance_name,
                "/Game/Materials/Instances",
                unreal.MaterialInstanceConstant,
                factory
            )
            
            if material_instance:
                self._apply_parameters_to_instance(material_instance, params)
                
                self.editor_asset_lib.save_asset(material_instance.get_path_name())
                
                return material_instance.get_path_name()
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating material instance: {str(e)}")
            return None
    
    def _create_basic_material(self, material_name: str, params: Dict[str, any]) -> Optional[str]:
        try:
            material_path = f"/Game/Materials/{material_name}"
            
            if self.editor_asset_lib.does_asset_exist(material_path):
                logger.warning(f"Material already exists: {material_path}")
                material_path = f"{material_path}_01"
            
            factory = unreal.MaterialFactoryNew()
            
            asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
            material = asset_tools.create_asset(
                material_name,
                "/Game/Materials",
                unreal.Material,
                factory
            )
            
            if material:
                logger.info(f"Created basic material: {material_name}")
                
                self.editor_asset_lib.save_asset(material.get_path_name())
                
                return material.get_path_name()
            
            return None
            
        except Exception as e:
            logger.error(f"Error creating basic material: {str(e)}")
            return None
    
    def _apply_parameters_to_instance(self, material_instance, params: Dict[str, any]):
        try:
            if "base_color" in params:
                base_color = params["base_color"]
                if isinstance(base_color, list) and len(base_color) == 3:
                    color = unreal.LinearColor(base_color[0], base_color[1], base_color[2])
                    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
                        material_instance,
                        "BaseColor",
                        color
                    )
            
            scalar_params = {
                "metallic": "Metallic",
                "roughness": "Roughness",
                "specular": "Specular",
                "normal_strength": "NormalStrength"
            }
            
            for param_key, param_name in scalar_params.items():
                if param_key in params:
                    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(
                        material_instance,
                        param_name,
                        float(params[param_key])
                    )
            
            if "emissive" in params:
                emissive = params["emissive"]
                if isinstance(emissive, list) and len(emissive) == 3:
                    color = unreal.LinearColor(emissive[0], emissive[1], emissive[2])
                    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(
                        material_instance,
                        "EmissiveColor",
                        color
                    )
            
            logger.info(f"Applied parameters to material instance")
            
        except Exception as e:
            logger.error(f"Error applying parameters: {str(e)}")
    
    def batch_generate_materials(self, prompts: List[str], master_material_path: Optional[str] = None) -> Dict[str, any]:
        stats = {
            "total_prompts": len(prompts),
            "materials_created": 0,
            "errors": 0,
            "created_materials": []
        }
        
        for prompt in prompts:
            try:
                material_path = self.generate_material_from_prompt(prompt, master_material_path)
                
                if material_path:
                    stats["materials_created"] += 1
                    stats["created_materials"].append(material_path)
                else:
                    stats["errors"] += 1
                    
            except Exception as e:
                logger.error(f"Error processing prompt '{prompt}': {str(e)}")
                stats["errors"] += 1
        
        logger.info(f"Batch material generation complete: {stats}")
        return stats
    
    def suggest_textures_for_material(self, material_description: str) -> List[str]:
        try:
            material_params = self.llm_client.generate_material_parameters(material_description)
            
            if material_params and "suggested_textures" in material_params:
                return material_params["suggested_textures"]
            
            return []
            
        except Exception as e:
            logger.error(f"Error suggesting textures: {str(e)}")
            return []
