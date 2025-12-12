"""
Knowledge Base Loader for Agno Assist Agent

This script loads the Agno documentation into the knowledge base.
Run this once to populate the vector database with documentation.

Usage:
    python load_knowledge.py

This will:
1. Download Agno documentation from https://docs.agno.com/llms-full.txt
2. Split it into chunks
3. Generate embeddings using OpenAI
4. Store in LanceDB vector database

The process may take 2-5 minutes depending on documentation size.
"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.knowledge.embedder.openai import OpenAIEmbedder


def load_documentation():
    """Load Agno documentation into knowledge base"""
    
    print("=" * 70)
    print(" Agno Assist - Knowledge Base Loader")
    print("=" * 70)
    print()
    print("[1/4] Creating knowledge base connection...")
    
    # Create knowledge base (same config as assist_agent.py)
    knowledge = Knowledge(
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="agno_assist_knowledge",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
        ),
    )
    
    print("[2/4] Downloading documentation from https://docs.agno.com/llms-full.txt...")
    print("      (This may take 2-5 minutes)")
    
    try:
        # Load documentation
        knowledge.add_content(
            name="Agno Documentation",
            url="https://docs.agno.com/llms-full.txt",
            skip_if_exists=True,
        )
        
        print()
        print("[SUCCESS] Documentation loaded successfully!")
        print()
        print("Knowledge base is now ready for Agno Assist agent.")
        print("You can start using the assist-agent with RAG capabilities.")
        print()
        
    except KeyboardInterrupt:
        print()
        print("[CANCELLED] Loading interrupted by user")
        print()
        sys.exit(1)
        
    except Exception as e:
        print()
        print(f"[ERROR] Failed to load documentation: {e}")
        print()
        print("Please check:")
        print("  1. Internet connection")
        print("  2. OPENAI_API_KEY environment variable is set")
        print("  3. OpenAI API has credits available")
        print()
        sys.exit(1)


if __name__ == "__main__":
    load_documentation()
