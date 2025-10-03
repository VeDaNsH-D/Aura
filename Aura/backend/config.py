import os
from dotenv import load_dotenv

# Load environment variables from a .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """
    Base configuration class.
    Loads settings from environment variables for security.
    """

    # --- Flask & General App Settings ---

    # Secret key for signing sessions and other security-related needs
    # IMPORTANT: Should be a long, random string.
    SECRET_KEY = os.getenv('SECRET_KEY', 'a-very-secret-key-for-dev')

    # --- Database Settings (PostgreSQL) ---

    # Database connection string
    # Example for PostgreSQL: postgresql://username:password@hostname:port/database_name
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/campus_db')

    # Disable SQLAlchemy event system to save resources as it's not needed by default
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Celery (Background Task Queue) Settings ---

    # URL for the message broker (Redis)
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')

    # URL for the result backend (Redis)
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
