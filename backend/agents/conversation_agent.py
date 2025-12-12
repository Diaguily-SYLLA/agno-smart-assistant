"""
Conversation Agent Module

Specialized module for creating the main Conversation Agent.
This is the primary agent for general-purpose chat interactions.

Agent Responsibilities:
- General-purpose chat and task execution
- Access to all MCP tools (Web Search, Math, Google, Gmail)
- Conversation persistence in SQLite
- Real-time responses with streaming

Configuration Source:
- Agent metadata from config.constants.CONVERSATION_AGENT_CONFIG
- Model and tools from application config

Database:
- Table: "agent_sessions" (stores all conversations)
- Shared SQLite file with other agents
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from config import CONVERSATION_AGENT_CONFIG, get_config
from config.model_provider import get_model


def create_conversation_agent() -> Agent:
    """
    Factory function to create the main Conversation Agent.
    
    This agent is designed for:
    - General-purpose chat interactions
    - Tool execution (Web Search, Math, etc.)
    - Long-running conversations
    - Context-aware responses
    
    Configuration:
    - Uses CONVERSATION_AGENT_CONFIG from constants
    - Inherits model, database, tools from BaseAgentBuilder
    - Separate database table from research agent
    
    Returns:
        Agent: Conversation agent instance configured and ready to use
        
    Usage:
        >>> agent = create_conversation_agent()
        >>> response = agent.run("Hello!")
    """
    config = get_config()

    # Setup database connection
    db = SqliteDb(db_file=config.database.db_file)

    # Create conversation agent with direct Agent() constructor
    return Agent(
        id=CONVERSATION_AGENT_CONFIG["db_table"],
        name=CONVERSATION_AGENT_CONFIG["name"],
        model=get_model(),
        db=db,
        description=CONVERSATION_AGENT_CONFIG["description"],
        instructions=CONVERSATION_AGENT_CONFIG["instructions"],
        add_history_to_context=True,
        num_history_runs=3,
        markdown=True,
    )
