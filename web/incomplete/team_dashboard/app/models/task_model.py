"""
Task data model.

This module defines the Task model for managing individual work items.
Tasks can be assigned to individual users or entire teams.
"""

# app/models/task_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from app.core.database import Base
from app.models.user_model import User


class Task(Base):
    """
    Task model representing work items in the system.
    
    Tasks can be either personal (assigned to a user) or team-based
    (assigned to a team). A task cannot be assigned to both simultaneously.
    """
    
    __tablename__ = "tasks"

    # Primary key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    # Task content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    
    # Task state
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Optional due date for task completion
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    
    # Task must have an owner (individual user)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped[User] = relationship("User", back_populates="tasks")

    # Optional team assignment - if set, task belongs to the team
    # If team_id is None, task is considered a personal task
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey("teams.id"), nullable=True)
    team: Mapped[Optional["Team"]] = relationship("Team", back_populates="tasks")
