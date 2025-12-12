"""
Base Agent Builder Module

Provides a flexible factory for creating Agno agents with customizable configuration.
This follows the Factory and Builder design patterns.

Each agent created by this builder can customize:
- Model (ChatGPT, Claude, etc.) - configurable via ModelConfig
- Database (SQLite, PostgreSQL, etc.)
- Tools (MCP tools, custom tools, etc.)
- RAG (Vector DB, knowledge base, embeddings)
- Users management
- Memory and context handling
- And more...

Defaults are provided for all parameters, but agents can override any of them.

Usage:
    from agents.base_agent import BaseAgentBuilder
    
    # Simple usage with defaults
    agent = BaseAgentBuilder.build(
        name="My Agent",
        description="Does something",
        instructions=["Be helpful"],
        db_table="my_sessions"
    )
    
    # Advanced usage with custom parameters
    agent = BaseAgentBuilder.build(
        name="Custom Agent",
        description="Custom setup",
        instructions=["Be custom"],
        db_table="custom_sessions",
        model=my_custom_model,        # Override model
        tools=my_custom_tools,        # Override tools
        vector_db=my_vector_db,       # Enable RAG
    )
"""

from typing import Optional, List, Any
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.mcp import MCPTools

from config import get_config
from config.model_provider import get_model


class BaseAgentBuilder:
    """
    Flexible factory for building Agno agents with customizable configuration.
    
    This class provides:
    1. Sensible defaults for all agent parameters
    2. Full customization capability via optional parameters
    3. Automatic fallback to defaults when parameters are None
    4. Support for RAG, custom tools, users, etc.
    5. Model-agnostic - works with any LLM provider (OpenAI, Anthropic, etc.)
    
    Design pattern: Factory + Builder with flexible defaults
    """

    @staticmethod
    def build(
        # Required parameters
        name: str,
        description: str,
        instructions: List[str],
        db_table: str,
        # Optional parameters - Agent can override defaults
        model: Optional[Any] = None,
        db: Optional[Any] = None,
        tools: Optional[List[Any]] = None,
        users: Optional[List[str]] = None,
        vector_db: Optional[Any] = None,
        knowledge_base: Optional[Any] = None,
        embeddings: Optional[Any] = None,
        # Behavior parameters (simplified for Agno compatibility)
        add_session_state_to_context: bool = True,
        add_dependencies_to_context: bool = True,
        add_memories_to_context: bool = True,
        # Memory and context
        memory_config: Optional[dict] = None,
    ) -> Agent:
        """
        Build an Agno Agent with flexible, customizable configuration.
        
        This method creates an agent with sensible defaults but allows
        full customization of any parameter. If a parameter is None,
        a default value is used from application config.
        
        The model is created using get_model() which respects MODEL_PROVIDER
        setting, making it easy to switch between OpenAI, Anthropic, etc.
        
        Required Args:
            name (str): Agent display name (shown in Web UI)
            description (str): Agent description (shown in API docs)
            instructions (List[str]): System instructions/prompt for the agent
            db_table (str): SQLite table name for storing conversations
            
        Optional Args - Model & Tools:
            model (Any): LLM model instance (default: from get_model() using config)
            tools (List[Any]): Tools available to agent (default: MCP tools from config)
            
        Optional Args - Database & Storage:
            db (Any): Database backend (default: SQLite from config)
            vector_db (Any): Vector database for RAG (default: None)
            knowledge_base (Any): Knowledge base documents (default: None)
            embeddings (Any): Embedding model for RAG (default: None)
            
        Optional Args - Users & Access:
            users (List[str]): List of authorized users (default: None)
            
        Optional Args - Behavior:
            add_session_state_to_context (bool): Include session state (default: True)
            add_dependencies_to_context (bool): Include dependencies (default: True)
            add_memories_to_context (bool): Include memories (default: True)
            
        Optional Args - Memory:
            memory_config (dict): Memory configuration (default: None)
            
        Returns:
            Agent: Configured Agno Agent instance ready to use
            
        Example - Simple:
            >>> agent = BaseAgentBuilder.build(
            ...     name="Helper",
            ...     description="Helpful assistant",
            ...     instructions=["You are helpful"],
            ...     db_table="helper_sessions"
            ... )
            
        Example - Advanced:
            >>> agent = BaseAgentBuilder.build(
            ...     name="Research Agent",
            ...     description="Research specialist",
            ...     instructions=["You research topics"],
            ...     db_table="research_sessions",
            ...     tools=custom_tools,           # Override tools
            ...     vector_db=my_vector_db,       # Enable RAG
            ... )
        """
        config = get_config()

        # Use provided values or fall back to defaults from config
        # Model: Uses get_model() factory which respects MODEL_PROVIDER setting
        final_model = model if model is not None else get_model()
        final_db = db if db is not None else SqliteDb(
            db_file=config.database.db_file,
            session_table=db_table,  # Changed from table_name to session_table
        )
        
        # Use provided tools or empty list (MCP tools can be added per-agent)
        # MCP lifecycle is now properly managed by agent_os.serve()
        # See: https://github.com/agno-agi/agno/tree/main/cookbook/agent_os/mcp_demo
        final_tools = tools if tools is not None else []

        # Build agent with core parameters
        agent = Agent(
            # Core parameters
            name=name,
            model=final_model,
            db=final_db,
            tools=final_tools,
            instructions=instructions,
            description=description,
            # Context parameters
            add_session_state_to_context=add_session_state_to_context,
            add_dependencies_to_context=add_dependencies_to_context,
            add_memories_to_context=add_memories_to_context,
        )

        # Add optional parameters if provided
        if vector_db is not None:
            agent.vector_db = vector_db
        if knowledge_base is not None:
            agent.knowledge_base = knowledge_base
        if embeddings is not None:
            agent.embeddings = embeddings
        if users is not None:
            agent.users = users
        if memory_config is not None:
            agent.memory_config = memory_config

        return agent

