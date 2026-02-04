import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import AdminLogin from './pages/AdminLogin'
import Dashboard from './pages/Dashboard'
import PersonsList from './pages/PersonsList'
import AddPerson from './pages/AddPerson'
import PersonDetails from './pages/PersonDetails'
import Verification from './pages/Verification'
import './index.css'

function App() {
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<AdminLogin />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/persons" element={<PersonsList />} />
        <Route path="/persons/add" element={<AddPerson />} />
        <Route path="/persons/:id" element={<PersonDetails />} />
        <Route path="/verification" element={<Verification />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  )
}

export default App
