import os
import json
from typing import Optional, Dict, List
from enum import Enum
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class LLMProvider(Enum):
    OPENAI = "openai"
    LOCAL = "local"
    ANTHROPIC = "anthropic"


class LLMClient:
    
    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.provider = provider
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        
        if self.provider == LLMProvider.OPENAI and not self.api_key:
            logger.warning("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
    
    def generate_completion(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Optional[str]:
        try:
            if self.provider == LLMProvider.OPENAI:
                return self._openai_completion(prompt, max_tokens, temperature)
            elif self.provider == LLMProvider.LOCAL:
                return self._local_completion(prompt, max_tokens, temperature)
            else:
                logger.error(f"Unsupported provider: {self.provider}")
                return None
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            return None
    
    def _openai_completion(self, prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
        try:
            import openai
            
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert Unreal Engine 5 technical artist assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            return None
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return None
    
    def _local_completion(self, prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
        try:
            import requests
            
            response = requests.post(
                f"{self.base_url}/completions",
                json={
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("choices", [{}])[0].get("text", "").strip()
            else:
                logger.error(f"Local LLM error: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Local LLM error: {str(e)}")
            return None
    
    def suggest_asset_name(self, asset_metadata: Dict[str, any]) -> Optional[str]:
        prompt = f"""
        Based on the following asset metadata, suggest a proper name following Unreal Engine naming conventions:
        
        Asset Class: {asset_metadata.get('class', 'Unknown')}
        Current Name: {asset_metadata.get('name', 'Unknown')}
        Path: {asset_metadata.get('path', 'Unknown')}
        
        Provide ONLY the suggested name with the appropriate prefix (SM_, T_, M_, etc.).
        Do not include any explanation, just the name.
        """
        
        return self.generate_completion(prompt, max_tokens=50, temperature=0.3)
    
    def generate_material_parameters(self, description: str) -> Optional[Dict[str, any]]:
        prompt = f"""
        Generate material parameters for Unreal Engine 5 based on this description:
        "{description}"
        
        Return a JSON object with the following structure:
        {{
            "base_color": [R, G, B] (0-1 range),
            "metallic": float (0-1),
            "roughness": float (0-1),
            "specular": float (0-1),
            "emissive": [R, G, B] (0-1 range),
            "normal_strength": float (0-1),
            "suggested_textures": ["texture_type1", "texture_type2"]
        }}
        
        Return ONLY valid JSON, no additional text.
        """
        
        response = self.generate_completion(prompt, max_tokens=300, temperature=0.5)
        
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                logger.error("Failed to parse material parameters JSON")
                return None
        
        return None
    
    def analyze_asset_context(self, asset_name: str, nearby_assets: List[str]) -> Optional[str]:
        prompt = f"""
        Analyze this asset in context:
        
        Asset: {asset_name}
        Nearby assets: {', '.join(nearby_assets[:10])}
        
        Suggest:
        1. What category this asset belongs to
        2. Recommended folder location
        3. Any naming improvements
        
        Be concise and specific.
        """
        
        return self.generate_completion(prompt, max_tokens=200, temperature=0.4)
