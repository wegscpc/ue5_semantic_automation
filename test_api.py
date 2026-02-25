import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ai.llm_client import LLMClient, LLMProvider

# This will use your environment variable
client = LLMClient(provider=LLMProvider.ANTHROPIC)

print(f"API key loaded: {client.api_key[:15]}...")
print(f"Provider: {client.provider.value}")
print(f"Model: {client.model}")
print("")
print("✓ Configuration is working correctly!")
