import { NextResponse } from 'next/server'

export async function GET() {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_AGNO_BACKEND_URL || 'http://localhost:8000'
    const response = await fetch(`${backendUrl}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    })
    
    if (response.ok) {
      const data = await response.json()
      return NextResponse.json({ status: 'ok', backend: data })
    }
    
    return NextResponse.json({ status: 'backend_error', backend: null })
  } catch (error) {
    return NextResponse.json({ status: 'error', backend: null })
  }
}
