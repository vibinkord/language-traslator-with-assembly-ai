# API Documentation

## Base URL
`http://localhost:5000`

## Endpoints

### 1. Text Translation
**POST** `/user/translate`

**Request:**
```json
{
  "TamilText": "நமस்ते"
}
```
OR
```json
{
  "EnglishText": "Hello"
}
```

**Response:**
```json
{
  "Tamil Text": "நமஸ்கரம்",
  "English Text": "Hello"
}
```

---

### 2. Audio Transcription & Translation
**POST** `/user/transcribe-and-translate`

**Parameters:**
- `audio` (file) - Audio file (WAV, MP3, etc.)
- `target_language` (string) - `en` for English, `ta` for Tamil

**Request (form-data):**
```
audio: <audio_file>
target_language: en
```

**Response:**
```json
{
  "Tamil Text": "வணக்கம்",
  "English Text": "Hello"
}
```

---

### 3. Audio Transcription Only
**POST** `/user/transcribe`

**Parameters:**
- `audio` (file) - Audio file

**Response:**
```json
{
  "transcribed_text": "Hello world",
  "status": "success"
}
```

---

### 4. API Documentation
**GET** `/`

Returns list of all available endpoints with descriptions.

**Response:**
```json
{
  "message": "Tamil-English Translator API",
  "endpoints": {
    "/user/translate": "POST - Translate Tamil/English text",
    "/user/transcribe": "POST - Transcribe audio to text",
    "/user/transcribe-and-translate": "POST - Transcribe and translate audio"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Please provide either TamilText or EnglishText"
}
```

### 500 Internal Server Error
```json
{
  "error": "Transcription failed: API key invalid"
}
```

## Rate Limiting

- AssemblyAI limits based on your plan
- Check https://www.assemblyai.com/ for current limits

## Headers

All requests should include:
```
Content-Type: application/json
```

For file uploads:
```
Content-Type: multipart/form-data
```

## Example Usage

### Python
```python
import requests

response = requests.post(
    'http://localhost:5000/user/translate',
    json={'TamilText': 'வணக்கம்'}
)
print(response.json())
```

### JavaScript (Fetch)
```javascript
fetch('http://localhost:5000/user/translate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({TamilText: 'வணக்கம்'})
})
.then(r => r.json())
.then(data => console.log(data))
```

### cURL
```bash
curl -X POST http://localhost:5000/user/translate \
  -H "Content-Type: application/json" \
  -d '{"TamilText":"வணக்கம்"}'
```
