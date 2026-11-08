import { useState } from 'react'
import { joinQueue } from '../../services/api.js'

// hardcoded until the backend has an endpoint for services
const SERVICE_TYPES = [
  'License Renewal',
  'Real ID',
  'Vehicle Registration',
  'Driving Test',
  'State ID',
]

// join endpoint expects customer id
const DEMO_CUSTOMER_ID = 1

export default function CheckIn() {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [phone, setPhone] = useState('')
  const [serviceType, setServiceType] = useState(SERVICE_TYPES[0])
  const [submitting, setSubmitting] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)

  async function handleSubmit(event) {
    event.preventDefault()
    setSubmitting(true)
    setMessage(null)
    setError(null)

    try {
      const result = await joinQueue(DEMO_CUSTOMER_ID, serviceType)
      setMessage(result.message)
    } catch (err) {
      setError(err.message)
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
            {SERVICE_TYPES.map((service) => (
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
