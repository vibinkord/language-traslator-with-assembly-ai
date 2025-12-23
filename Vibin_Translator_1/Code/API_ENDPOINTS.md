# API Endpoints Documentation

## Existing Endpoints

### 1. Text Translation
**POST** `/user/translate`

Translate Tamil text to English.

**Request:**
```json
{
  "TamilText": "வணக்கம்"
}
```

**Response:**
```json
{
  "Tamil Text": "வணக்கம்",
  "English Text": "Hello"
}
```

---

## New AssemblyAI Integration Endpoints

### 2. Audio Transcription
**POST** `/user/transcribe`

Transcribe audio file to text using AssemblyAI.

**Request:**
- Form data with key `audio` containing the audio file (WAV, MP3, M4A, etc.)

**Response:**
```json
{
  "transcribed_text": "Hello world",
  "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST -F "audio=@audio.wav" http://localhost:5000/user/transcribe
```

---

### 3. Audio Transcription + Translation
**POST** `/user/transcribe-and-translate`

Transcribe Tamil audio and translate to English in one request.

**Request:**
- Form data with key `audio` containing the Tamil audio file

**Response:**
```json
{
  "Tamil Text": "வணக்கம்",
  "English Text": "Hello",
  "status": "success"
}
```

**Example cURL:**
```bash
curl -X POST -F "audio=@tamil_audio.wav" http://localhost:5000/user/transcribe-and-translate
```

---

## Setup Instructions

1. **Get AssemblyAI API Key:**
   - Visit https://www.assemblyai.com/
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Configure Environment:**
   - Copy `.env.example` to `.env`
   - Add your AssemblyAI API key to `.env`

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python main.py
   ```

---

## Supported Audio Formats
- WAV
- MP3
- M4A
- FLAC
- OGG
- ULAW
- And more (AssemblyAI supports all common formats)

## Error Handling
All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing data, invalid audio)
- `500`: Server error (API key not configured, processing error)
