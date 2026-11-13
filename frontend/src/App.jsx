import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import CheckIn from './pages/Customer/CheckIn.jsx'
import StaffDashboard from './pages/Staff/StaffDashboard'
import AdminDashboard from './pages/Admin/AdminDashboard'

function DashboardLayout({ children }) {
  return (
    <>
      <header className="app-header dashboard-header">
        <Link to="/" className="app-brand">EasyQueue</Link>
        <nav aria-label="Dashboards">
          <Link to="/staff">Staff dashboard</Link>
          <Link to="/admin">Administrator dashboard</Link>
        </nav>
      </header>
      {children}
    </>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CheckIn />} />
        <Route path="/staff" element={<DashboardLayout><StaffDashboard /></DashboardLayout>} />
        <Route path="/admin" element={<DashboardLayout><AdminDashboard /></DashboardLayout>} />
      </Routes>
    </BrowserRouter>
  )
}
