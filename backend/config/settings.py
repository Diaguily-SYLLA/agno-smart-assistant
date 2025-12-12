"""
Application Settings Module

Loads environment variables and provides typed configuration.
Implements the Configuration Object pattern (similar to Spring Boot).

This module:
1. Reads environment variables
2. Validates required settings (API keys, etc.)
3. Provides typed configuration objects via dataclasses
4. Maintains a global singleton instance

Design Pattern: Singleton + Configuration Object

Usage:
    from config import get_config
    
    config = get_config()
    print(config.server.port)
    print(config.anthropic.api_key)
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    # dotenv not installed, continue without loading .env
    pass

from config.constants import (
    APP_NAME,
    APP_VERSION,
    APP_DESCRIPTION,
    DEFAULT_DB_FILE,
    DEFAULT_VECTOR_DB_FILE,
    DEFAULT_MODEL_ID,
    DEFAULT_MCP_URL,
    DEFAULT_PORT,
    DEFAULT_HOST,
    DEFAULT_LOG_LEVEL,
)


@dataclass
class OpenAIConfig:
    """
    OpenAI API Configuration
    
    Loads API credentials from environment and validates them.
    """

    api_key: str  # OpenAI API key (secret)

    @staticmethod
    def from_env() -> "OpenAIConfig":
        """
        Load OpenAI configuration from environment variables.
        
        Optional: OPENAI_API_KEY environment variable
        Not required if using Anthropic provider
        
        Returns:
            OpenAIConfig: Loaded configuration (empty if not set)
        """
        return OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", "")
        )


@dataclass
class AnthropicConfig:
    """
    Anthropic API Configuration
    
    Loads API credentials from environment and validates them.
    """

    api_key: str  # Anthropic API key (secret)

    @staticmethod
    def from_env() -> "AnthropicConfig":
        """
        Load Anthropic configuration from environment variables.
        
        Optional: ANTHROPIC_API_KEY environment variable
        Not required if using OpenAI provider
        
        Returns:
            AnthropicConfig: Loaded configuration (empty if not set)
        """
        return AnthropicConfig(
            api_key=os.getenv("ANTHROPIC_API_KEY", "")
        )


@dataclass
class DatabaseConfig:
    """
    Database Configuration
    
    Manages SQLite database file paths for conversation storage
    and vector embeddings.
    """

    db_file: str        # SQLite database file (conversations)
    vector_db_file: str  # Vector database file (embeddings)

    @staticmethod
    def from_env() -> "DatabaseConfig":
        """
        Load database configuration from environment variables.
        
        Environment Variables:
        - AGNO_DB_FILE: SQLite database file (default: agno.db)
        - VECTOR_DB_FILE: Vector database file (default: vector.db)
        
        Returns:
            DatabaseConfig: Loaded configuration with defaults
        """
        return DatabaseConfig(
            db_file=os.getenv("AGNO_DB_FILE", DEFAULT_DB_FILE),
            vector_db_file=os.getenv("VECTOR_DB_FILE", DEFAULT_VECTOR_DB_FILE),
        )


@dataclass
class ModelConfig:
    """
    Model Provider Configuration
    
    Manages which LLM provider to use (OpenAI, Anthropic, etc.)
    and default model IDs for each provider.
    """

    provider: str   # "openai" or "anthropic"
    model_id: str   # Model ID for the selected provider

    @staticmethod
    def from_env() -> "ModelConfig":
        """
        Load model configuration from environment variables.
        
        Environment Variables:
        - MODEL_PROVIDER: Provider to use (default: openai)
          Options: "openai", "anthropic"
        - MODEL_ID: Model ID (varies by provider)
          OpenAI: gpt-4, gpt-4-turbo, gpt-3.5-turbo, etc.
          Anthropic: claude-3-5-sonnet, claude-3-opus, etc.
        
        Returns:
            ModelConfig: Loaded configuration with defaults
        """
        provider = os.getenv("MODEL_PROVIDER", "openai").lower()
        
        # Default model IDs by provider
        default_models = {
            "openai": "gpt-4",
            "anthropic": "claude-3-5-sonnet-20241022",
        }
        
        model_id = os.getenv("MODEL_ID", default_models.get(provider, "gpt-4"))
        
        return ModelConfig(
            provider=provider,
            model_id=model_id,
        )


@dataclass
class AgentConfig:
    """
    Agno Agent Configuration
    
    Manages agent runtime settings including model selection
    and tool integration endpoints.
    """

    model_id: str   # Model ID (deprecated, use ModelConfig.model_id)
    mcp_url: str    # Model Context Protocol endpoint URL

    @staticmethod
    def from_env() -> "AgentConfig":
        """
        Load agent configuration from environment variables.
        
        Environment Variables:
        - AGNO_MODEL_ID: Model ID (default: gpt-4)
        - AGNO_MCP_URL: MCP endpoint (default: https://docs.agno.com/mcp)
        
        Returns:
            AgentConfig: Loaded configuration with defaults
        """
        return AgentConfig(
            model_id=os.getenv("AGNO_MODEL_ID", DEFAULT_MODEL_ID),
            mcp_url=os.getenv("AGNO_MCP_URL", DEFAULT_MCP_URL),
        )


@dataclass
class ServerConfig:
    """
    HTTP Server Configuration
    
    Manages uvicorn/FastAPI server settings including
    port, host, reload behavior, and logging.
    """

    host: str       # Server hostname (0.0.0.0 = all interfaces)
    port: int       # Server port (typically 8000)
    reload: bool    # Auto-reload on code changes (development)
    log_level: str  # Logging verbosity (info, debug, warning, error)

    @staticmethod
    def from_env() -> "ServerConfig":
        """
        Load server configuration from environment variables.
        
        Environment Variables:
        - HOST: Server host (default: 0.0.0.0)
        - PORT: Server port (default: 8000)
        - RELOAD: Auto-reload (default: true) - set to false in production
        - LOG_LEVEL: Log level (default: info)
        
        Returns:
            ServerConfig: Loaded configuration with defaults
        """
        reload_str = os.getenv("RELOAD", "true").lower()
        reload = reload_str in ("true", "1", "yes")

        port_str = os.getenv("PORT", str(DEFAULT_PORT))
        try:
            port = int(port_str)
        except ValueError:
            port = DEFAULT_PORT

        return ServerConfig(
            host=os.getenv("HOST", DEFAULT_HOST),
            port=port,
            reload=reload,
            log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        )


@dataclass
class AppConfig:
    """
    Complete Application Configuration
    
    This is the main configuration object that combines all sub-configurations.
    It's created once at startup and accessed globally via get_config().
    
    Design Pattern: Singleton configuration holder
    """

    name: str = APP_NAME
    version: str = APP_VERSION
    description: str = APP_DESCRIPTION
    openai: OpenAIConfig = None             # OpenAI API settings
    anthropic: AnthropicConfig = None       # Anthropic API settings
    model: ModelConfig = None               # Model provider selection
    database: DatabaseConfig = None         # Database settings
    agent: AgentConfig = None               # Agent runtime settings
    server: ServerConfig = None             # HTTP server settings

    def __post_init__(self):
        """
        Initialize sub-configurations if not provided.
        This is called automatically after dataclass initialization.
        """
        if self.openai is None:
            self.openai = OpenAIConfig.from_env()
        if self.anthropic is None:
            self.anthropic = AnthropicConfig.from_env()
        if self.model is None:
            self.model = ModelConfig.from_env()
        if self.database is None:
            self.database = DatabaseConfig.from_env()
        if self.agent is None:
            self.agent = AgentConfig.from_env()
        if self.server is None:
            self.server = ServerConfig.from_env()
        
        # Validate: At least one API key must be provided
        if not self.openai.api_key and not self.anthropic.api_key:
            raise ValueError(
                "❌ No API key configured.\n"
                "   Set either OPENAI_API_KEY or ANTHROPIC_API_KEY\n"
                "   Current provider: " + self.model.provider
            )

    @staticmethod
    def from_env() -> "AppConfig":
        """
        Load complete configuration from environment variables.
        
        This is the main factory method for creating the app config.
        It loads all sub-configurations and validates them.
        
        Returns:
            AppConfig: Complete application configuration
            
        Raises:
            ValueError: If required settings are missing
        """
        return AppConfig(
            openai=OpenAIConfig.from_env(),
            anthropic=AnthropicConfig.from_env(),
            model=ModelConfig.from_env(),
            database=DatabaseConfig.from_env(),
            agent=AgentConfig.from_env(),
            server=ServerConfig.from_env(),
        )

    def to_dict(self) -> dict:
        """
        Convert config to dictionary for display/logging.
        
        Useful for displaying config info without exposing secrets.
        API key is masked: "***abcd" (last 4 chars only)
        
        Returns:
            dict: Configuration as nested dictionary
        """
        return {
            "app": {
                "name": self.name,
                "version": self.version,
                "description": self.description,
            },
            "model": {
                "provider": self.model.provider,
                "model_id": self.model.model_id,
            },
            "openai": {"api_key": "***" + (self.openai.api_key[-4:] if self.openai.api_key else "NOT SET")},
            "anthropic": {"api_key": "***" + (self.anthropic.api_key[-4:] if self.anthropic.api_key else "NOT SET")},
            "database": {
                "db_file": self.database.db_file,
                "vector_db_file": self.database.vector_db_file,
            },
            "agent": {
                "model_id": self.agent.model_id,
                "mcp_url": self.agent.mcp_url,
            },
            "server": {
                "host": self.server.host,
                "port": self.server.port,
                "reload": self.server.reload,
                "log_level": self.server.log_level,
            },
        }


# ============================================================================
# Global Configuration Instance (Singleton Pattern)
# ============================================================================

_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """
    Get or initialize the global configuration instance.
    
    This implements the Singleton pattern:
    - First call creates config from environment
    - Subsequent calls return the same instance
    - Ensures configuration is loaded only once
    
    Returns:
        AppConfig: Global configuration instance
        
    Example:
        >>> config = get_config()
        >>> print(config.server.port)
        8000
    """
    global _config
    if _config is None:
        _config = AppConfig.from_env()
    return _config


def reset_config() -> None:
    """
    Reset configuration (primarily for testing).
    
    This clears the global config instance so that
    the next call to get_config() will reload from environment.
    
    Only use this in testing or when environment variables change.
    """
    global _config
    _config = None
