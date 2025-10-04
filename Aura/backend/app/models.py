from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

# Initialize the SQLAlchemy extension
db = SQLAlchemy()

class Entity(db.Model):
    """
    Represents a person (student, staff) or an asset (e.g., laptop, projector).
    This is the central table for all resolved entities on campus.
    """
    __tablename__ = 'entities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False) # e.g., 'student', 'staff', 'asset'
    primary_email = db.Column(db.String(128), unique=True, nullable=True)

    # --- Relationships ---
    # One-to-Many: One Entity can have multiple Identifiers
    identifiers = relationship('Identifier', back_populates='entity', cascade='all, delete-orphan')
    # One-to-Many: One Entity can have many Events
    events = relationship('Event', back_populates='entity', cascade='all, delete-orphan')
    # One-to-Many: One Entity can have multiple Alerts
    alerts = relationship('Alert', back_populates='entity', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Entity {self.name} ({self.entity_type})>'

class Identifier(db.Model):
    """
    Stores various identifiers for an entity.
    This table links different source IDs (card_id, email, device_hash) to a single canonical Entity.
    """
    __tablename__ = 'identifiers'

    id = db.Column(db.Integer, primary_key=True)
    identifier_type = db.Column(db.String(50), nullable=False) # e.g., 'card_id', 'device_hash', 'face_id'
    value = db.Column(db.String(255), nullable=False, index=True)

    # --- Foreign Keys ---
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)

    # --- Relationships ---
    # Many-to-One: Many Identifiers belong to one Entity
    entity = relationship('Entity', back_populates='identifiers')

    def __repr__(self):
        return f'<Identifier {self.identifier_type}: {self.value}>'

class Event(db.Model):
    """
    Represents a single recorded activity for an entity from any data source.
    This table forms the basis for generating activity timelines.
    """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    location = db.Column(db.String(255), nullable=True)
    source_type = db.Column(db.String(50), nullable=False) # e.g., 'swipe', 'wifi', 'library', 'cctv'
    description = db.Column(db.Text, nullable=True)

    # --- Foreign Keys ---
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)

    # --- Relationships ---
    # Many-to-One: Many Events belong to one Entity
    entity = relationship('Entity', back_populates='events')

    def __repr__(self):
        return f'<Event {self.source_type} at {self.timestamp} for Entity ID {self.entity_id}>'

class Alert(db.Model):
    """
    Represents a triggered alert for an entity, typically due to anomalous activity.
    """
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    severity = db.Column(db.String(50), nullable=False) # e.g., 'low', 'medium', 'high', 'critical'
    message = db.Column(db.Text, nullable=False)
    is_acknowledged = db.Column(db.Boolean, default=False, nullable=False)

    # --- Foreign Keys ---
    entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)

    # --- Relationships ---
    # Many-to-One: Many Alerts belong to one Entity
    entity = relationship('Entity', back_populates='alerts')

    def __repr__(self):
        return f'<Alert {self.severity} at {self.timestamp} for Entity ID {self.entity_id}>'
