from flask_restx import Resource
from sqlalchemy.orm import joinedload
from ..dto import AlertDto
from ...models import Alert

# Get the namespace from the DTO
api = AlertDto.api

@api.route('/')
class AlertList(Resource):
    """
    Resource for handling the collection of alerts.
    """
    @api.doc('list_alerts')
    @api.marshal_list_with(AlertDto.alert, envelope='alerts')
    def get(self):
        """
        List all alerts, ordered by most recent.

        Fetches all alerts from the database, eager loading the related entity
        to avoid N+1 query problems.
        """
        return Alert.query.options(joinedload(Alert.entity)).order_by(Alert.timestamp.desc()).all()