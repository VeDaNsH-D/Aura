import logging
from datetime import datetime, timedelta
from celery import shared_task
from ..models import db, Event, Entity, Alert

log = logging.getLogger(__name__)

@shared_task(name='tasks.check_inactive_entities')
def check_inactive_entities():
    """
    Queries for inactive entities and creates an Alert record for each one found.
    """
    from app import create_app
    app = create_app()
    with app.app_context():
        log.info("Running periodic check for inactive entities...")

        twelve_hours_ago = datetime.utcnow() - timedelta(hours=12)

        last_event_subquery = db.session.query(
            Event.entity_id,
            db.func.max(Event.timestamp).label('last_event_ts')
        ).group_by(Event.entity_id).subquery()

        inactive_entities = db.session.query(
            Entity
        ).outerjoin(
            last_event_subquery, Entity.id == last_event_subquery.c.entity_id
        ).filter(
            (last_event_subquery.c.last_event_ts < twelve_hours_ago) |
            (last_event_subquery.c.last_event_ts == None)
        ).all()

        if not inactive_entities:
            log.info("SUCCESS: No inactive entities found.")
            return "Task completed. No inactive entities."

        log.warning(f"ALERT: Found {len(inactive_entities)} inactive entities. Creating alerts...")
        
        for entity in inactive_entities:
            # Check if an unacknowledged alert for this entity already exists to avoid duplicates
            existing_alert = Alert.query.filter_by(entity_id=entity.id, is_acknowledged=False).first()
            
            if not existing_alert:
                message = f"Entity '{entity.name}' has not been observed in the last 12 hours."
                alert = Alert(
                    entity_id=entity.id,
                    severity='medium',
                    message=message,
                    is_acknowledged=False
                )
                db.session.add(alert)
                log.info(f"Created alert for entity: {entity.name} (ID: {entity.id})")

        db.session.commit()

        return f"Task completed. {len(inactive_entities)} inactive entities processed."

