"""
Team data model.

This module defines the Team model for organizing users into collaborative groups.
Teams can have multiple members and can be assigned tasks.
"""

# app/models/team_model.py
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from app.core.database import Base


class Team(Base):
    """
    Team model representing collaborative groups of users.
    
    Teams organize users for task management and collaboration.
    Each team has a unique name and maintains relationships with members and tasks.
    """
    
    __tablename__ = "teams"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Team identifier - must be unique across all teams
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relationships
    
    # Many-to-Many relationship with User via TeamMember join table
    # This represents all members of the team with their roles
    members: Mapped[List["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="team",
        cascade="all, delete-orphan"  # Remove team members when team is deleted
    )

    # One-to-Many relationship with Task (tasks assigned to this team)
    # Tasks can be assigned to either a user or a team, but not both
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="team",
        cascade="all, delete-orphan"  # Unassign tasks when team is deleted
    )
