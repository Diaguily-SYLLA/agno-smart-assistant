"""
Model Provider Factory

Abstraction layer that supports multiple LLM providers (OpenAI, Anthropic, etc.)
This allows easy switching between different AI model providers without code changes.

Supported Providers:
- openai: ChatGPT (GPT-4, GPT-3.5)
- anthropic: Claude (Sonnet, Opus)

Design Pattern: Factory + Strategy

Usage:
    from config.model_provider import get_model
    
    # Simple usage - uses provider from config
    model = get_model()
    
    # Or specify provider directly
    model = get_model(provider="openai", model_id="gpt-4")
"""

from typing import Optional, Literal
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude

from config import get_config


ModelProvider = Literal["openai", "anthropic"]


def get_model(
    provider: Optional[ModelProvider] = None,
    model_id: Optional[str] = None,
) -> Optional[object]:
    """
    Factory function to create model instances based on provider.
    
    Args:
        provider: Model provider ("openai" or "anthropic")
                 If None, uses config default
        model_id: Model ID (e.g., "gpt-4", "claude-sonnet-4-5")
                 If None, uses config default
    
    Returns:
        Model instance (OpenAIChat, Claude, etc.)
    
    Example:
        # Use config defaults
        model = get_model()
        
        # Override provider and model
        model = get_model(provider="openai", model_id="gpt-4-turbo")
        
        # Just override model
        model = get_model(model_id="gpt-3.5-turbo")
    """
    config = get_config()
    
    # Use provided values or fall back to config
    final_provider = provider or config.model.provider
    final_model_id = model_id or config.model.model_id
    
    if final_provider == "openai":
        return OpenAIChat(
            id=final_model_id,
            api_key=config.openai.api_key,
        )
    elif final_provider == "anthropic":
        return Claude(
            id=final_model_id,
            api_key=config.anthropic.api_key,
        )
    else:
        raise ValueError(
            f"❌ Unsupported provider: {final_provider}\n"
            f"   Supported: 'openai', 'anthropic'"
        )


def get_provider_name(provider: Optional[ModelProvider] = None) -> str:
    """
    Get human-readable provider name.
    
    Args:
        provider: Provider ID
        
    Returns:
        Human-readable name
    """
    config = get_config()
    final_provider = provider or config.model.provider
    
    names = {
        "openai": "OpenAI ChatGPT",
        "anthropic": "Anthropic Claude",
    }
    return names.get(final_provider, "Unknown Provider")
