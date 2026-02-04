import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'
import Navbar from '../components/Navbar'

function Verification() {
  const [faceFile, setFaceFile] = useState(null)
  const [voiceFile, setVoiceFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const handleVerify = async () => {
    if (!faceFile && !voiceFile) {
      toast.error('Please upload at least one biometric file')
      return
    }

    setLoading(true)
    setResult(null)

    const formData = new FormData()
    if (faceFile) formData.append('face', faceFile)
    if (voiceFile) formData.append('voice', voiceFile)

    try {
      const response = await axios.post('http://localhost:5001/api/attendance/checkin', formData)

      if (response.data.verified) {
        setResult(response.data)
        const person = response.data.person
        const time = response.data.attendance.check_in
        toast.success(`Welcome, ${person.name}! Checked in at ${time}`)
      } else {
        toast.error('Verification failed. No matching person found.')
        setResult(response.data)
      }
    } catch (error) {
      console.error(error)
      toast.error('Verification failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-darker">
      <Navbar />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Biometric Verification</h1>
          <p className="text-secondary">Check-in with face and/or voice recognition</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Face Upload */}
          <div className="glass-panel p-6">
            <h3 className="text-lg font-semibold text-white mb-4">👤 Face Identification</h3>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFaceFile(e.target.files[0])}
              className="input-field mb-4"
            />
            {faceFile && (
              <div className="p-3 bg-green-500/20 text-green-400 rounded text-sm">
                ✓ {faceFile.name}
              </div>
            )}
          </div>

          {/* Voice Upload */}
          <div className="glass-panel p-6">
            <h3 className="text-lg font-semibold text-white mb-4">🎤 Voice Verification</h3>
            <input
              type="file"
              accept="audio/*"
              onChange={(e) => setVoiceFile(e.target.files[0])}
              className="input-field mb-4"
            />
            {voiceFile && (
              <div className="p-3 bg-green-500/20 text-green-400 rounded text-sm">
                ✓ {voiceFile.name}
              </div>
            )}
          </div>
        </div>

        {/* Verify Button */}
        <button
          onClick={handleVerify}
          disabled={loading}
          className="btn-primary w-full mb-8"
        >
          {loading ? 'Verifying...' : '✅ CHECK IN'}
        </button>

        {/* Results */}
        {result && (
          <div className="glass-panel p-8">
            {result.verified ? (
              <div>
                <div className="text-center mb-6">
                  <div className="w-20 h-20 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-4xl">✓</span>
                  </div>
                  <h2 className="text-2xl font-bold text-green-400 mb-2">ACCESS GRANTED</h2>
                  <p className="text-secondary">Identity verified successfully</p>
                </div>

                {/* Person Info */}
                <div className="bg-surface/50 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-semibold text-white mb-4">Identified Person</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-secondary text-sm">Name</div>
                      <div className="text-white font-medium">{result.person.name}</div>
                    </div>
                    <div>
                      <div className="text-secondary text-sm">Employee ID</div>
                      <div className="text-white font-medium">{result.person.employee_id}</div>
                    </div>
                    <div>
                      <div className="text-secondary text-sm">Department</div>
                      <div className="text-white font-medium">{result.person.department}</div>
                    </div>
                    <div>
                      <div className="text-secondary text-sm">Check-in Time</div>
                      <div className="text-white font-medium">{result.attendance.check_in}</div>
                    </div>
                  </div>
                </div>

                {/* Scores */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-secondary text-sm mb-1">Face Score</div>
                    <div className="text-2xl font-bold text-blue-400">
                      {(result.scores.face * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-secondary text-sm mb-1">Voice Score</div>
                    <div className="text-2xl font-bold text-purple-400">
                      {(result.scores.voice * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-secondary text-sm mb-1">Fused Score</div>
                    <div className="text-2xl font-bold text-green-400">
                      {(result.scores.fused * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center">
                <div className="w-20 h-20 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-4xl">✗</span>
                </div>
                <h2 className="text-2xl font-bold text-red-400 mb-2">ACCESS DENIED</h2>
                <p className="text-secondary mb-6">{result.message}</p>

                <div className="grid grid-cols-3 gap-4">
                  <div className="text-center">
                    <div className="text-secondary text-sm mb-1">Face Score</div>
                    <div className="text-2xl font-bold text-slate-400">
                      {(result.scores.face * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-secondary text-sm mb-1">Voice Score</div>
                    <div className="text-2xl font-bold text-slate-400">
                      {(result.scores.voice * 100).toFixed(0)}%
                    </div>
                  </div>
                  <div className="text-center">
                    <div className="text-secondary text-sm mb-1">Fused Score</div>
                    <div className="text-2xl font-bold text-slate-400">
                      {(result.scores.fused * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Verification
