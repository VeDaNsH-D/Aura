from ..models import Entity

def get_all_entities():
    """
    Retrieves all entity records from the database.

    This function queries the database for all entities (e.g., students, staff, assets)
    and returns them.

    Returns:
        A list of Entity model objects. Returns an empty list if the table is empty.
    """
    # Use the SQLAlchemy Entity model to query the database for all records.
    # The .all() method executes the query and returns the results as a list.
    entities = Entity.query.all()

    return entities