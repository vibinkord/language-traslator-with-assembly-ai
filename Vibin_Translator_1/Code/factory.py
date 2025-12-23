import os
from flask import Flask, jsonify
import os
from flask_cors import CORS
from dotenv import load_dotenv


def create_app() -> Flask:
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # Enable CORS for all routes (frontend dev server on 3001/3002)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register API blueprint
    from api.view import api_bp
    app.register_blueprint(api_bp)

    # Root endpoint to describe the API
    @app.get("/")
    def index():
        return jsonify({
        from pathlib import Path
            "message": "Tamil-English Translator API",
            "endpoints": {
                "/user/translate": "POST - Translate Tamil/English text",
                "/user/transcribe": "POST - Transcribe audio to text (English)",
                "/user/transcribe-and-translate": "POST - Transcribe and translate audio"
            }
            # Load environment variables from both backend folder and repo root
            backend_dir = Path(__file__).resolve().parent
            repo_root = backend_dir.parent.parent
            # Load root .env first (so local backend .env can override)
            load_dotenv(dotenv_path=repo_root / ".env", override=False)
            load_dotenv(dotenv_path=backend_dir / ".env", override=False)
            # Also load from process env and default working dir
            load_dotenv(override=False)
    # Simple health endpoint to verify environment
    @app.get("/health")
    def health():
        key_present = bool(os.getenv("ASSEMBLYAI_API_KEY", ""))
        return jsonify({
            "ok": True,
            "assemblyai_key_present": key_present
        })

    return app
