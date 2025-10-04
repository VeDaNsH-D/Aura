from flask_restx import Resource
from ..dto import EventDto
from ...models import Event

# Get the namespace from the DTO
api = EventDto.api

@api.route('/<int:entity_id>')
@api.param('entity_id', 'The ID of the entity')
class Timeline(Resource):
    """
    Resource for retrieving the timeline of a specific entity.
    """
    @api.doc('get_entity_timeline')
    @api.marshal_list_with(EventDto.event, envelope='events')
    def get(self, entity_id):
        """
        Get the event timeline for a specific entity.

        Fetches all events for a given entity, sorted from most recent to oldest.
        """
        # Query the database for all events matching the entity_id,
        # ordered by the timestamp in descending order (most recent first).
        return Event.query.filter_by(entity_id=entity_id).order_by(Event.timestamp.desc()).all()