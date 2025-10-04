from flask_restx import Resource

from ..dto import EntityDto
from ...services.resolution_service import get_all_entities

# Get the namespace from the DTO for consistency
ns = EntityDto.ns

@ns.route("")
class EntityList(Resource):
    """
    Handles operations related to the list of all entities.
    """
    @ns.doc('list_entities', description='Get a list of all campus entities (students, staff, and assets).')
    @ns.marshal_list_with(EntityDto.entity, envelope='entities')
    def get(self):
        """
        Returns the complete list of all entities.

        This endpoint calls the resolution service to fetch all records from the
        Entity table in the database and serializes the response using the EntityDto.
        """
        # Call the service layer function to get the data
        entities = get_all_entities()
        return entities, 200