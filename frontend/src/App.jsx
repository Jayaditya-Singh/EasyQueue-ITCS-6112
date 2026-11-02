import { useCallback, useEffect, useMemo, useState } from 'react'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const starterQueue = [
  { customer_id: 1042, customer_name: 'Olivia Martin', service_type: 'License renewal', position: 1, status: 'WAITING', estimated_wait_time: 6, joined: '9:42 AM', window: null },
  { customer_id: 1043, customer_name: 'Noah Williams', service_type: 'Real ID', position: 2, status: 'CALLED', estimated_wait_time: 0, joined: '9:46 AM', window: 'Window 03' },
  { customer_id: 1044, customer_name: 'Ava Johnson', service_type: 'Vehicle registration', position: 3, status: 'WAITING', estimated_wait_time: 18, joined: '9:51 AM', window: null },
  { customer_id: 1045, customer_name: 'Liam Brown', service_type: 'License renewal', position: 4, status: 'IN_SERVICE', estimated_wait_time: 0, joined: '9:54 AM', window: 'Window 01' },
  { customer_id: 1046, customer_name: 'Sophia Davis', service_type: 'Title transfer', position: 5, status: 'WAITING', estimated_wait_time: 30, joined: '10:02 AM', window: null },
]

const serviceNames = ['All services', 'License renewal', 'Real ID', 'Vehicle registration', 'Title transfer']
const displayStatus = (status) => status.toLowerCase().replace('_', ' ')

function App() {
  const [queue, setQueue] = useState(starterQueue)
  const [completed, setCompleted] = useState(34)
  const [search, setSearch] = useState('')
  const [notice, setNotice] = useState('')
  const [busy, setBusy] = useState(false)
  const [showAddForm, setShowAddForm] = useState(false)
  const [newCustomer, setNewCustomer] = useState({ name: '', service: serviceNames[1] })

  const refresh = useCallback(async () => {
    try {
      const [queueResponse, summaryResponse] = await Promise.all([
        fetch(`${API_URL}/queue/active`),
        fetch(`${API_URL}/staff/summary`),
      ])
      if (!queueResponse.ok || !summaryResponse.ok) throw new Error('API unavailable')
      const [queueData, summary] = await Promise.all([queueResponse.json(), summaryResponse.json()])
      if (Array.isArray(queueData.customers)) {
        setQueue(queueData.customers.map((entry, index) => ({
          ...entry,
          joined: entry.joined || '—',
          window: entry.window || null,
          position: entry.position || index + 1,
          estimated_wait_time: entry.estimated_wait_time ?? (entry.status === 'WAITING' ? (entry.position || index + 1) * 6 : 0),
        })))
      }
      if (Number.isFinite(summary.customers_completed)) setCompleted(summary.customers_completed)
      setNotice('Queue refreshed')
    } catch {
      setNotice('Showing sample queue · API is not connected')
    }
    window.setTimeout(() => setNotice(''), 3200)
  }, [])

  useEffect(() => { refresh() }, [refresh])

  const counts = useMemo(() => ({
    waiting: queue.filter((person) => person.status === 'WAITING' || person.status === 'CALLED').length,
    inService: queue.filter((person) => person.status === 'IN_SERVICE').length,
  }), [queue])

  const serviceCounts = useMemo(() => serviceNames.slice(1).map((service) => ({
    name: service,
    customers: queue.filter((person) => person.service_type.toLowerCase() === service.toLowerCase() && person.status === 'WAITING'),
    count: queue.filter((person) => person.service_type.toLowerCase() === service.toLowerCase() && person.status === 'WAITING').length,
  })), [queue])

  const visibleQueue = useMemo(() => queue
    .filter((person) => person.status !== 'COMPLETED' && person.status !== 'CANCELED')
    .filter((person) => `${person.customer_name} ${person.customer_id} ${person.service_type}`.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => a.position - b.position), [queue, search])

  const currentCustomer = queue.find((person) => person.status === 'IN_SERVICE') || queue.find((person) => person.status === 'CALLED')

  const updateStatus = async (person, action) => {
    setBusy(true)
    try {
      const endpoint = action === 'start' ? `/staff/start-service/${person.customer_id}` : `/staff/complete-service/${person.customer_id}`
      const response = await fetch(`${API_URL}${endpoint}`, { method: 'POST' })
      if (!response.ok) throw new Error('Request failed')
    } catch {
      setNotice('Could not reach the API · updated this view only')
    }
    const nextStatus = action === 'start' ? 'IN_SERVICE' : 'COMPLETED'
    setQueue((items) => items.map((item) => item.customer_id === person.customer_id ? { ...item, status: nextStatus } : item))
    if (action === 'complete') setCompleted((value) => value + 1)
    setBusy(false)
    window.setTimeout(() => setNotice(''), 3200)
  }

  const callNext = async () => {
    const next = queue.filter((person) => person.status === 'WAITING').sort((a, b) => a.position - b.position)[0]
    if (!next) { setNotice('There are no waiting customers'); return }
    setBusy(true)
    try {
      const response = await fetch(`${API_URL}/staff/call-next`, { method: 'POST' })
      if (!response.ok) throw new Error('Request failed')
    } catch { setNotice('Could not reach the API · called customer in this view only') }
    setQueue((items) => items.map((item) => item.customer_id === next.customer_id ? { ...item, status: 'CALLED', window: item.window || 'Window 02' } : item))
    setBusy(false)
    window.setTimeout(() => setNotice(''), 3200)
  }

  const addCustomer = (event) => {
    event.preventDefault()
    const name = newCustomer.name.trim()
    if (!name) return
    const id = Math.max(1000, ...queue.map((person) => Number(person.customer_id) || 1000)) + 1
    setQueue((items) => [...items, { customer_id: id, customer_name: name, service_type: newCustomer.service, position: items.length + 1, status: 'WAITING', estimated_wait_time: (items.length + 1) * 6, joined: new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }), window: null }])
    setNewCustomer({ name: '', service: serviceNames[1] })
    setShowAddForm(false)
    setNotice(`${name} added to this queue view`)
    window.setTimeout(() => setNotice(''), 3200)
  }

  const removeCustomer = (person) => {
    setQueue((items) => items.filter((item) => item.customer_id !== person.customer_id).map((item, index) => ({ ...item, position: index + 1 })))
    setNotice(`${person.customer_name} removed from this queue view`)
    window.setTimeout(() => setNotice(''), 3200)
  }

  return (
    <div className="simple-app" id="dashboard">
      <header className="simple-header">
        <a className="simple-logo" href="#dashboard">EasyQueue</a>
        <span>Staff dashboard</span>
        <button className="simple-refresh" onClick={refresh} aria-label="Refresh queue">Refresh queue</button>
      </header>
      <div className="simple-layout">
        <aside className="simple-sidebar">
          <nav aria-label="Main navigation">
            <a className="simple-nav-active" href="#dashboard">Home</a>
            <a href="#services">Services</a>
            <a href="#queue">Queue</a>
            <a href="#help">Help</a>
          </nav>
          <button className="simple-add" onClick={() => setShowAddForm((show) => !show)}>＋ Add customer</button>
        </aside>
        <main className="simple-main">
          <h1>Customer Queue Management</h1>
          {notice && <div className="simple-notice" role="status">{notice}</div>}
          {showAddForm && <form className="simple-add-form" onSubmit={addCustomer}>
            <label>Customer name<input autoFocus value={newCustomer.name} onChange={(event) => setNewCustomer({ ...newCustomer, name: event.target.value })} placeholder="Enter customer name" required /></label>
            <label>Service<select value={newCustomer.service} onChange={(event) => setNewCustomer({ ...newCustomer, service: event.target.value })}>{serviceNames.slice(1).map((service) => <option key={service}>{service}</option>)}</select></label>
            <button type="submit">Add customer</button><button className="simple-cancel" type="button" onClick={() => setShowAddForm(false)}>Cancel</button>
          </form>}

          <section className="simple-top-grid">
            <div className="simple-actions">
              <p className="simple-kicker">SERVICE CONTROLS</p>
              <button className="simple-call" onClick={callNext} disabled={busy}>Call next customer</button>
              <button className="simple-complete" onClick={() => currentCustomer && updateStatus(currentCustomer, 'complete')} disabled={busy || !currentCustomer}>Complete service</button>
              <p className="simple-hint">{currentCustomer ? `${currentCustomer.customer_name} is the current customer.` : 'No customer is currently being served.'}</p>
            </div>
            <article className="simple-current">
              <h2>Current customer information</h2>
              {currentCustomer ? <div className="simple-customer-info">
                <p><strong>Name</strong><span>{currentCustomer.customer_name}</span></p>
                <p><strong>Service</strong><span>{currentCustomer.service_type}</span></p>
                <p><strong>Queue number</strong><span>EQ-{currentCustomer.customer_id}</span></p>
                <p><strong>Window</strong><span>{currentCustomer.window || 'Not assigned'}</span></p>
                <p><strong>Status</strong><span className="simple-status">{displayStatus(currentCustomer.status)}</span></p>
              </div> : <p className="simple-empty">Call the next customer to see their information here.</p>}
            </article>
          </section>

          <section className="simple-overview" id="queue">
            <div className="simple-section-title"><div><h2>General service queue overview</h2><p>{counts.waiting} customers waiting · {counts.inService} in service · {completed} completed today</p></div><label className="simple-search"><span>Search</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Name or service" /></label></div>
            <div className="simple-queue-list">{visibleQueue.map((person) => <article className="simple-queue-row" key={person.customer_id}>
              <span className="simple-position">{person.position}</span><div className="simple-person"><strong>{person.customer_name}</strong><span>{person.service_type} · EQ-{person.customer_id}</span></div><span className="simple-wait">{person.status === 'WAITING' ? `~${person.estimated_wait_time ?? person.position * 6} min wait` : person.status === 'CALLED' ? 'Ready now' : 'In service'}</span><span className={`simple-tag simple-tag-${person.status.toLowerCase()}`}>{displayStatus(person.status)}</span>
              <span className="simple-window">{person.window || 'Waiting for window'}</span>
              <div className="simple-row-actions">{person.status === 'WAITING' && <button onClick={() => setQueue((items) => items.map((item) => item.customer_id === person.customer_id ? { ...item, status: 'CALLED', window: 'Window 01' } : item))}>Call</button>}{person.status === 'CALLED' && <button onClick={() => updateStatus(person, 'start')}>Start</button>}{person.status === 'IN_SERVICE' && <button onClick={() => updateStatus(person, 'complete')}>Complete</button>}<button className="simple-remove" onClick={() => removeCustomer(person)} aria-label={`Remove ${person.customer_name}`}>Remove</button></div>
            </article>)}{visibleQueue.length === 0 && <p className="simple-empty">No customers in this queue.</p>}</div>
          </section>

          <section className="simple-specialized" id="services">
            <h2>Specialized service queues</h2>
            <div className="simple-service-grid">{serviceCounts.map((service) => { const averageWait = service.count ? Math.round(service.customers.reduce((total, person) => total + (person.estimated_wait_time ?? person.position * 6), 0) / service.count) : 0; return <article className="simple-service-card" key={service.name}><h3>{service.name}</h3><strong>{service.count}</strong><span>customers waiting</span><span className="service-wait">{service.count ? `~${averageWait} min average wait` : 'No wait'}</span></article> })}</div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
