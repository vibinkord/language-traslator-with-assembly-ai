from flask import request, Blueprint, jsonify
from translate import Translator
import assemblyai as aai
import os
from dotenv import load_dotenv

load_dotenv()

users = Blueprint("api", __name__, url_prefix="/user")

# Set up AssemblyAI API key
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "")
if ASSEMBLYAI_API_KEY:
    aai.settings.api_key = ASSEMBLYAI_API_KEY


@users.route("/translate", methods=["POST"])
def translate():
    try:
        # Get text from the JSON body
        data = request.get_json()
        tamil_text = data.get("TamilText", "")
        english_text = data.get("EnglishText", "")

        if not tamil_text and not english_text:
            return jsonify({
                "error": "Provide either TamilText or EnglishText"
            }), 400

        if tamil_text:
            # Translate Tamil to English
            translator = Translator(from_lang="ta", to_lang="en")
            english_translation = translator.translate(tamil_text)
            return jsonify({
                "Tamil Text": tamil_text,
                "English Text": english_translation
            }), 200
        elif english_text:
            # Translate English to Tamil
            translator = Translator(from_lang="en", to_lang="ta")
            tamil_translation = translator.translate(english_text)
            return jsonify({
                "English Text": english_text,
                "Tamil Text": tamil_translation
            }), 200
    except Exception as e:
        return jsonify({
            "error": f"Translation failed: {str(e)}"
        }), 400

@users.route("/transcribe", methods=["POST"])
def transcribe_audio():
    """
    Transcribe audio file using AssemblyAI
    Expects: audio file in form data with key 'audio'
    Returns: Transcribed text
    """
    try:
        if "audio" not in request.files:
            return jsonify({
                "error": "No audio file provided"
            }), 400
        
        audio_file = request.files["audio"]
        
        if audio_file.filename == "":
            return jsonify({
                "error": "No selected file"
            }), 400
        
        if not ASSEMBLYAI_API_KEY:
            return jsonify({
                "error": "AssemblyAI API key not configured"
            }), 500
        
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            temp_path = tmp.name
        
        try:
            # Transcribe the audio
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(temp_path)
            
            # Clean up temp file
            os.remove(temp_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                return jsonify({
                    "error": f"Transcription failed: {transcript.error}"
                }), 400
            
            return jsonify({
                "transcribed_text": transcript.text,
                "status": "success"
            }), 200
        
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
    
    except Exception as e:
        return jsonify({
            "error": f"Error transcribing audio: {str(e)}"
        }), 500


@users.route("/transcribe-and-translate", methods=["POST"])
def transcribe_and_translate():
    """
    Transcribe audio and translate to target language
    Expects: audio file in form data with key 'audio'
             target_language in form data (en or ta, defaults to en)
    """
    try:
        if "audio" not in request.files:
            return jsonify({
                "error": "No audio file provided"
            }), 400
        
        audio_file = request.files["audio"]
        target_language = request.form.get("target_language", "en")  # Default to English
        
        if audio_file.filename == "":
            return jsonify({
                "error": "No selected file"
            }), 400
        
        if not ASSEMBLYAI_API_KEY:
            return jsonify({
                "error": "AssemblyAI API key not configured"
            }), 500
        
        # Save temporary file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            temp_path = tmp.name
        
        try:
            # Transcribe the audio - try to detect language
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(temp_path)
            
            # Clean up temp file
            os.remove(temp_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                return jsonify({
                    "error": f"Transcription failed: {transcript.error}"
                }), 400
            
            transcribed_text = transcript.text
            
            # Determine source language and translate
            if target_language == "en":
                # Assume audio is Tamil, translate to English
                translator = Translator(from_lang="ta", to_lang="en")
                translated_text = translator.translate(transcribed_text)
                return jsonify({
                    "Tamil Text": transcribed_text,
                    "English Text": translated_text,
                    "status": "success"
                }), 200
            elif target_language == "ta":
                # Assume audio is English, translate to Tamil
                translator = Translator(from_lang="en", to_lang="ta")
                translated_text = translator.translate(transcribed_text)
                return jsonify({
                    "English Text": transcribed_text,
                    "Tamil Text": translated_text,
                    "status": "success"
                }), 200
            else:
                return jsonify({
                    "error": "Invalid target language. Use 'en' or 'ta'"
                }), 400
        
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise e
    
    except Exception as e:
        return jsonify({
            "error": f"Error processing audio: {str(e)}"
        }), 500