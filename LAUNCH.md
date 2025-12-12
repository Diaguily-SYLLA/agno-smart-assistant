# 🚀 Agno Smart Assistant - Guide de Lancement

## Architecture
- **Backend**: Python FastAPI + Agno Agents (port 8000)
- **Frontend**: Next.js (port 3000)
- **Agents**: 2 agents (Conversation + Research)
- **MCP**: Désactivé temporairement (cause des crashes)

## Lancement

### 1. Backend (Terminal 1)
```powershell
cd C:\Users\dsylla\Documents\agno-smart-assistant\backend
C:\Users\dsylla\Documents\agno-smart-assistant\.venv\Scripts\python.exe -m uvicorn agno_agent:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Frontend (Terminal 2)
```powershell
cd C:\Users\dsylla\Documents\agno-smart-assistant\frontend
npm run dev
```

## Accès
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Configuration
- Fichier: `backend/.env`
- Model: OpenAI GPT-4 (configurable)
- Provider: `MODEL_PROVIDER=openai` ou `anthropic`

## Agents Disponibles
1. **agno-smart-assistant**: Agent conversationnel général
2. **research-agent**: Agent de recherche (MCP désactivé)

## Notes
- CORS configuré pour permettre frontend → backend
- MCP tools désactivés car causent un crash au démarrage
- Pour réactiver MCP: décommenter dans `backend/core/runtime.py` ligne 58
