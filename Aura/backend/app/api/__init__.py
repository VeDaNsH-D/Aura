from flask import Blueprint
from flask_restx import Api

# Import DTOs to access their namespaces
from .dto import EntityDto, EventDto, AlertDto

# Create a Blueprint for the API
api_bp = Blueprint('api', __name__)

# Initialize the Flask-RESTx Api with the blueprint
# This provides the framework for creating the RESTful API endpoints.
api = Api(
    api_bp,
    title='Aura Campus Intelligence API',
    version='1.0',
    description='A comprehensive API for tracking and managing campus entities, events, and alerts.',
    doc='/doc' # URL for the Swagger UI documentation
)

# Add namespaces from DTOs to the API
# Each namespace corresponds to a set of related resources.
api.add_namespace(EntityDto.api)
api.add_namespace(EventDto.api)
api.add_namespace(AlertDto.api)

# Import the resource files to ensure their routes are registered with the namespaces.
# This is a common pattern in Flask to ensure views/resources are connected.
from .resources import entity, timeline, alert