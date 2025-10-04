from flask_restx import Resource
from ..dto import EntityDto
from ...models import Entity

# Get the namespace from the DTO
api = EntityDto.api

@api.route('/')
class EntityList(Resource):
    """
    Resource for handling the collection of entities.
    """
    @api.doc('list_entities')
    @api.marshal_list_with(EntityDto.entity, envelope='entities')
    def get(self):
        """
        List all entities.

        Fetches all entities from the database and returns them in a list.
        """
        return Entity.query.all()