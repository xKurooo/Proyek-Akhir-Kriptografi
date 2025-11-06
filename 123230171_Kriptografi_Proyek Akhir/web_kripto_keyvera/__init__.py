# web_kripto_keyvera/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """
    Factory to create Flask app.
    Registers blueprints that we'll create in web_kripto_keyvera/routes/.
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    # Load configuration from config.py
    app.config.from_object('web_kripto_keyvera.config.Config')

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (routes). These modules will be created next.
    # Register main pages first, then auth, crypto, stego
    from .routes.main_routes import main_bp
    from .routes.auth_routes import auth_bp
    from .routes.crypto_routes import crypto_bp
    from .routes.stego_routes import stego_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(crypto_bp, url_prefix='/crypto')
    app.register_blueprint(stego_bp, url_prefix='/stego')

    # Ensure database tables exist (mirrors behavior in original app.py)
    with app.app_context():
        db.create_all()

    return app