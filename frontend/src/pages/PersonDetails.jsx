import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { format, parseISO } from 'date-fns'
import Navbar from '../components/Navbar'

function PersonDetails() {
  const { id } = useParams()
  const [person, setPerson] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [id])

  const fetchData = async () => {
    try {
      const [personRes, analyticsRes] = await Promise.all([
        axios.get(`http://localhost:5001/api/persons/${id}`),
        axios.get(`http://localhost:5001/api/analytics/person/${id}`)
      ])

      setPerson(personRes.data)
      setAnalytics(analyticsRes.data)
    } catch (error) {
      console.error('Error fetching person details:', error)
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

  if (!person) {
    return (
      <div className="min-h-screen bg-darker">
        <Navbar />
        <div className="flex items-center justify-center h-96">
          <div className="text-white">Person not found</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-darker">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Person Info Card */}
        <div className="glass-panel p-8 mb-8">
          <div className="flex items-start gap-6">
            <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-4xl text-white">
              {person.name.charAt(0)}
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-white mb-2">{person.name}</h1>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <div className="text-secondary">Employee ID</div>
                  <div className="text-white">{person.employee_id}</div>
                </div>
                <div>
                  <div className="text-secondary">Department</div>
                  <div className="text-white">{person.department}</div>
                </div>
                <div>
                  <div className="text-secondary">Gender</div>
                  <div className="text-white">{person.gender || '-'}</div>
                </div>
                <div>
                  <div className="text-secondary">Email</div>
                  <div className="text-white">{person.email || '-'}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Total Days Present</div>
            <div className="text-3xl font-bold text-white">{analytics?.stats.total_days_present || 0}</div>
          </div>
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Attendance %</div>
            <div className="text-3xl font-bold text-green-400">{analytics?.stats.attendance_percentage || 0}%</div>
          </div>
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">On Time</div>
            <div className="text-3xl font-bold text-blue-400">{analytics?.stats.on_time_count || 0}</div>
          </div>
          <div className="glass-panel p-6">
            <div className="text-secondary text-sm mb-1">Late Count</div>
            <div className="text-3xl font-bold text-yellow-400">{analytics?.stats.late_count || 0}</div>
          </div>
        </div>

        {/* Attendance History */}
        <div className="glass-panel p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Attendance History</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-secondary text-sm">Date</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Check-in</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Check-out</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Status</th>
                </tr>
              </thead>
              <tbody>
                {analytics?.history.slice(0, 20).map((record) => (
                  <tr key={record.id} className="border-b border-white/5 hover:bg-surface/30">
                    <td className="py-3 px-4 text-white">{record.date}</td>
                    <td className="py-3 px-4 text-slate-300">{record.check_in || '-'}</td>
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

export default PersonDetails
