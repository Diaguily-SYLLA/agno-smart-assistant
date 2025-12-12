"""
Application Constants

Hardcoded values that don't change per environment.
"""

# ============================================================================
# Application Info
# ============================================================================

from sqlalchemy import true


APP_NAME = "Agno Smart Assistant"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Multi-agent AI assistant powered by Agno"

# ============================================================================
# Database Defaults
# ============================================================================

DEFAULT_DB_FILE = "agno.db"
DEFAULT_VECTOR_DB_FILE = "vector.db"

# ============================================================================
# Model Defaults
# ============================================================================

DEFAULT_MODEL_PROVIDER = "openai"  # "openai" or "anthropic"
DEFAULT_MODEL_ID = "gpt-4"         # OpenAI: gpt-4, gpt-3.5-turbo, etc.
                                    # Anthropic: claude-3-5-sonnet, claude-3-opus, etc.

# ============================================================================
# Agent Defaults
# ============================================================================

DEFAULT_MCP_URL = "https://docs.agno.com/mcp"

# ============================================================================
# Server Defaults
# ============================================================================

DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"
DEFAULT_LOG_LEVEL = "info"

# ============================================================================
# Agent Configurations
# ============================================================================

CONVERSATION_AGENT_CONFIG = {
    "name": "Agno Smart Assistant",
    "description": "Main conversational agent with tool access",
    "instructions": [
        "You are a helpful AI assistant powered by Agno.",
        "You have access to tools and can perform tasks.",
        "Always be concise, clear, and helpful.",
    ],
    "db_table": "agno-smart-assistant",  # Frontend uses this as ID
    "show_tool_calls": True,
    "add_datetime_to_context": True,
}

RESEARCH_AGENT_CONFIG = {
    "name": "Research Agent",
    "description": "Specialized agent for research and analysis",
    "instructions": [
        "You are a research specialist.",
        "Help users find, analyze, and synthesize information.",
        "Provide well-structured and detailed responses.",
    ],
    "db_table": "research-agent",  # Frontend uses this as ID
    "show_tool_calls": True,
    "add_datetime_to_context": False,
}

ASSIST_AGENT_CONFIG = {
    "name": "Agno Assist",
    "description": "Documentation assistant using RAG for Agno framework questions",
    "instructions": [
        "You help answer questions about the Agno framework.",
        "Search your knowledge before answering the question.",
        "Provide accurate answers grounded in the documentation.",
        "If information is not in the documentation, say so clearly.",
    ],
    "db_table": "assist-agent",  # Frontend uses this as ID
    "show_tool_calls": True,
    "add_datetime_to_context": True,
}

# ============================================================================
# UI Settings
# ============================================================================

ENABLE_UI = True
ENABLE_API_DOCS = True
ENABLE_STREAMING = True

# ============================================================================
# Feature Flags
# ============================================================================

DEBUG_MODE = False
