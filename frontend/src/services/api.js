// Wrapper around EasyQueue FastAPI backend
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(`${response.status} ${response.statusText}: ${detail}`)
  }

  return response.json()
}

export function joinQueue(customerId, serviceType) {
  return request('/queue/join', {
    method: 'POST',
    body: JSON.stringify({ customer_id: customerId, service_type: serviceType }),
  })
}

export function getQueueStatus(customerId) {
  return request(`/queue/status/${customerId}`)
}

export function leaveQueue(customerId) {
  return request(`/queue/leave/${customerId}`, { method: 'DELETE' })
}
