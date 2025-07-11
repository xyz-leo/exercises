# models.py

from database import db
from datetime import datetime

# Define Task model class for SQLAlchemy ORM
class Task(db.Model):
    # Primary key column - unique integer ID for each task
    id = db.Column(db.Integer, primary_key=True)

    # Task title column - string, required (nullable=False)
    title = db.Column(db.String, nullable=False)

    # Task description column - text, optional (nullable=True)
    description = db.Column(db.Text, nullable=True)

    # Creation timestamp column - stores date/time when record created
    # Default value set to current UTC time when object is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

