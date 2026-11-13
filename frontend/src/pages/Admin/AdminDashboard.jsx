import { useEffect, useMemo, useState } from 'react'
import './admin-dashboard.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const initialQueue = [
  { customer_id: 1042, customer_name: 'Olivia Martin', service_type: 'License renewal', position: 1, status: 'WAITING', estimated_wait_time: 6 },
  { customer_id: 1043, customer_name: 'Noah Williams', service_type: 'Real ID', position: 2, status: 'CALLED', estimated_wait_time: 0 },
  { customer_id: 1044, customer_name: 'Ava Johnson', service_type: 'Vehicle registration', position: 3, status: 'WAITING', estimated_wait_time: 18 },
  { customer_id: 1045, customer_name: 'Liam Brown', service_type: 'License renewal', position: 4, status: 'IN_SERVICE', estimated_wait_time: 0 },
  { customer_id: 1046, customer_name: 'Sophia Davis', service_type: 'Title transfer', position: 5, status: 'WAITING', estimated_wait_time: 30 },
]

const initialServices = ['License renewal', 'Real ID', 'Vehicle registration', 'Title transfer']
  .map((name) => ({ name, active: true }))

const initialWindows = [
  { name: 'Window 01', staff: 'Jordan Miller', status: 'Serving' },
  { name: 'Window 02', staff: 'Taylor Morgan', status: 'Serving' },
  { name: 'Window 03', staff: 'Unassigned', status: 'Available' },
  { name: 'Window 04', staff: 'Unassigned', status: 'Offline' },
]

export default function AdminDashboard() {
  const [queue, setQueue] = useState(initialQueue)
  const [completed, setCompleted] = useState(34)
  const [services, setServices] = useState(initialServices)
  const [windows, setWindows] = useState(initialWindows)
  const [showServiceForm, setShowServiceForm] = useState(false)
  const [serviceName, setServiceName] = useState('')
  const [notice, setNotice] = useState('')

  useEffect(() => {
    let active = true
    Promise.all([fetch(`${API_URL}/queue/active`), fetch(`${API_URL}/staff/summary`)])
      .then(async ([queueResponse, summaryResponse]) => {
        if (!queueResponse.ok || !summaryResponse.ok) throw new Error('API unavailable')
        return Promise.all([queueResponse.json(), summaryResponse.json()])
      })
      .then(([queueData, summary]) => {
        if (!active) return
        if (Array.isArray(queueData.customers)) {
          setQueue(queueData.customers.map((person, index) => ({
            ...person,
            position: person.position || index + 1,
            estimated_wait_time: person.estimated_wait_time ?? (person.status === 'WAITING' ? (person.position || index + 1) * 6 : 0),
          })))
        }
        if (Number.isFinite(summary.customers_completed)) setCompleted(summary.customers_completed)
      })
      .catch(() => { if (active) setNotice('Showing sample information because the API is unavailable.') })
    return () => { active = false }
  }, [])

  const metrics = useMemo(() => {
    const waiting = queue.filter((person) => ['WAITING', 'CALLED'].includes(person.status)).length
    const inService = queue.filter((person) => person.status === 'IN_SERVICE').length
    const estimatedWait = queue.filter((person) => person.status === 'WAITING')
      .reduce((total, person) => total + (person.estimated_wait_time || 0), 0)
    const waitingCount = queue.filter((person) => person.status === 'WAITING').length
    return {
      waiting,
      inService,
      completed,
      averageWait: waitingCount ? Math.round(estimatedWait / waitingCount) : 0,
    }
  }, [queue, completed])

  const servicesWithStats = services.map((service) => {
    const customers = queue.filter((person) => person.service_type.toLowerCase() === service.name.toLowerCase() && person.status === 'WAITING')
    const wait = customers.length
      ? Math.round(customers.reduce((sum, person) => sum + (person.estimated_wait_time || 0), 0) / customers.length)
      : 0
    return { ...service, count: customers.length, wait }
  })

  const addService = (event) => {
    event.preventDefault()
    const name = serviceName.trim()
    if (!name || services.some((service) => service.name.toLowerCase() === name.toLowerCase())) return
    setServices((items) => [...items, { name, active: true }])
    setServiceName('')
    setShowServiceForm(false)
    setNotice(`${name} service added to this dashboard.`)
    window.setTimeout(() => setNotice(''), 3000)
  }

  const toggleWindow = (windowName) => {
    setWindows((items) => items.map((item) => item.name !== windowName ? item : {
      ...item,
      status: item.status === 'Offline' ? 'Available' : 'Offline',
    }))
  }

  return (
    <main className="admin-page">
      <div className="admin-heading">
        <div>
          <p className="admin-eyebrow">CHARLOTTE DMV</p>
          <h1>Administrator dashboard</h1>
          <p className="admin-subtitle">A quick look at today’s service center.</p>
        </div>
        <span className="admin-date">{new Intl.DateTimeFormat(undefined, { dateStyle: 'long' }).format(new Date())}</span>
      </div>

      {notice && <p className="admin-notice" role="status">{notice}</p>}

      <section className="admin-metrics" aria-label="Today's service center summary">
        <article><span>Waiting</span><strong>{metrics.waiting}</strong><small>Customers in queue</small></article>
        <article><span>In service</span><strong>{metrics.inService}</strong><small>Customers at a window</small></article>
        <article><span>Average wait</span><strong>{metrics.averageWait} <em>min</em></strong><small>Estimated for waiting customers</small></article>
        <article><span>Completed</span><strong>{metrics.completed}</strong><small>Customers served today</small></article>
      </section>

      <section className="admin-panel" id="admin-services">
        <div className="admin-panel-heading">
          <div><h2>Services</h2><p>Queue size and wait time</p></div>
          <button className="admin-button" onClick={() => setShowServiceForm((open) => !open)}>{showServiceForm ? 'Cancel' : '+ Add service'}</button>
        </div>
        {showServiceForm && <form className="admin-service-form" onSubmit={addService}>
          <label htmlFor="service-name">Service name</label>
          <input id="service-name" value={serviceName} onChange={(event) => setServiceName(event.target.value)} placeholder="e.g. Address change" required />
          <button className="admin-button admin-button-dark" type="submit">Save service</button>
        </form>}
        <div className="admin-service-grid">{servicesWithStats.map((service) => <article className="admin-service-card" key={service.name}>
          <div className="admin-service-card-top"><span className={`admin-availability ${service.active ? 'is-open' : 'is-paused'}`}><i />{service.active ? 'Open' : 'Paused'}</span>
            <button className="admin-text-button" onClick={() => setServices((items) => items.map((item) => item.name === service.name ? { ...item, active: !item.active } : item))}>{service.active ? 'Pause' : 'Resume'}</button>
          </div>
          <h3>{service.name}</h3>
          <div className="admin-service-numbers"><strong>{service.count}<small> waiting</small></strong><span>{service.count ? `~${service.wait} min wait` : 'No wait'}</span></div>
        </article>)}</div>
        <p className="admin-footnote">Waits are estimates based on the active queue.</p>
      </section>

      <section className="admin-panel admin-staff-panel" id="admin-staff">
        <div className="admin-panel-heading"><div><h2>Staff windows</h2><p>Who is serving customers now</p></div></div>
        <div className="admin-window-grid">{windows.map((item) => <article className="admin-window-card" key={item.name}>
          <div className="admin-window-top"><h3>{item.name}</h3><span className={`admin-availability ${item.status === 'Offline' ? 'is-paused' : 'is-open'}`}><i />{item.status}</span></div>
          <p className="admin-window-staff">{item.staff}</p>
          <button className="admin-text-button" onClick={() => toggleWindow(item.name)}>{item.status === 'Offline' ? 'Bring online' : 'Set offline'}</button>
        </article>)}</div>
      </section>

      <p className="admin-demo-note">Admin changes are saved in this browser view only.</p>
    </main>
  )
}
