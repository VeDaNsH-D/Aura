from ..models import Event

def get_timeline_for_entity(entity_id: int):
    """
    Retrieves the event timeline for a specific entity from the database.

    This service function encapsulates the database query to fetch all event
    records associated with a given entity_id, sorted by timestamp.
    """
    return Event.query.filter_by(entity_id=entity_id).order_by(Event.timestamp.desc()).all()