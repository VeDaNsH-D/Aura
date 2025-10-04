import logging
from datetime import datetime, timedelta
from celery import shared_task
from ..models import db, Event, Entity

# It's good practice to get the logger for the current module
log = logging.getLogger(__name__)

@shared_task(name='tasks.check_inactive_entities')
def check_inactive_entities():
    """
    A Celery task that queries for entities with no events in the last 12 hours.
    This task is designed to be run periodically by Celery Beat.
    """
    # To run database queries, we need access to the application context.
    # Since this task runs in a separate process, we must create a new app instance.
    from app import create_app
    app = create_app()
    with app.app_context():
        log.info("Running periodic check for inactive entities...")

        twelve_hours_ago = datetime.utcnow() - timedelta(hours=12)

        # A subquery to find the last event time for each entity.
        # This is more efficient than processing in Python.
        last_event_subquery = db.session.query(
            Event.entity_id,
            db.func.max(Event.timestamp).label('last_event_ts')
        ).group_by(Event.entity_id).subquery()

        # We perform an OUTER JOIN from Entity to the subquery.
        # This ensures that we also find entities that have ZERO events.
        inactive_entities = db.session.query(
            Entity.id, Entity.name, Entity.entity_type
        ).outerjoin(
            last_event_subquery, Entity.id == last_event_subquery.c.entity_id
        ).filter(
            # An entity is inactive if its last event was > 12 hours ago,
            # OR if it has no last event time at all (NULL).
            (last_event_subquery.c.last_event_ts < twelve_hours_ago) |
            (last_event_subquery.c.last_event_ts == None)
        ).all()

        if not inactive_entities:
            log.info("SUCCESS: No inactive entities found.")
            return "Task completed. No inactive entities."

        log.warning(f"ALERT: Found {len(inactive_entities)} inactive entities.")
        for entity in inactive_entities:
            # In a real system, you would replace this log with an email,
            # a Slack message, or an entry in an alert dashboard.
            log.warning(
                f"  - Entity '{entity.name}' (ID: {entity.id}, Type: {entity.entity_type}) "
                "has not been observed in the last 12 hours."
            )

        return f"Task completed. {len(inactive_entities)} inactive entities logged."