import { BrowserRouter, Route, Routes } from 'react-router-dom'

// placeholder until the real pages are added
function PlaceholderPage() {
  return (
    <main className="page">
      <h1>Check in</h1>
      <div className="card">
        <p>Service selection will go here.</p>
        <button type="button">Join Queue</button>
      </div>
      <button type="button" className="secondary">Leave Queue</button>
      <p className="muted">Frontend setup only, not connected to the backend yet.</p>
    </main>
  )
}

// add a <Route> for each new page
export default function App() {
  return (
    <BrowserRouter>
      <header className="app-header">EasyQueue</header>
      <Routes>
        <Route path="/" element={<PlaceholderPage />} />
      </Routes>
    </BrowserRouter>
  )
}
