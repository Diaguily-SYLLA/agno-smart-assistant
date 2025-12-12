'use client'

import { useState, useEffect } from 'react'

type ChatMessage = { role: 'user' | 'assistant'; text: string }

const backendUrl =
  process.env.NEXT_PUBLIC_AGNO_BACKEND_URL || 'http://localhost:8000'

export default function ChatClient() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sessionId, setSessionId] = useState<string>('')
  const [health, setHealth] = useState<any>(null)
  const [selectedAgent, setSelectedAgent] = useState<'agno-smart-assistant' | 'research-agent' | 'assist-agent'>('agno-smart-assistant')

  useEffect(() => {
    setSessionId(`web_${Math.random().toString(36).slice(2)}`)
    // Health check
    fetch('/api/health')
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: 'error' }))
  }, [])

  const updateAssistant = (index: number, text: string) => {
    setMessages((prev) => prev.map((m, i) => (i === index ? { ...m, text } : m)))
  }

  const sendMessage = async () => {
    if (!input.trim() || isSending || !sessionId) return
    setError(null)
    const userMsg: ChatMessage = { role: 'user', text: input.trim() }
    const assistantMsg: ChatMessage = { role: 'assistant', text: '' }
    const baseMessages = [...messages, userMsg, assistantMsg]
    const assistantIndex = baseMessages.length - 1
    setMessages(baseMessages)
    setInput('')
    setIsSending(true)

    const agentId = selectedAgent

    const handleText = (chunk: string) => {
      updateAssistant(assistantIndex, chunk)
    }

    try {
      // AgentOS expects FormData
      const formData = new FormData()
      formData.append('message', userMsg.text)
      formData.append('stream', 'true')
      if (sessionId) {
        formData.append('session_id', sessionId)
        formData.append('user_id', sessionId)
      }

      // Use the correct Agno API endpoint with streaming
      const streamRes = await fetch(
        `${backendUrl}/agents/${agentId}/runs`,
        {
          method: 'POST',
          body: formData,
        }
      )

      if (streamRes.ok && streamRes.body) {
        const reader = streamRes.body.getReader()
        const decoder = new TextDecoder()
        let acc = ''
        
        while (true) {
          const { value, done } = await reader.read()
          if (done) break
          
          const chunk = decoder.decode(value, { stream: true })
          const lines = chunk.split('\n')
          
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const data = line.slice(6)
              if (data && data !== '[DONE]') {
                try {
                  const json = JSON.parse(data)
                  if (json.content) {
                    acc += json.content
                    handleText(acc)
                  }
                } catch (e) {
                  // Not JSON, treat as raw text
                  acc += data
                  handleText(acc)
                }
              }
            }
          }
        }
        
        if (!acc) {
          const finalText = await streamRes.text()
          handleText(finalText || 'Réponse vide')
        }
        setIsSending(false)
        return
      }

      // Fallback to non-streaming
      const formDataNoStream = new FormData()
      formDataNoStream.append('message', userMsg.text)
      formDataNoStream.append('stream', 'false')
      if (sessionId) {
        formDataNoStream.append('user_id', sessionId)
      }
      
      const res = await fetch(`${backendUrl}/agents/${agentId}/runs`, {
        method: 'POST',
        body: formDataNoStream,  // FormData instead of JSON
      })

      if (!res.ok) {
        throw new Error(`Backend error ${res.status}`)
      }

      const contentType = res.headers.get('content-type') || ''
      if (contentType.includes('application/json')) {
        const data = await res.json()
        const text =
          data?.response || data?.message || data?.content || JSON.stringify(data, null, 2)
        handleText(text)
      } else {
        const text = await res.text()
        handleText(text || 'Réponse vide')
      }
    } catch (err: any) {
      console.error(err)
      setError(err?.message || 'Erreur inconnue')
      updateAssistant(assistantIndex, 'Une erreur est survenue.')
    } finally {
      setIsSending(false)
    }
  }

  return (
    <div style={{ width: '720px', marginTop: 24 }}>
      {/* Agent Selector */}
      <div style={{ marginBottom: 16, display: 'flex', gap: 8, alignItems: 'center' }}>
        <label style={{ fontWeight: 600, fontSize: 14 }}>Agent:</label>
        <select
          value={selectedAgent}
          onChange={(e) => setSelectedAgent(e.target.value as any)}
          style={{
            padding: '8px 12px',
            borderRadius: 8,
            border: '1px solid #e6edf3',
            fontSize: 14,
            background: '#fff',
            cursor: 'pointer',
          }}
        >
          <option value="agno-smart-assistant">💬 Conversation Assistant</option>
          <option value="research-agent">🔍 Research Agent</option>
          <option value="assist-agent">📚 Agno Assist</option>
        </select>
        {health?.status === 'ok' && (
          <span style={{ fontSize: 12, color: '#10b981' }}>● Connected</span>
        )}
      </div>
      
      <div
        style={{
          height: 360,
          border: '1px solid #e6edf3',
          borderRadius: 12,
          padding: 12,
          background: '#fff',
          overflow: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: 12,
        }}
      >
        {messages.length === 0 && (
          <p style={{ color: '#9aa3ad' }}>Posez une question pour démarrer.</p>
        )}
        {messages.map((m, idx) => (
          <div
            key={idx}
            style={{
              alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start',
              background: m.role === 'user' ? '#0ea5e9' : '#f6f9fc',
              color: m.role === 'user' ? '#fff' : '#111827',
              padding: '10px 12px',
              borderRadius: 10,
              maxWidth: '80%',
              whiteSpace: 'pre-wrap',
            }}
          >
            {m.text || (isSending && m.role === 'assistant' ? '...' : '')}
          </div>
        ))}
      </div>
      <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              sendMessage()
            }
          }}
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: 10,
            border: '1px solid #e6edf3',
          }}
          placeholder="Poser une question..."
          disabled={isSending}
        />
        <button
          style={{
            padding: '10px 16px',
            borderRadius: 10,
            background: '#0ea5e9',
            color: '#fff',
            border: 'none',
            minWidth: 120,
            opacity: isSending ? 0.7 : 1,
          }}
          onClick={sendMessage}
          disabled={isSending}
        >
          {isSending ? 'Envoi...' : 'Envoyer'}
        </button>
      </div>
      <div
        style={{
          marginTop: 8,
          color: '#9aa3ad',
          fontSize: 13,
          display: 'flex',
          gap: 12,
          flexWrap: 'wrap',
        }}
      >
        <span>Backend: {health ? (health.status ?? 'unknown') : 'no backend connection'}</span>
        <span>Agent: qa</span>
        {sessionId && <span>Session: {sessionId}</span>}
      </div>
      {error && (
        <div style={{ marginTop: 8, color: '#b91c1c', fontSize: 13 }}>Erreur: {error}</div>
      )}
    </div>
  )
}

