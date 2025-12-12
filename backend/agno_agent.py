#!/usr/bin/env python3
"""
Agno Smart Assistant - Main Entry Point

This is the application's entry point and main orchestrator.
It is responsible for:

1. Loading application configuration from environment
2. Creating the FastAPI application
3. Displaying startup information
4. Running the uvicorn HTTP server

Execution Flow:
    1. Load config from environment variables (ANTHROPIC_API_KEY, PORT, etc.)
    2. Create FastAPI app with all agents initialized
    3. Display banner with connection info
    4. Start uvicorn server
    5. Handle graceful shutdown (Ctrl+C)

Usage:
    python agno_agent.py

Access:
    - Web UI: http://localhost:8000
    - API Docs: http://localhost:8000/docs

Environment Variables:
    - ANTHROPIC_API_KEY: Required. Your Anthropic API key
    - PORT: Server port (default 8000)
    - HOST: Server host (default 0.0.0.0)
    - AGNO_DB_FILE: Database file (default agno.db)
    - LOG_LEVEL: Log level (default info)
"""

from config import get_config, APP_NAME, APP_VERSION, APP_DESCRIPTION
from core.runtime import create_runtime


# Create runtime and get FastAPI app
runtime = create_runtime()
app = runtime.get_app()


if __name__ == "__main__":
    
    # Load configuration from environment
    # This validates that OPENAI_API_KEY or ANTHROPIC_API_KEY is set
    config = get_config()

    # Display startup banner with server information
    banner = f"""
====================================================================
    Agno Smart Assistant - Single Responsibility MVP
====================================================================
  Web UI: http://{config.server.host}:{config.server.port}
  API Docs: http://localhost:{config.server.port}/docs
  Agents: Conversation + Research
  DB: {config.database.db_file}
  Model: {config.agent.model_id}
====================================================================
    """
    print(banner)

    try:
        # Use uvicorn.run directly - agent_os.serve() causes shutdown issues
        import uvicorn
        uvicorn.run(
            app=app,
            host=config.server.host,
            port=config.server.port,
            reload=False,
            access_log=True,
        )
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n✋ Server stopped by user")
    except Exception as e:
        # Handle other errors
        print(f"❌ Error: {e}")
        raise
