"""
Team Member join model.

This module defines the TeamMember model which serves as a join table
between Users and Teams, storing additional information about the membership
such as moderator status and join date.
"""

# app/models/team_member_model.py
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class TeamMember(Base):
    """
    Team Member model representing the many-to-many relationship between Users and Teams.
    
    This join table stores additional information about team membership
    beyond the basic relationship, including role permissions and timestamps.
    """
    
    __tablename__ = "team_members"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys to User and Team
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Role information - moderators have additional permissions
    is_moderator = Column(Boolean, default=False)
    
    # Timestamp for when the user joined the team
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    
    # Many-to-One relationship with Team
    # Each team member record belongs to one team
    team = relationship("Team", back_populates="members")
    
    # Many-to-One relationship with User  
    # Each team member record belongs to one user
    user = relationship("User", back_populates="teams")
