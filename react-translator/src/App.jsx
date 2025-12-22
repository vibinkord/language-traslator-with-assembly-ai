import React, { useState } from 'react'
import axios from 'axios'

// Configure axios to use the Flask backend
const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  }
})

function App() {
  const [activeTab, setActiveTab] = useState('text')
  const [tamilText, setTamilText] = useState('')
  const [englishText, setEnglishText] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [translationMode, setTranslationMode] = useState('tamil-to-english') // or 'english-to-tamil'
  // Audio states
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState(null)
  const [audioFile, setAudioFile] = useState(null)
  const [audioFileName, setAudioFileName] = useState('')
  const [audioMode, setAudioMode] = useState('tamil-to-english') // or 'english-to-tamil'

  // Text Translation
  const handleTranslate = async () => {
    const fromTamil = translationMode === 'tamil-to-english'
    const sourceText = fromTamil ? tamilText : englishText
    
    if (!sourceText.trim()) {
      setError(`Please enter ${fromTamil ? 'Tamil' : 'English'} text to translate`)
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const payload = fromTamil 
        ? { TamilText: sourceText }
        : { EnglishText: sourceText }
      
      const response = await api.post('/user/translate', payload)
      
      if (fromTamil) {
        setEnglishText(response.data['English Text'])
      } else {
        setTamilText(response.data['Tamil Text'])
      }
      setSuccess('Translation successful!')
    } catch (err) {
      console.error('Translation error:', err)
      setError('Translation failed: ' + (err.response?.data?.error || err.message))
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setTamilText('')
    setEnglishText('')
    setError('')
    setSuccess('')
  }

  // Audio Recording
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      const audioChunks = []

      recorder.ondataavailable = (event) => {
        audioChunks.push(event.data)
      }

      recorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' })
        setAudioFile(audioBlob)
        setAudioFileName('recorded-audio.wav')
        stream.getTracks().forEach(track => track.stop())
      }

      recorder.start()
      setMediaRecorder(recorder)
      setIsRecording(true)
      setError('')
    } catch (err) {
      setError('Microphone access denied: ' + err.message)
    }
  }

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop()
      setIsRecording(false)
    }
  }

  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      setAudioFile(file)
      setAudioFileName(file.name)
      setError('')
    }
  }

  const handleTranscribeAndTranslate = async () => {
    if (!audioFile) {
      setError('Please record or upload an audio file first')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const formData = new FormData()
      formData.append('audio', audioFile, audioFileName)
      formData.append('target_language', audioMode === 'tamil-to-english' ? 'en' : 'ta')

      const response = await api.post('/user/transcribe-and-translate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      if (audioMode === 'tamil-to-english') {
        setTamilText(response.data['Tamil Text'])
        setEnglishText(response.data['English Text'])
      } else {
        setEnglishText(response.data['English Text'])
        setTamilText(response.data['Tamil Text'])
      }
      setSuccess('Audio transcribed and translated successfully!')
    } catch (err) {
      console.error('Audio processing error:', err)
      setError('Processing failed: ' + (err.response?.data?.error || err.message))
    } finally {
      setLoading(false)
    }
  }

  const clearAudio = () => {
    setAudioFile(null)
    setAudioFileName('')
    setTamilText('')
    setEnglishText('')
    setError('')
    setSuccess('')
  }

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>🌐 Tamil-English Translator</h1>
          <p>Translate text or transcribe audio with AI</p>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'text' ? 'active' : ''}`}
            onClick={() => setActiveTab('text')}
          >
            📝 Text Translation
          </button>
          <button
            className={`tab ${activeTab === 'audio' ? 'active' : ''}`}
            onClick={() => setActiveTab('audio')}
          >
            🎤 Audio Translation
          </button>
        </div>

        {activeTab === 'text' && (
          <div>
            <div className="mode-selector">
              <label>
                <input
                  type="radio"
                  name="textMode"
                  value="tamil-to-english"
                  checked={translationMode === 'tamil-to-english'}
                  onChange={(e) => {
                    setTranslationMode(e.target.value)
                    handleClear()
                  }}
                />
                தமிழ் → English
              </label>
              <label>
                <input
                  type="radio"
                  name="textMode"
                  value="english-to-tamil"
                  checked={translationMode === 'english-to-tamil'}
                  onChange={(e) => {
                    setTranslationMode(e.target.value)
                    handleClear()
                  }}
                />
                English → தமிழ்
              </label>
            </div>

            <div className="translation-section">
              <div className="input-box">
                <h3>{translationMode === 'tamil-to-english' ? 'Tamil (தமிழ்)' : 'English'}</h3>
                <textarea
                  value={translationMode === 'tamil-to-english' ? tamilText : englishText}
                  onChange={(e) => translationMode === 'tamil-to-english' ? setTamilText(e.target.value) : setEnglishText(e.target.value)}
                  placeholder={`Enter ${translationMode === 'tamil-to-english' ? 'Tamil' : 'English'} text here...`}
                />
              </div>

              <div className="output-box">
                <h3>{translationMode === 'tamil-to-english' ? 'English' : 'Tamil (தமிழ்)'}</h3>
                <textarea
                  value={translationMode === 'tamil-to-english' ? englishText : tamilText}
                  readOnly
                  placeholder="Translation will appear here..."
                />
              </div>
            </div>

            <div className="button-group">
              <button
                className="btn btn-primary"
                onClick={handleTranslate}
                disabled={loading}
              >
                {loading ? <span className="loading"></span> : '🔄'} Translate
              </button>
              <button
                className="btn btn-secondary"
                onClick={handleClear}
                disabled={loading}
              >
                🗑️ Clear
              </button>
            </div>
          </div>
        )}

        {activeTab === 'audio' && (
          <div className="audio-section">
            <div className="mode-selector">
              <label>
                <input
                  type="radio"
                  name="audioMode"
                  value="tamil-to-english"
                  checked={audioMode === 'tamil-to-english'}
                  onChange={(e) => setAudioMode(e.target.value)}
                />
                தமிழ் Audio → English
              </label>
              <label>
                <input
                  type="radio"
                  name="audioMode"
                  value="english-to-tamil"
                  checked={audioMode === 'english-to-tamil'}
                  onChange={(e) => setAudioMode(e.target.value)}
                />
                English Audio → தமிழ்
              </label>
            </div>

            <div className="audio-controls">
              <button
                className={`record-btn ${isRecording ? 'recording' : ''}`}
                onClick={isRecording ? stopRecording : startRecording}
                disabled={loading}
              >
                {isRecording ? '⏹️' : '🎤'}
              </button>
              <div className={`status-text ${isRecording ? 'recording' : ''}`}>
                {isRecording ? '🔴 Recording... Click to stop' : 'Click microphone to record'}
              </div>
            </div>

            <div className="file-upload">
              <div className="file-input-wrapper">
                <input
                  type="file"
                  id="audio-file"
                  className="file-input"
                  accept="audio/*"
                  onChange={handleFileUpload}
                  disabled={loading}
                />
                <label htmlFor="audio-file" className="file-label">
                  📁 Upload Audio File
                </label>
              </div>
              {audioFileName && (
                <div className="file-name">
                  ✓ {audioFileName}
                </div>
              )}
            </div>

            {audioFile && (
              <>
                <div className="button-group">
                  <button
                    className="btn btn-primary"
                    onClick={handleTranscribeAndTranslate}
                    disabled={loading}
                  >
                    {loading ? <span className="loading"></span> : '🎯'} Transcribe & Translate
                  </button>
                  <button
                    className="btn btn-secondary"
                    onClick={clearAudio}
                    disabled={loading}
                  >
                    🗑️ Clear
                  </button>
                </div>

                {(tamilText || englishText) && (
                  <div className="translation-section" style={{ marginTop: '30px' }}>
                    <div className="input-box">
                      <h3>{audioMode === 'tamil-to-english' ? 'Transcribed Tamil' : 'Transcribed English'}</h3>
                      <textarea value={audioMode === 'tamil-to-english' ? tamilText : englishText} readOnly />
                    </div>
                    <div className="output-box">
                      <h3>{audioMode === 'tamil-to-english' ? 'English Translation' : 'Tamil Translation'}</h3>
                      <textarea value={audioMode === 'tamil-to-english' ? englishText : tamilText} readOnly />
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {error && <div className="error">❌ {error}</div>}
        {success && <div className="success">✅ {success}</div>}
      </div>
    </div>
  )
}

export default App
