from flask_restx import Resource

from ..dto import EventDto
from ...services.timeline_service import get_timeline_for_entity

# Get the namespace from the DTO for consistency
ns = EventDto.ns

@ns.route("/<int:entity_id>")
@ns.param('entity_id', 'The unique identifier for the entity')
class Timeline(Resource):
    """
    Handles operations related to the activity timeline of a specific entity.
    """
    @ns.doc('get_entity_timeline', description='Get the chronological event timeline for a specific entity.')
    @ns.marshal_list_with(EventDto.event, envelope='events')
    def get(self, entity_id: int):
        """
        Returns the event timeline for a single entity.

        This endpoint calls the timeline service to fetch all event records
        associated with the provided entity_id, sorts them by timestamp,
        and serializes the response using the EventDto.
        """
        # Call the service layer function to get the data
        timeline = get_timeline_for_entity(entity_id)
        return timeline, 200