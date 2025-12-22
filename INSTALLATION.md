# Tamil-English Translator - Installation Guide

## Prerequisites
- Python 3.8+
- Node.js 14+
- Git

## Backend Setup

1. **Navigate to backend directory:**
```bash
cd Vibin_Translator_1/Code
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your AssemblyAI API key
```

5. **Run backend:**
```bash
python main.py
```
Backend will start on `http://localhost:5000`

## Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd react-translator
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run development server:**
```bash
npm run dev
```
Frontend will start on `http://localhost:3002` (or available port)

## Full Stack Startup

**Easy way - use startup script:**
```bash
bash start-all.sh
```

This starts both Flask backend and React frontend automatically.

## Troubleshooting

### Port Already in Use
If port 5000 or 3001/3002 is busy:
- Close other applications using those ports
- Or modify `vite.config.js` for custom port

### AssemblyAI API Key Error
- Verify API key is correct in `.env`
- Check https://www.assemblyai.com/ for API status
- Restart Flask server after adding key

### CORS Errors
- Flask-CORS should handle this, but verify CORS is enabled in `factory.py`

### Module Not Found
- Ensure you activated the virtual environment
- Run `pip install -r requirements.txt` again

## Environment Variables

### Backend (.env)
```
ASSEMBLYAI_API_KEY=your_key_here
FLASK_ENV=development
DEBUG=True
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## Testing Endpoints

### Text Translation
```bash
curl -X POST http://localhost:5000/user/translate \
  -H "Content-Type: application/json" \
  -d '{"TamilText": "நमस्ते"}'
```

### Audio Transcription
```bash
curl -X POST http://localhost:5000/user/transcribe-and-translate \
  -F "audio=@audio.wav" \
  -F "target_language=en"
```

## Production Deployment

See `DEPLOYMENT.md` for cloud deployment instructions.
