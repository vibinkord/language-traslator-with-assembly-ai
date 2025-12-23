import os
import tempfile
from flask import Blueprint, request, jsonify
from translate import Translator
from dotenv import load_dotenv
import assemblyai as aai

api_bp = Blueprint("api", __name__)

# Ensure env loaded if factory not yet called
load_dotenv()

def _ensure_aai_key():
    # Refresh the API key from environment in case server started from different cwd
    key = os.getenv("ASSEMBLYAI_API_KEY", "")
    if aai.settings.api_key != key:
        aai.settings.api_key = key


def _make_translator(to_lang: str):
    # translate library uses language codes like 'en', 'ta'
    return Translator(to_lang=to_lang)


@api_bp.post("/user/translate")
def translate_text():
    try:
        data = request.get_json(silent=True) or {}
        tamil_text = data.get("TamilText")
        english_text = data.get("EnglishText")

        if not tamil_text and not english_text:
            return jsonify({"error": "Please provide either TamilText or EnglishText"}), 400

        if tamil_text:
            # Tamil -> English
            translator = _make_translator("en")
            translated = translator.translate(tamil_text)
            return jsonify({
                "Tamil Text": tamil_text,
                "English Text": translated
            })
        else:
            # English -> Tamil
            translator = _make_translator("ta")
            translated = translator.translate(english_text)
            return jsonify({
                "Tamil Text": translated,
                "English Text": english_text
            })
    except Exception as e:
        return jsonify({"error": f"Translation failed: {e}"}), 500


@api_bp.post("/user/transcribe")
def transcribe_audio():
    _ensure_aai_key()
    if not aai.settings.api_key:
        return jsonify({"error": "Missing ASSEMBLYAI_API_KEY in environment"}), 500

    if "audio" not in request.files:
        return jsonify({"error": "Please upload an audio file as 'audio'"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as tmp:
            audio_path = tmp.name
            audio_file.save(audio_path)

        transcriber = aai.Transcriber()
        # Force English STT as discussed
        config = aai.TranscriptionConfig(language_code="en")
        transcript = transcriber.transcribe(audio_path, config=config)

        text = transcript.text or ""
        return jsonify({
            "transcribed_text": text,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {e}"}), 500
    finally:
        try:
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception:
            pass


@api_bp.post("/user/transcribe-and-translate")
def transcribe_and_translate():
    _ensure_aai_key()
    if not aai.settings.api_key:
        return jsonify({"error": "Missing ASSEMBLYAI_API_KEY in environment"}), 500

    if "audio" not in request.files:
        return jsonify({"error": "Please upload an audio file as 'audio'"}), 400

    target_language = request.form.get("target_language", "en").strip().lower()
    if target_language not in {"en", "ta"}:
        return jsonify({"error": "target_language must be 'en' or 'ta'"}), 400

    audio_file = request.files["audio"]
    if audio_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as tmp:
            audio_path = tmp.name
            audio_file.save(audio_path)

        transcriber = aai.Transcriber()
        config = aai.TranscriptionConfig(language_code="en")
        transcript = transcriber.transcribe(audio_path, config=config)
        text = (transcript.text or "").strip()

        if not text:
            return jsonify({"error": "No transcription text produced"}), 500

        if target_language == "en":
            translator = _make_translator("en")
            english_text = text
            tamil_text = _make_translator("ta").translate(text)
        else:
            translator = _make_translator("ta")
            tamil_text = translator.translate(text)
            english_text = text

        return jsonify({
            "Tamil Text": tamil_text,
            "English Text": english_text
        })
    except Exception as e:
        return jsonify({"error": f"Transcribe+Translate failed: {e}"}), 500
    finally:
        try:
            if 'audio_path' in locals() and os.path.exists(audio_path):
                os.remove(audio_path)
        except Exception:
            pass
