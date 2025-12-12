import ChatClient from './components/ChatClient'

export default function Home() {
  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Inter, Arial' }}>
      <aside style={{ width: 260, borderRight: '1px solid #ececec', padding: 24 }}>
        <h2 style={{ marginBottom: 16 }}>Assistants</h2>
        <div style={{ fontSize: 14, color: '#666', marginBottom: 12 }}>
          Choisissez un agent dans le chat →
        </div>
      </aside>
      <main
        style={{
          flex: 1,
          padding: 24,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <h1 style={{ marginBottom: 8 }}>Comment puis-je vous aider ?</h1>
        <ChatClient />
      </main>
    </div>
  )
}

