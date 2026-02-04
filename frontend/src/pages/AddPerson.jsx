import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import toast from 'react-hot-toast'
import Navbar from '../components/Navbar'

function AddPerson() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    employee_id: '',
    date_of_birth: '',
    gender: '',
    department: '',
    email: '',
    phone: ''
  })
  const [faceFile, setFaceFile] = useState(null)
  const [voiceFile, setVoiceFile] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.name || !faceFile) {
      toast.error('Name and face image are required')
      return
    }

    setLoading(true)
    const data = new FormData()

    // Append form fields
    Object.keys(formData).forEach(key => {
      if (formData[key]) data.append(key, formData[key])
    })

    // Append files
    if (faceFile) data.append('face', faceFile)
    if (voiceFile) data.append('voice', voiceFile)

    try {
      await axios.post('http://localhost:5001/api/persons', data)
      toast.success('Person registered successfully!')
      navigate('/persons')
    } catch (error) {
      console.error(error)
      toast.error('Failed to register person')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-darker">
      <Navbar />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Add New Person</h1>
          <p className="text-secondary">Register a new employee with biometric data</p>
        </div>

        <form onSubmit={handleSubmit} className="glass-panel p-8">
          {/* Personal Information */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-4">Personal Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Full Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="input-field"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Employee ID</label>
                <input
                  type="text"
                  value={formData.employee_id}
                  onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Date of Birth</label>
                <input
                  type="date"
                  value={formData.date_of_birth}
                  onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Gender</label>
                <select
                  value={formData.gender}
                  onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
                  className="input-field"
                >
                  <option value="">Select...</option>
                  <option value="Male">Male</option>
                  <option value="Female">Female</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Department</label>
                <select
                  value={formData.department}
                  onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                  className="input-field"
                >
                  <option value="">Select...</option>
                  <option value="Engineering">Engineering</option>
                  <option value="Marketing">Marketing</option>
                  <option value="Sales">Sales</option>
                  <option value="HR">HR</option>
                  <option value="Finance">Finance</option>
                  <option value="Operations">Operations</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="input-field"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium mb-2">Phone</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="input-field"
                />
              </div>
            </div>
          </div>

          {/* Biometric Data */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-4">Biometric Data</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Face Image *</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setFaceFile(e.target.files[0])}
                  className="input-field"
                  required
                />
                {faceFile && (
                  <div className="mt-2 p-2 bg-green-500/20 text-green-400 rounded text-sm">
                    ✓ {faceFile.name}
                  </div>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Voice Recording</label>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={(e) => setVoiceFile(e.target.files[0])}
                  className="input-field"
                />
                {voiceFile && (
                  <div className="mt-2 p-2 bg-green-500/20 text-green-400 rounded text-sm">
                    ✓ {voiceFile.name}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex-1"
            >
              {loading ? 'Registering...' : 'Register Person'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/persons')}
              className="px-6 py-3 bg-surface hover:bg-surface/70 text-white rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddPerson
