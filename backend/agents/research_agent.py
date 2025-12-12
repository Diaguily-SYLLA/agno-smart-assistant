"""
Research Agent Module

Specialized module for creating the Research Agent.
This agent is optimized for information gathering and analysis tasks.

Agent Responsibilities:
- Information retrieval and synthesis
- Research and analysis tasks
- Detailed structured responses
- Access to MCP tools for web searches and data

Configuration Source:
- Agent metadata from config.constants.RESEARCH_AGENT_CONFIG
- Model and tools from application config

Database:
- Table: "research_sessions" (separate from conversation agent)
- Shared SQLite file but isolated conversation history

Use Cases:
- Document analysis and summarization
- Research queries and information synthesis
- Data analysis tasks
- Report generation
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.tools.mcp import MCPTools

from config import RESEARCH_AGENT_CONFIG, get_config
from config.model_provider import get_model


def create_research_agent() -> Agent:
    """
    Factory function to create the Research Specialist Agent.
    
    This agent is designed for:
    - Information research and gathering
    - Analysis and synthesis of complex topics
    - Detailed report generation
    - Structured information extraction
    
    Configuration:
    - Uses RESEARCH_AGENT_CONFIG from constants
    - MCP Tools activated for enhanced research capabilities
    - MCP URL: https://docs.agno.com/mcp (Agno knowledge base)
    - Separate database table keeps research conversations isolated
    - No memories (research is stateless)
    
    Tools:
    - MCP (Model Context Protocol) tools for web search, data access, etc.
    - Provides SearchAgno tool for searching Agno documentation
    
    Returns:
        Agent: Research agent instance configured with MCP tools
        
    Usage:
        >>> agent = create_research_agent()
        >>> response = agent.run("Research quantum computing")
    """
    config = get_config()

    # Setup database connection
    db = SqliteDb(db_file=config.database.db_file)

    # Configure MCP tools for research agent
    # Transport: streamable-http for HTTP-based MCP servers
    # URL comes from config (e.g., https://docs.agno.com/mcp)
    mcp_tools = MCPTools(
        transport="streamable-http",
        url=getattr(config.agent, "mcp_url", "https://docs.agno.com/mcp"),
    )
    
    # Create research agent with MCP tools
    return Agent(
        id=RESEARCH_AGENT_CONFIG["db_table"],
        name=RESEARCH_AGENT_CONFIG["name"],
        model=get_model(),
        db=db,
        tools=[mcp_tools],  # MCP tools for research capabilities
        description=RESEARCH_AGENT_CONFIG["description"],
        instructions=RESEARCH_AGENT_CONFIG["instructions"],
        add_history_to_context=True,
        num_history_runs=3,
        markdown=True,
    )
