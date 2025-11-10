"""
Team-related Pydantic schemas.

This module defines request and response schemas for team operations,
including creation, reading, updating team information and relationships.
"""

# app/schemas/team_schema.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, List, TYPE_CHECKING

# Conditional imports for type hints to avoid circular dependencies
if TYPE_CHECKING:
    from .task_schema import TaskRead
    from .team_member_schema import TeamMemberRead


class TeamBase(BaseModel):
    """
    Base schema for team data containing common fields.
    
    Used as foundation for other team-related schemas.
    """
    name: str  # Team name (must be unique across all teams)


class TeamCreate(TeamBase):
    """
    Schema for creating new teams.
    
    Used in POST /teams/ endpoint. Currently inherits all fields from TeamBase.
    The creator is automatically added as a moderator in the service layer.
    """
    pass


class TeamUpdate(BaseModel):
    """
    Schema for updating existing teams.
    
    Used in PUT /teams/{team_id} endpoint. All fields are optional
    to support partial updates. Only the team name can be updated.
    """
    name: Optional[str] = None  # New team name (optional, must remain unique)

    model_config = {
        "from_attributes": True  # Allow creation from ORM objects
    }


class TeamResponse(TeamBase):
    """
    Schema for team responses (reading team data).
    
    Used in GET endpoints to return team information to clients.
    Includes the team ID for reference in other operations.
    """
    id: int  # Team's unique identifier

    model_config = {
        "from_attributes": True  # Allow creation from SQLAlchemy models
    }
