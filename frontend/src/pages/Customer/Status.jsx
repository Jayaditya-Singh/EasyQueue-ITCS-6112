import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { getQueueStatus, leaveQueue } from '../../services/api.js'

// page refresh
const REFRESH_MS = 15000
const TICK_MS = 30000

const STATUS_LABELS = {
  WAITING: "You are in line. Thank you for your patience!",
  CALLED: "You've been called. Please go to the correct window.",
  IN_SERVICE: 'You are being served',
  COMPLETED: 'All done. Thank you for visiting!',
  CANCELED: 'You have left the queue',
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
}

export default function Status() {
  const { customerId } = useParams()
  const navigate = useNavigate()
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)
  const [leaving, setLeaving] = useState(false)
  const [baseline, setBaseline] = useState(null)
  const [now, setNow] = useState(() => Date.now())

  useEffect(() => {
    let cancelled = false

    async function load() {
      try {
        const data = await getQueueStatus(customerId)
        if (!cancelled) {
          setStatus(data)
          setError(null)
          setBaseline((prev) =>
            prev && prev.wait === data.estimated_wait_time
              ? prev
              : { wait: data.estimated_wait_time, since: Date.now() }
          )
        }
      } catch (err) {
        if (!cancelled) setError(err.message)
      }
    }

    load()
    const timer = setInterval(load, REFRESH_MS)
    return () => {
      cancelled = true
      clearInterval(timer)
    }
  }, [customerId])

  useEffect(() => {
    const clock = setInterval(() => setNow(Date.now()), TICK_MS)
    return () => clearInterval(clock)
  }, [])

  async function handleLeave() {
    if (!window.confirm('Leave the queue? You will lose your place in line.')) return

    setLeaving(true)
    try {
      await leaveQueue(customerId)
      navigate('/')
    } catch (err) {
      setError(err.message)
      setLeaving(false)
    }
  }

  const waiting = status?.status === 'WAITING'
  const canLeave = waiting || status?.status === 'CALLED'
  const finished = status?.status === 'COMPLETED' || status?.status === 'CANCELED'
  const minutesPassed = baseline ? Math.max(0, Math.floor((now - baseline.since) / 60000)) : 0
  const remaining = baseline ? Math.max(0, baseline.wait - minutesPassed) : 0
  const appointment = baseline ? formatTime(baseline.since + baseline.wait * 60000) : ''

  return (
    <div className="customer-app">
      <header className="app-header">EasyQueue</header>
      <main className="page">
        {error && <p className="error">Could not load your status. {error}</p>}
        {!status && !error && <p className="muted">Loading…</p>}

        {status && (
          <div className="card status-card">
            <h3 className="status-label">{STATUS_LABELS[status.status] ?? status.status}</h3>

            {waiting && (
              <div className="stat">
                <p className="stat-caption">Estimated wait</p>
                <span className="stat-value">{remaining}</span>
                <span className="stat-unit"> min</span>
                <p className="stat-caption">
                  Estimated appointment time <strong>{appointment}</strong>
                </p>
              </div>
            )}

            {waiting && (
              <>
                <p>Name: <strong>{status.customer_name}</strong></p>
                <p>Service: <strong>{status.service_type}</strong></p>
                <p>Position in line: <strong>{status.position}</strong></p>
              </>
            )}
          </div>
        )}

        {canLeave && (
          <button type="button" className="secondary" onClick={handleLeave} disabled={leaving}>
            {leaving ? 'Leaving…' : 'Leave Queue'}
          </button>
        )}
        {finished && (
          <button type="button" onClick={() => navigate('/')}>
            Check in again
          </button>
        )}
      </main>
    </div>
  )
}
