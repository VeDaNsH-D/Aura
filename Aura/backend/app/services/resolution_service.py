from ..models import Entity

def get_all_entities():
    """
    Retrieves all entities from the database.

    This service function encapsulates the database query to fetch all records
    from the Entity table.
    """
    return Entity.query.all()