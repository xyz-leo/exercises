"""
Task-related Pydantic schemas.

This module defines request and response schemas for task operations,
including creation, reading, updating task information with proper validation
for task ownership (user vs team assignment).
"""

# app/schemas/task_schema.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """
    Base schema for task data containing common fields.
    
    Defines the core task structure including ownership information.
    A task must have either an owner (personal task) or a team (team task).
    """
    title: str                       # Task title (required)
    description: Optional[str] = None  # Task description (optional)
    status: str = "pending"          # Task status with default value
    due_date: Optional[datetime] = None  # Optional due date for the task
    owner_id: int                    # REQUIRED: ID of the user who owns this task
    team_id: Optional[int] = None    # OPTIONAL: ID of the team this task belongs to


class TaskCreate(TaskBase):
    """
    Schema for creating new tasks.
    
    Used in POST /tasks/ endpoint. Inherits all fields from TaskBase.
    The service layer validates that owner_id exists and team_id (if provided) exists.
    """
    pass


class TaskUpdate(BaseModel):
    """
    Schema for updating existing tasks.
    
    Used in PUT /tasks/{task_id} endpoint. All fields are optional
    to support partial updates. Validates task ownership logic during updates.
    """
    title: Optional[str] = None           # New task title (optional)
    description: Optional[str] = None     # New description (optional)
    status: Optional[str] = None          # New status (optional)
    due_date: Optional[datetime] = None   # New due date (optional)
    owner_id: Optional[int] = None        # New owner (optional - must validate)
    team_id: Optional[int] = None         # New team (optional - must validate)

    model_config = {
        "from_attributes": True  # Allow creation from ORM objects
    }


class TaskRead(TaskBase):
    """
    Schema for task responses (reading task data).
    
    Used in GET endpoints to return task information to clients.
    Includes system-generated fields like ID and timestamps that aren't
    provided during task creation.
    """
    id: int                    # Task's unique identifier
    created_at: datetime       # When the task was created (auto-generated)
    updated_at: datetime       # When the task was last updated (auto-generated)

    model_config = {
        "from_attributes": True  # Allow creation from SQLAlchemy models
    }
