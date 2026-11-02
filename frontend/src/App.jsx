import { BrowserRouter, Route, Routes } from 'react-router-dom'
import StaffDashboard from './pages/Staff/StaffDashboard'

function PlaceholderPage() {
  return (
    <main className="page">
      <h1>Check in</h1>
      <div className="card">
        <p>Service selection will go here.</p>
        <button type="button">Join Queue</button>
      </div>
      <button type="button" className="secondary">
        Leave Queue
      </button>
      <p className="muted">
        Frontend setup only, not connected to the backend yet.
      </p>
    </main>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <header className="app-header">EasyQueue</header>

      <Routes>
        <Route path="/" element={<PlaceholderPage />} />
        <Route path="/staff" element={<StaffDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}
