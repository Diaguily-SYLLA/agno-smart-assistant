"""
Configuration Module

Exports:
- get_config(): Global configuration accessor
- AppConfig: Main configuration dataclass
- Constants: Application constants
"""

from config.constants import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    CONVERSATION_AGENT_CONFIG,
    RESEARCH_AGENT_CONFIG,
    ASSIST_AGENT_CONFIG,
    DEFAULT_MCP_URL,
)
from config.settings import (
    AppConfig,
    AnthropicConfig,
    DatabaseConfig,
    AgentConfig,
    ServerConfig,
    get_config,
    reset_config,
)

__all__ = [
    "AppConfig",
    "AnthropicConfig",
    "DatabaseConfig",
    "AgentConfig",
    "ServerConfig",
    "get_config",
    "reset_config",
    "APP_NAME",
    "APP_VERSION",
    "APP_DESCRIPTION",
    "CONVERSATION_AGENT_CONFIG",
    "RESEARCH_AGENT_CONFIG",
    "DEFAULT_MCP_URL",
]
