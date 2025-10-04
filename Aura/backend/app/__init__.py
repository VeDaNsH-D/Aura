from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .models import db  # Import db instance from models.py
from config import Config

# Initialize extensions but do not attach them to an app yet
migrate = Migrate()

def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.
    This pattern is known as the 'Application Factory'.
    """
    app = Flask(__name__)

    # --- 1. Load Configuration ---
    # Load configuration from the 'config.py' file/class
    app.config.from_object(config_class)

    # --- 2. Initialize Extensions ---
    # Initialize SQLAlchemy with the app
    db.init_app(app)
    # Initialize Flask-Migrate for database migrations
    migrate.init_app(app, db)

    # --- 3. Register Blueprints ---
    # Blueprints help in organizing a large application into smaller, manageable parts.
    from .api import api_bp  # Import the API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # --- 4. Shell Context for easy debugging ---
    # This makes 'db' and your models available in the 'flask shell' command
    # without needing to import them manually.
    @app.shell_context_processor
    def make_shell_context():
        from .models import Entity, Identifier, Event
        return {'db': db, 'Entity': Entity, 'Identifier': Identifier, 'Event': Event}

    return app