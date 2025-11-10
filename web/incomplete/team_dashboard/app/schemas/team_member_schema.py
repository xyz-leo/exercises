"""
Team Member-related Pydantic schemas.

This module defines request and response schemas for team membership operations,
including adding members to teams, updating roles, and reading membership information.
"""

# app/schemas/team_member_schema.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TeamMemberBase(BaseModel):
    """
    Base schema for team member data containing common fields.
    
    Defines the core team membership structure including user-team relationship
    and role information.
    """
    user_id: int                # ID of the user being added to the team
    team_id: int                # ID of the team the user is joining
    is_moderator: bool = False  # Role flag - moderators have additional permissions


class TeamMemberCreate(TeamMemberBase):
    """
    Schema for creating new team memberships.
    
    Used in POST /team-members/teams/{team_id}/members endpoint.
    Inherits all fields from TeamMemberBase. The service layer validates
    that both user and team exist and that the requester has moderator permissions.
    """
    pass


class TeamMemberUpdate(BaseModel):
    """
    Schema for updating existing team memberships.
    
    Used in PUT /team-members/teams/{team_id}/members/{user_id}/role endpoint.
    Currently only supports updating the moderator status. The service layer
    validates that the requester has moderator permissions.
    """
    is_moderator: Optional[bool] = None  # New moderator status (optional)


class TeamMemberRead(TeamMemberBase):
    """
    Schema for team member responses (reading membership data).
    
    Used in GET endpoints to return team membership information to clients.
    Includes system-generated fields like ID and join timestamp.
    """
    id: int                    # Membership record unique identifier
    joined_at: datetime        # When the user joined the team (auto-generated)

    model_config = {
        "from_attributes": True  # Allow creation from SQLAlchemy models
    }
