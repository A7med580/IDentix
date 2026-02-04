import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import toast from 'react-hot-toast'

function AdminLogin() {
  const [faceFile, setFaceFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleLogin = async () => {
    if (!faceFile) {
      toast.error('Please upload your face image')
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('face', faceFile)

    try {
      const response = await axios.post('http://localhost:5001/api/admin/login', formData)

      if (response.data.success) {
        localStorage.setItem('admin', JSON.stringify(response.data.admin))
        toast.success(`Welcome, ${response.data.admin.name}!`)
        navigate('/dashboard')
      }
    } catch (error) {
      console.error(error)
      toast.error('Authentication failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-darker flex items-center justify-center p-8">
      <div className="glass-panel p-12 max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500 mb-2">
            IDentix Admin
          </h1>
          <p className="text-secondary">Secure Face Authentication</p>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Admin Face Image</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFaceFile(e.target.files[0])}
            className="input-field"
          />
          {faceFile && (
            <div className="mt-4 p-3 bg-surface rounded text-sm text-green-400">
              ✓ {faceFile.name}
            </div>
          )}
        </div>

        <button
          onClick={handleLogin}
          disabled={loading}
          className="btn-primary"
        >
          {loading ? 'Authenticating...' : 'Login as Admin'}
        </button>
      </div>
    </div>
  )
}

export default AdminLogin
