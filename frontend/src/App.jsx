import { BrowserRouter, Route, Routes } from 'react-router-dom'
import StaffDashboard from './pages/Staff/StaffDashboard'
import CheckIn from './pages/Customer/CheckIn.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CheckIn />} />
        <Route path="/staff" element={<StaffDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}