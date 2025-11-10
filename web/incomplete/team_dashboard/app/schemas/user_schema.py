"""
User-related Pydantic schemas.

This module defines request and response schemas for user operations,
including creation, reading, updating, and deletion of user accounts.
"""

# app/schemas/user_schema.py
from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, TYPE_CHECKING

# Import only for type checking to avoid circular imports
if TYPE_CHECKING:
    from .task_schema import TaskRead
    from .team_member_schema import TeamMemberRead


class UserBase(BaseModel):
    """
    Base schema for user data containing common fields.
    
    Used as base for other user schemas to avoid field duplication.
    """
    username: str      # Unique username identifier
    email: EmailStr    # Unique email address (validated format)


class UserCreate(UserBase):
    """
    Schema for creating new users.
    
    Used in POST /users/ endpoint. Includes password field for initial setup.
    Inherits username and email from UserBase and adds password requirement.
    """
    password: str  # Plain text password (will be hashed before storage)


class UserUpdate(BaseModel):
    """
    Schema for updating existing users.
    
    Used in PUT /users/{user_id} endpoint. All fields are optional
    to support partial updates. Only provided fields will be updated.
    """
    username: Optional[str] = None      # New username (optional)
    email: Optional[EmailStr] = None    # New email (optional, validated)
    password: Optional[str] = None      # New password (optional, will be hashed)

    model_config = {
        "from_attributes": True  # Allow creation from ORM objects
    }


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=1, description="Current password")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")


class UserResponse(UserBase):
    """
    Schema for user responses (reading user data).
    
    Used in GET endpoints to return user information to clients.
    Includes the user ID but excludes sensitive information like password hashes.
    """
    id: int  # User's unique identifier

    model_config = {
        "from_attributes": True  # Allow creation from SQLAlchemy models
    }
