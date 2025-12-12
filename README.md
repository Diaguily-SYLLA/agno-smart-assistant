# Agno Smart Assistant

Multi-agent AI assistant powered by **Agno** and **Claude AI**.

## 🎯 Features

✅ **Multi-Agent Support** - Conversation + Research agents  
✅ **Persistent Storage** - SQLite for conversation history  
✅ **Single Responsibility** - Clean, modular architecture  
✅ **Tool Integration** - MCP tools for external integrations  
✅ **Built-in Web UI** - Chat interface at `http://localhost:8000`  
✅ **Comprehensive Docs** - Detailed comments in every file

## 📸 Screenshots

### Conversation Assistant
General-purpose chat and task execution with full context awareness.

![Conversation Assistant](assets/screenshot-conversation.png)

### Research Agent
Specialized agent for research, analysis, and information retrieval.

![Research Agent](assets/screenshot-research.png)

### Agno Assist
RAG-powered documentation assistant with knowledge base integration.

![Agno Assist](assets/screenshot-assist.png)

## 🏗️ Architecture

```
backend/
├── 📁 config/        → Configuration (settings, constants)
├── 📁 agents/        → Agent definitions (Conversation, Research)
├── 📁 core/          → Runtime setup (AgentOS, FastAPI)
├── 📁 utils/         → Utilities (logging)
├── 📄 agno_agent.py  → Entry point (59 lines)
├── 📄 requirements.txt
└── 📄 .env
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `config/` | Load environment variables, provide typed configuration |
| `agents/` | Define and build agents using factory pattern |
| `core/` | Initialize AgentOS runtime and FastAPI app |
| `utils/` | Logging and utility functions |
| `agno_agent.py` | Application entry point and server startup |

## 🚀 Quick Start

### 1. Set API Key

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### 2. Run the Application

```bash
cd backend
python agno_agent.py
```

### 3. Access the Application

- **Web UI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📦 Installation

```bash
pip install -r backend/requirements.txt
```

## 🔧 Configuration

All configuration comes from environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Required | Your Anthropic API key |
| `AGNO_MODEL_ID` | `claude-sonnet-4-5` | Claude model to use |
| `PORT` | `8000` | Server port |
| `AGNO_DB_FILE` | `agno.db` | SQLite database file |
| `HOST` | `0.0.0.0` | Server host |
| `LOG_LEVEL` | `info` | Logging level |
| `RELOAD` | `true` | Auto-reload on code changes |

## 🤖 Agents

### Conversation Agent
- **Name**: Agno Smart Assistant
- **Description**: Main conversational agent with tool access
- **Database Table**: `agent_sessions`
- **Features**:
  - General-purpose chat and task execution
  - Access to all MCP tools
  - Conversation persistence
  - Full context awareness

### Research Agent
- **Name**: Research Agent
- **Description**: Specialized agent for research and analysis
- **Database Table**: `research_sessions`
- **Features**:
  - Information retrieval and synthesis
  - Detailed structured responses
  - Focused analysis capabilities

## 📝 Code Structure & Patterns

### Design Patterns Used

1. **Singleton Pattern** - Global config instance
2. **Factory Pattern** - Agent creation (BaseAgentBuilder)
3. **Configuration Object** - AppConfig and sub-configs
4. **Dependency Injection** - Services injected via config

### Example: Adding a New Agent

```python
# 1. Create agents/my_agent.py
from agents.base_agent import BaseAgentBuilder

def create_my_agent():
    return BaseAgentBuilder.build(
        name="My Agent",
        description="Does something special",
        instructions=["You are helpful"],
        db_table="my_agent_sessions"
    )

# 2. Update core/runtime.py
from agents import create_my_agent

def create_runtime():
    my_agent = create_my_agent()
    # Add to agents list...
```

## 📚 File Documentation

Every file includes detailed docstrings explaining:
- **Purpose**: What the module does
- **Responsibilities**: What it's responsible for
- **Dependencies**: What it depends on
- **Usage**: How to use it

**Example docstrings cover**:
- Module-level: Purpose, design patterns, usage examples
- Functions: Args, returns, examples, error conditions
- Classes: Responsibilities, design considerations
- Configuration: Environment variables, defaults

## 🧪 Testing

### Test Imports
```bash
cd backend
python -c "from core import get_app; print('✅ OK')"
```

### API Testing
Use the built-in Swagger UI: http://localhost:8000/docs

### Configuration Testing
```bash
python -c "from config import get_config; c = get_config(); print(f'Port: {c.server.port}')"
```

## 🔍 Troubleshooting

### ANTHROPIC_API_KEY not set
```
Error: ANTHROPIC_API_KEY environment variable is required
```
**Solution**: Set your API key before running:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### Port 8000 already in use
```
Error: Address already in use
```
**Solution**: Use a different port:
```powershell
$env:PORT = "8001"
python agno_agent.py
```

### Module import errors
```
ModuleNotFoundError: No module named 'agno'
```
**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

## 📚 Further Reading

- **Agno Docs**: https://docs.agno.com
- **Claude API**: https://docs.anthropic.com
- **FastAPI**: https://fastapi.tiangolo.com
- **Python Logging**: https://docs.python.org/3/library/logging.html

## 📝 License

MIT
