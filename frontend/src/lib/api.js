const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export async function checkHealth() {
  const response = await fetch(`${API_URL}/api/health`)
  if (!response.ok) throw new Error('Could not reach the ReplyBuddy API.')
  return response.json()
}

export async function generateReplies(payload) {
  const response = await fetch(`${API_URL}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(data.detail || 'Could not generate replies. Please try again.')
  return data
}
