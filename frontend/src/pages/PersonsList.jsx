import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import Navbar from '../components/Navbar'

function PersonsList() {
  const [persons, setPersons] = useState([])
  const [filteredPersons, setFilteredPersons] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [departmentFilter, setDepartmentFilter] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPersons()
  }, [])

  useEffect(() => {
    filterPersons()
  }, [searchTerm, departmentFilter, persons])

  const fetchPersons = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/persons')
      setPersons(response.data.persons)
      setFilteredPersons(response.data.persons)
    } catch (error) {
      console.error('Error fetching persons:', error)
    } finally {
      setLoading(false)
    }
  }

  const filterPersons = () => {
    let filtered = persons

    if (searchTerm) {
      filtered = filtered.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.employee_id.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    if (departmentFilter) {
      filtered = filtered.filter(p => p.department === departmentFilter)
    }

    setFilteredPersons(filtered)
  }

  const departments = [...new Set(persons.map(p => p.department))]

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

  return (
    <div className="min-h-screen bg-darker">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">All Persons</h1>
            <p className="text-secondary">{filteredPersons.length} registered persons</p>
          </div>
          <Link to="/persons/add" className="btn-primary">
            ➕ Add New Person
          </Link>
        </div>

        {/* Filters */}
        <div className="glass-panel p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="Search by name or employee ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field"
            />
            <select
              value={departmentFilter}
              onChange={(e) => setDepartmentFilter(e.target.value)}
              className="input-field"
            >
              <option value="">All Departments</option>
              {departments.map(dept => (
                <option key={dept} value={dept}>{dept}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Persons Table */}
        <div className="glass-panel p-6">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/10">
                  <th className="text-left py-3 px-4 text-secondary text-sm">Name</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Employee ID</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Department</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Email</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Status</th>
                  <th className="text-left py-3 px-4 text-secondary text-sm">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredPersons.map((person) => (
                  <tr key={person.id} className="border-b border-white/5 hover:bg-surface/30 transition-colors">
                    <td className="py-3 px-4 text-white font-medium">{person.name}</td>
                    <td className="py-3 px-4 text-slate-300">{person.employee_id}</td>
                    <td className="py-3 px-4 text-slate-300">{person.department}</td>
                    <td className="py-3 px-4 text-slate-300">{person.email || '-'}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded text-xs ${person.status === 'active'
                          ? 'bg-green-500/20 text-green-400'
                          : 'bg-gray-500/20 text-gray-400'
                        }`}>
                        {person.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <Link
                        to={`/persons/${person.id}`}
                        className="text-blue-400 hover:text-blue-300 text-sm"
                      >
                        View Details →
                      </Link>
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

export default PersonsList
