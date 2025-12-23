from flask import Flask, jsonify
from flask_cors import CORS
from api.view import users

def create_app():
    app=Flask(__name__)
    app.register_blueprint(users)
    CORS(app,origins="*")
    
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "status": "success",
            "message": "Tamil-English Translator API",
            "version": "1.0",
            "endpoints": {
                "translate": {
                    "method": "POST",
                    "url": "/user/translate",
                    "description": "Translate Tamil text to English",
                    "example": {"TamilText": "வணக்கம்"}
                },
                "transcribe": {
                    "method": "POST",
                    "url": "/user/transcribe",
                    "description": "Transcribe audio to text",
                    "body": "multipart/form-data with 'audio' field"
                },
                "transcribe_and_translate": {
                    "method": "POST",
                    "url": "/user/transcribe-and-translate",
                    "description": "Transcribe Tamil audio and translate to English",
                    "body": "multipart/form-data with 'audio' field"
                }
            }
        }), 200
    
    return app
