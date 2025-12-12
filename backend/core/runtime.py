"""
Agno Runtime Module

Core module responsible for initializing and managing the AgentOS runtime.
This is where all agents are instantiated and assembled into the runtime.

Responsibilities:
- Creating agent instances from builders
- Initializing AgentOS runtime with agents
- Exporting FastAPI application for uvicorn
- Managing agent lifecycle and MCP tools

Dependencies:
- agents/ - Agent factory functions
- config/ - Configuration management
- agno.os - AgentOS runtime framework

Note: AgentOS handles MCP tool lifecycle automatically.
"""

from agno.os import AgentOS
from fastapi.middleware.cors import CORSMiddleware

from config import get_config, APP_NAME, APP_VERSION, APP_DESCRIPTION
from agents.conversation_agent import create_conversation_agent
from agents.research_agent import create_research_agent
from agents.assist_agent import create_assist_agent


def create_runtime() -> AgentOS:
    """
    Create and initialize the Agno runtime with all agents.
    
    This function:
    1. Loads configuration from environment
    2. Creates agent instances (Conversation + Research)
    3. Initializes AgentOS with agents
    4. Configures UI, streaming, and API docs
    
    The runtime handles:
    - Agent lifecycle management (initialization, shutdown)
    - API endpoint registration (REST + WebSocket)
    - WebSocket streaming for real-time responses
    - Built-in Web UI at http://localhost:8000
    
    Returns:
        AgentOS: Configured runtime instance with all agents
    """
    config = get_config()

    # Create agents using factory functions
    # Each agent module is responsible for its own configuration
    conversation_agent = create_conversation_agent()
    research_agent = create_research_agent()
    assist_agent = create_assist_agent()

    # Initialize AgentOS runtime with agents
    runtime = AgentOS(
        name=APP_NAME,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
        agents=[conversation_agent, research_agent, assist_agent],
    )

    # Add CORS middleware to allow frontend requests
    app = runtime.get_app()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # Frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return runtime
