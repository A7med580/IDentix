import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import Navbar from '../components/Navbar'

const COLORS = ['#3b82f6', '#ef4444', '#10b981']

function Dashboard() {
  const [overview, setOverview] = useState(null)
  const [todayAttendance, setTodayAttendance] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [overviewRes, attendanceRes] = await Promise.all([
        axios.get('http://localhost:5001/api/analytics/overview'),
        axios.get('http://localhost:5001/api/attendance/today')
      ])

      setOverview(overviewRes.data)
      setTodayAttendance(attendanceRes.data.attendance)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-darker">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-white">Loading...</div>
        </div>
      </div>
    )
  }

  // Prepare chart data
  const attendanceData = [
    { name: 'Present', value: overview?.present_today || 0 },
    { name: 'Absent', value: (overview?.total_persons || 0) - (overview?.present_today || 0) }
  ]

  const statusData = [
    { name: 'On Time', value: (overview?.present_today || 0) - (overview?.late_today || 0) },
    { name: 'Late', value: overview?.late_today || 0 }
  ]

  return (
    <div className="min-h-screen bg-darker">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
          <p className="text-secondary">Overview of attendance and analytics</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Total Persons</div>
            <div className="text-3xl font-bold text-white">{overview?.total_persons || 0}</div>
          </div>
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Present Today</div>
            <div className="text-3xl font-bold text-green-400">{overview?.present_today || 0}</div>
          </div>
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Late Today</div>
            <div className="text-3xl font-bold text-yellow-400">{overview?.late_today || 0}</div>
          </div>
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Attendance Rate</div>
            <div className="text-3xl font-bold text-blue-400">{overview?.attendance_rate || 0}%</div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Attendance Pie Chart */}
          <div className="glass-panel p-6">
            <h3 className="text-lg font-semibold text-white mb-4">Today's Attendance</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={attendanceData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {attendanceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Status Pie Chart */}
          <div className="glass-panel p-6">
            <h3 className="text-lg font-semibold text-white mb-4">On-Time vs Late</h3>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={statusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === 0 ? '#10b981' : '#f59e0b'} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link to="/persons/add" className="glass-panel p-6 hover:bg-surface/70 transition-colors cursor-pointer">
            <div className="text-4xl mb-2">➕</div>
            <div className="text-lg font-semibold text-white">Add New Person</div>
            <div className="text-sm text-secondary">Register a new employee</div>
          </Link>
          <Link to="/persons" className="glass-panel p-6 hover:bg-surface/70 transition-colors cursor-pointer">
            <div className="text-4xl mb-2">👥</div>
            <div className="text-lg font-semibold text-white">View All Persons</div>
            <div className="text-sm text-secondary">Manage registered persons</div>
          </Link>
          <Link to="/verification" className="glass-panel p-6 hover:bg-surface/70 transition-colors cursor-pointer">
            <div className="text-4xl mb-2">✅</div>
            <div className="text-lg font-semibold text-white">Verification</div>
            <div className="text-sm text-secondary">Check-in / Check-out</div>
          </Link>
        </div>

        {/* Today's Attendance Table */}
        <div className="glass-panel p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Today's Attendance Log</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-secondary text-sm">Name</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Department</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Check-in</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Check-out</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Status</th>
                </tr>
              </thead>
              <tbody>
                {todayAttendance.map((record) => (
                  <tr key={record.id} className="border-b border-white/5 hover:bg-surface/30">
                    <td className="py-3 px-4 text-white">{record.person_name}</td>
                    <td className="py-3 px-4 text-slate-300">{record.department}</td>
                    <td className="py-3 px-4 text-slate-300">{record.check_in}</td>
                    <td className="py-3 px-4 text-slate-300">{record.check_out || '-'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${record.status === 'on_time' ? 'bg-green-500/20 text-green-400' : 'bg-yellow-500/20 text-yellow-400'
                        }`}>
                        {record.status === 'on_time' ? 'On Time' : 'Late'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
