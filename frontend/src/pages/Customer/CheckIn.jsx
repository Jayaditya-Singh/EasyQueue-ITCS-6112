import { useEffect, useState } from 'react'
import { createCustomer, getServices, joinQueue } from '../../services/api.js'

// Used only if GET /services can't be reached
const FALLBACK_SERVICE_TYPES = [
  'License Renewal',
  'Real ID',
  'Vehicle Registration',
  'Driving Test',
  'State ID',
]

// FastAPI validation errors come back as JSON with a "detail" field
function readableError(err) {
  const json = err.message.slice(err.message.indexOf('{'))
  try {
    const { detail } = JSON.parse(json)
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d) => d.msg.replace(/^Value error, /, '')).join(' ')
  } catch {
    // not JSON; fall through
  }
  return err.message
}

export default function CheckIn() {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [phone, setPhone] = useState('')
  const [serviceTypes, setServiceTypes] = useState(FALLBACK_SERVICE_TYPES)
  const [serviceType, setServiceType] = useState(FALLBACK_SERVICE_TYPES[0])
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    getServices()
      .then((services) => {
        const names = services.map((service) => service.service_name)
        if (names.length > 0) {
          setServiceTypes(names)
          setServiceType(names[0])
        }
      })
      .catch(() => {})
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    setMessage(null)
    setError(null)

    try {
      const customer = await createCustomer(`${firstName} ${lastName}`, phone)
      const result = await joinQueue(customer.customer_id, serviceType)
      setMessage(result.message)
    } catch (err) {
      setError(readableError(err))
    }

    setSubmitting(false)
  }

  return (
    <div className="customer-app">
      <header className="app-header">EasyQueue</header>
      <main className="page">
        <h1>Check in</h1>
        <form className="card" onSubmit={handleSubmit}>
          <label className="field">
            First name
            <input
              type="text"
              value={firstName}
              onChange={(event) => setFirstName(event.target.value)}
              autoComplete="given-name"
              required
            />
          </label>
          <label className="field">
            Last name
            <input
              type="text"
              value={lastName}
              onChange={(event) => setLastName(event.target.value)}
              autoComplete="family-name"
              required
            />
          </label>
          <label className="field">
            Phone number
            <input
              type="tel"
              value={phone}
              onChange={(event) => setPhone(event.target.value)}
              autoComplete="tel"
              required
            />
          </label>
          <fieldset className="service-selector">
            <legend>What are you here for?</legend>
            {serviceTypes.map((service) => (
              <label
                key={service}
                className={service === serviceType ? 'service-option selected' : 'service-option'}
              >
                <input
                  type="radio"
                  name="service"
                  value={service}
                  checked={service === serviceType}
                  onChange={() => setServiceType(service)}
                />
                {service}
              </label>
            ))}
          </fieldset>
          {error && <p className="error">Couldn't join the queue. {error}</p>}
          {message && <p className="muted">{message}</p>}
          <button type="submit" disabled={submitting}>
            {submitting ? 'Joining…' : 'Join Queue'}
          </button>
        </form>
      </main>
    </div>
  )
}
