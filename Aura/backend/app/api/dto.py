from flask_restx import Namespace, fields

class EntityDto:
    """
    Data Transfer Objects for the Entity models.
    """
    # Create a namespace for entities, which helps in organizing the API documentation
    api = Namespace('entity', description='Entity related operations')

    # Define the model for an entity, which will be used for serialization
    entity = api.model('Entity', {
        'id': fields.Integer(readonly=True, description='The unique identifier of an entity'),
        'name': fields.String(required=True, description='The name of the entity'),
        'entity_type': fields.String(required=True, description='The type of the entity (e.g., student, staff)'),
        'primary_email': fields.String(description='The primary email address of the entity'),
    })

class EventDto:
    """
    Data Transfer Objects for the Event models.
    """
    # Create a namespace for timelines/events
    api = Namespace('timeline', description='Timeline and event related operations')

    # Define the model for a single event
    event = api.model('Event', {
        'timestamp': fields.DateTime(required=True, description='The time the event occurred', dt_format='iso8601'),
        'location': fields.String(required=True, description='The location where the event took place'),
        'source_type': fields.String(required=True, description='The source system of the event (e.g., swipe, wifi)'),
        'description': fields.String(required=True, description='A human-readable description of the event'),
    })

class AlertDto:
    """
    Data Transfer Objects for the Alert model.
    """
    # Create a namespace for alerts
    api = Namespace('alert', description='Alert related operations')

    # Define the model for a single alert
    alert = api.model('Alert', {
        'id': fields.Integer(readonly=True, description='The unique identifier of an alert'),
        'timestamp': fields.DateTime(required=True, description='The time the alert was triggered', dt_format='iso8601'),
        'severity': fields.String(required=True, description='The severity of the alert (e.g., low, medium, high)'),
        'message': fields.String(required=True, description='A human-readable message describing the alert'),
        'is_acknowledged': fields.Boolean(required=True, description='Flag indicating if the alert has been reviewed'),
        'entity_name': fields.String(attribute='entity.name', description='Name of the associated entity'),
    })