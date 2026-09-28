"""RecallOps Flask application factory."""

import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    app.config["MAX_CONTENT_LENGTH"] = (
        int(os.getenv("MAX_CONTENT_LENGTH_MB", "50")) * 1024 * 1024
    )

    # Ensure upload and chart directories exist
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    chart_dir = os.path.join(os.path.dirname(__file__), "static", "img", "charts")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(chart_dir, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_dir
    app.config["CHART_FOLDER"] = chart_dir

    # Database
    db_path = os.getenv("DATABASE_PATH", "data/recallops.db")
    abs_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_path)
    os.makedirs(os.path.dirname(abs_db_path), exist_ok=True)
    app.config["DATABASE_PATH"] = abs_db_path

    # Ollama config
    app.config["OLLAMA_BASE_URL"] = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )
    app.config["OLLAMA_MODEL"] = os.getenv("OLLAMA_MODEL", "llama3.2")
    app.config["OLLAMA_VISION_MODEL"] = os.getenv("OLLAMA_VISION_MODEL", "llava")
    app.config["MAX_VIDEO_DURATION_SECONDS"] = int(
        os.getenv("MAX_VIDEO_DURATION_SECONDS", "60")
    )
    app.config["VIDEO_SAMPLE_FRAMES"] = int(os.getenv("VIDEO_SAMPLE_FRAMES", "5"))

    # Initialize database
    from app.services.database import init_db

    init_db(app.config["DATABASE_PATH"])

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.cases import cases_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(cases_bp, url_prefix="/cases")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
