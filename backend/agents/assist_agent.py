"""
Agno Assist Agent Module

Specialized documentation assistant using Retrieval-Augmented Generation (RAG).
This agent answers questions using Agno documentation to provide accurate,
grounded responses without hallucinations.

Agent Responsibilities:
- Answer questions about Agno framework
- Search documentation using hybrid search (semantic + keyword)
- Provide accurate, documentation-grounded responses
- Maintain conversation history for context

Configuration Source:
- Agent metadata from config.constants.ASSIST_AGENT_CONFIG
- Model and knowledge base from application config

Database:
- Table: "assist-agent" (separate from other agents)
- Shared SQLite file but isolated conversation history

Vector Database:
- LanceDB with hybrid search (semantic + keyword matching)
- Stores Agno documentation embeddings
- Uses OpenAI text-embedding-3-small for embeddings

Use Cases:
- Documentation Q&A
- Customer support for Agno-related questions
- Educational tutoring on Agno framework
- Help desk for developers using Agno
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType

from config import ASSIST_AGENT_CONFIG, get_config
from config.model_provider import get_model


def create_assist_agent() -> Agent:
    """
    Factory function to create the Agno Assist Agent.
    
    This agent uses Retrieval-Augmented Generation (RAG) to answer questions:
    1. Search: Queries vector database using hybrid search
    2. Retrieve: Gets relevant documentation chunks from LanceDB
    3. Context: Combines retrieved docs with conversation history
    4. Generate: LLM creates documentation-grounded answer
    
    Configuration:
    - Uses ASSIST_AGENT_CONFIG from constants
    - Knowledge base with hybrid search (semantic + keyword)
    - Vector DB: LanceDB with OpenAI embeddings
    - Documentation loaded from https://docs.agno.com/llms-full.txt
    - Separate database table for conversation history
    
    Tools:
    - Knowledge base search (automatic RAG)
    - No external MCP tools needed
    
    Returns:
        Agent: Assist agent instance with knowledge base
        
    Usage:
        >>> agent = create_assist_agent()
        >>> response = agent.run("What is Agno?")
    """
    config = get_config()

    # Setup database connection for conversation history
    db = SqliteDb(db_file=config.database.db_file)

    # Create knowledge base with hybrid search (semantic + keyword)
    try:
        knowledge = Knowledge(
            vector_db=LanceDb(
                uri="tmp/lancedb",  # Vector DB storage location
                table_name="agno_assist_knowledge",
                search_type=SearchType.hybrid,  # Combines semantic + keyword search
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
            ),
        )
        print("[INFO] Assist agent created with RAG enabled (knowledge base ready)")
    except Exception as e:
        print(f"[WARNING] Could not create knowledge base: {e}")
        print("[INFO] Creating assist agent WITHOUT RAG (basic mode)")
        knowledge = None

    # Create assist agent with RAG capabilities
    return Agent(
        id=ASSIST_AGENT_CONFIG["db_table"],
        name=ASSIST_AGENT_CONFIG["name"],
        model=get_model(),
        db=db,
        knowledge=knowledge,  # Enable RAG (None if failed)
        description=ASSIST_AGENT_CONFIG["description"],
        instructions=ASSIST_AGENT_CONFIG["instructions"],
        add_history_to_context=True,
        num_history_runs=3,
        add_datetime_to_context=True,
        markdown=True,
    )
