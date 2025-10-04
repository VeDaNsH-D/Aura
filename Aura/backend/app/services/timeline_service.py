from ..models import Event

def get_timeline_for_entity(entity_id: int):
    """
    Retrieves all event records for a specific entity from the database.

    This function queries the database for all events associated with the given
    entity_id and returns them sorted chronologically, with the most recent
    event appearing first.

    Args:
        entity_id: The integer ID of the entity whose timeline is being requested.

    Returns:
        A list of Event model objects, ordered by timestamp in descending order.
        Returns an empty list if no events are found for the entity.
    """
    # Use the SQLAlchemy model to query the Event table.
    # - filter_by(entity_id=entity_id): Finds all records matching the entity's ID.
    # - order_by(Event.timestamp.desc()): Sorts the results by the timestamp field
    #   in descending order (newest first).
    # - all(): Executes the query and returns all results as a list.
    timeline = Event.query.filter_by(entity_id=entity_id).order_by(Event.timestamp.desc()).all()

    return timeline