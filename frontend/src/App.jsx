import { useState } from 'react'
import axios from 'axios'

function App() {
  const [faceFile, setFaceFile] = useState(null)
  const [voiceFile, setVoiceFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleVerify = async () => {
    if (!faceFile && !voiceFile) {
      setError("Please upload at least one biometric file.")
      return
    }
    setError(null)
    setLoading(true)
    setResult(null)

    const formData = new FormData()
    if (faceFile) formData.append('face', faceFile)
    if (voiceFile) formData.append('voice', voiceFile)

    try {
      // Assuming backend is on port 5001
      const response = await axios.post('http://localhost:5001/api/verify', formData)
      setResult(response.data)
    } catch (err) {
      console.error(err)
      setError("Verification failed. Check console for details.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-8 bg-darker flex flex-col items-center">
      {/* Header */}
      <header className="mb-12 text-center">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-indigo-500 mb-2">
          IDentix
        </h1>
        <p className="text-secondary">Multi-Modal Biometric Security Suite</p>
      </header>

      {/* Main Grid */}
      <main className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">

        {/* Face Card */}
        <div className="glass-panel p-6 flex flex-col items-center">
          <div className="w-16 h-16 bg-blue-500/20 rounded-full flex items-center justify-center mb-4">
            <span className="text-2xl">👤</span>
          </div>
          <h2 className="text-xl font-semibold mb-4">Face Identification</h2>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setFaceFile(e.target.files[0])}
            className="input-field"
          />
          {faceFile && (
            <div className="mt-4 p-2 bg-surface rounded text-sm text-green-400">
              Selected: {faceFile.name}
            </div>
          )}
        </div>

        {/* Voice Card */}
        <div className="glass-panel p-6 flex flex-col items-center">
          <div className="w-16 h-16 bg-purple-500/20 rounded-full flex items-center justify-center mb-4">
            <span className="text-2xl">🎙️</span>
          </div>
          <h2 className="text-xl font-semibold mb-4">Voice Verification</h2>
          <input
            type="file"
            accept="audio/*"
            onChange={(e) => setVoiceFile(e.target.files[0])}
            className="input-field"
          />
          {voiceFile && (
            <div className="mt-4 p-2 bg-surface rounded text-sm text-green-400">
              Selected: {voiceFile.name}
            </div>
          )}
        </div>
      </main>

      {/* Action Area */}
      <div className="w-full max-w-md mb-12">
        <button
          onClick={handleVerify}
          disabled={loading}
          className="btn-primary"
        >
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
          ) : "VERIFY IDENTITY"}
        </button>
        {error && <p className="mt-4 text-red-500 text-center">{error}</p>}
      </div>

      {/* Results */}
      {result && (
        <div className={`w-full max-w-2xl glass-panel p-8 border-l-4 ${result.verified ? 'border-green-500' : 'border-red-500'} animate-fade-in`}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-2xl font-bold">Authentication Result</h3>
              <p className="text-secondary">Fusion Analysis Complete</p>
            </div>
            <div className={`px-4 py-2 rounded-full font-bold ${result.verified ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'}`}>
              {result.verified ? "ACCESS GRANTED" : "ACCESS DENIED"}
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-4 bg-dark/30 rounded-lg">
              <div className="text-sm text-secondary">Face Score</div>
              <div className="text-xl font-mono text-blue-400">{(result.scores.face * 100).toFixed(1)}%</div>
            </div>
            <div className="p-4 bg-dark/30 rounded-lg">
              <div className="text-sm text-secondary">Voice Score</div>
              <div className="text-xl font-mono text-purple-400">{(result.scores.voice * 100).toFixed(1)}%</div>
            </div>
            <div className="p-4 bg-dark/30 rounded-lg border border-white/5">
              <div className="text-sm text-secondary">Fused Score</div>
              <div className={`text-xl font-mono font-bold ${result.verified ? 'text-green-400' : 'text-red-400'}`}>
                {(result.scores.fused * 100).toFixed(1)}%
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
