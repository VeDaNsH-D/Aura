import os
from app import create_app, db
from celery import Celery

def make_celery(app):
    """
    Celery configuration factory.
    This ties the Celery instance to the Flask application context.
    """
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['app.tasks.alerting'] # Tell Celery where to find tasks
    )
    celery.conf.update(app.config)

    # --- Configure the periodic task schedule (Celery Beat) ---
    celery.conf.beat_schedule = {
        'check-inactivity-every-hour': {
            'task': 'tasks.check_inactive_entities',
            'schedule': 3600.0,  # Time in seconds (3600s = 1 hour)
        },
    }
    celery.conf.timezone = 'UTC'

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Create the Flask app and then the Celery instance
flask_app = create_app()
celery = make_celery(flask_app)