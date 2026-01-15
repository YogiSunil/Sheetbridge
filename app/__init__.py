from flask import Flask
from dotenv import load_dotenv
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["API_KEY"] = os.getenv("API_KEY", "")
    app.config["GOOGLE_CREDENTIALS_PATH"] = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials/service_account.json")

    Limiter(
        get_remote_address,
        app=app,
        default_limits=["30 per minute"]
    )

    from app.routes import api_bp
    app.register_blueprint(api_bp)

    return app
