import os
import json
import logging
from typing import Optional, Dict, List
from enum import Enum

try:
    from ..utils.logger import setup_logger
    logger = setup_logger(__name__)
except ImportError:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    OPENAI = "openai"
    LOCAL = "local"
    ANTHROPIC = "anthropic"


class LLMClient:
    
    def __init__(self, provider: LLMProvider = LLMProvider.OPENAI, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.provider = provider
        
        # Try multiple environment variables for API key
        if api_key:
            self.api_key = api_key
        elif provider == LLMProvider.ANTHROPIC:
            self.api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        else:
            self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        
        self.model = model
        self.base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        
        if not self.api_key:
            logger.warning(f"{provider.value} API key not found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
    
    def generate_completion(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Optional[str]:
        try:
            if self.provider == LLMProvider.OPENAI:
                return self._openai_completion(prompt, max_tokens, temperature)
            elif self.provider == LLMProvider.ANTHROPIC:
                return self._anthropic_completion(prompt, max_tokens, temperature)
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
    
    def _anthropic_completion(self, prompt: str, max_tokens: int, temperature: float) -> Optional[str]:
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model=self.model if self.model.startswith("claude") else "claude-sonnet-4-6",
                max_tokens=max_tokens,
                temperature=temperature,
                system="You are an expert Unreal Engine 5 technical artist assistant.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return message.content[0].text.strip()
        except ImportError:
            logger.error("Anthropic library not installed. Install with: pip install anthropic")
            return None
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
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
        prompt = f"""Generate PBR material parameters for: "{description}"

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):
{{
    "base_color": [0.8, 0.1, 0.1],
    "metallic": 0.9,
    "roughness": 0.3,
    "specular": 0.5
}}

Values must be floats between 0 and 1. Return only the JSON."""
        
        response = self.generate_completion(prompt, max_tokens=200, temperature=0.3)
        
        if response:
            try:
                # Clean up response - remove markdown code blocks if present
                cleaned = response.strip()
                if cleaned.startswith('```'):
                    # Remove markdown code blocks
                    cleaned = cleaned.split('```')[1]
                    if cleaned.startswith('json'):
                        cleaned = cleaned[4:]
                    cleaned = cleaned.strip()
                
                return json.loads(cleaned)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse material parameters JSON: {e}")
                logger.error(f"Response was: {response}")
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
