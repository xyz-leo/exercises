# app/services/team_service.py
"""
Team service layer for business logic operations.

This module contains the business logic for team management operations,
including creation, retrieval, updating, and deletion of teams.
Handles team membership and task relationships.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.team_model import Team
from app.models.team_member_model import TeamMember
from app.schemas.team_schema import TeamCreate, TeamUpdate
from app.models.task_model import Task


def create_team(db: Session, team_data: TeamCreate, creator_id: int) -> Team:
    """
    Create a new team and assign the creator as a moderator.
    
    Validates team name uniqueness and automatically creates a team membership
    record for the creator with moderator privileges.
    
    Args:
        db: Database session
        team_data: Team creation data (name)
        creator_id: ID of the user creating the team
        
    Returns:
        Team: Newly created team object
        
    Raises:
        HTTPException: 400 if team name exists or creator not found
        HTTPException: 500 if database operation fails
    """
    try:
        from app.models.user_model import User
        # Verify creator exists
        creator = db.query(User).filter(User.id == creator_id).first()
        if not creator:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Creator user not found"
            )

        # Check if team name already exists
        existing_team = db.query(Team).filter(Team.name == team_data.name).first()
        if existing_team:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team name already exists"
            )
        
        # Create new team
        new_team = Team(name=team_data.name)
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        
        # Assign creator as moderator
        membership = TeamMember(
            user_id=creator_id,
            team_id=new_team.id,
            is_moderator=True
        )
        db.add(membership)
        db.commit()
        db.refresh(membership)
        db.refresh(new_team)  # Refresh to get relationships
        
        return new_team
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating team: {str(e)}"
        )


def get_all_teams(db: Session) -> list[Team]:
    """
    Retrieve all teams from database.
    
    Args:
        db: Database session
        
    Returns:
        list[Team]: List of all teams
        
    Raises:
        HTTPException: 500 if database query fails
    """
    try:
        return db.query(Team).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving teams: {str(e)}"
        )


def get_team_by_id(db: Session, team_id: int) -> Team:
    """
    Retrieve a team by ID.
    
    Args:
        db: Database session
        team_id: ID of the team to retrieve
        
    Returns:
        Team: Requested team object
        
    Raises:
        HTTPException: 404 if team not found
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found"
        )
    return team


def update_team(db: Session, team_id: int, team_data: TeamUpdate) -> Team:
    """
    Update team information.
    
    Supports partial updates and validates team name uniqueness.
    
    Args:
        db: Database session
        team_id: ID of the team to update
        team_data: Data to update (partial updates supported)
        
    Returns:
        Team: Updated team object
        
    Raises:
        HTTPException: 404 if team not found
        HTTPException: 400 if new team name already taken
        HTTPException: 500 if database operation fails
    """
    try:
        # Find team
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Update fields if provided
        update_data = team_data.model_dump(exclude_unset=True)
        
        if "name" in update_data and update_data["name"]:
            # Check if new name is taken by another team
            existing_team = db.query(Team).filter(
                Team.name == update_data["name"],
                Team.id != team_id
            ).first()
            if existing_team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Team name already taken"
                )
            team.name = update_data["name"]
        
        # Commit changes
        db.commit()
        db.refresh(team)
        
        return team
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating team: {str(e)}"
        )


def delete_team(db: Session, team_id: int) -> bool:
    """
    Delete a team by ID.
    
    Handles cleanup of related team members and tasks to maintain
    database integrity through cascading operations.
    
    Args:
        db: Database session
        team_id: ID of the team to delete
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: 404 if team not found
        HTTPException: 500 if database operation fails
    """
    try:
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Delete associated team members first (due to foreign key constraints)
        db.query(TeamMember).filter(TeamMember.team_id == team_id).delete()
        
        # Delete team tasks (if they exist)
        from app.models.task_model import Task
        db.query(Task).filter(Task.team_id == team_id).update({"team_id": None})
        
        # Delete the team
        db.delete(team)
        db.commit()
        
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting team: {str(e)}"
        )


def get_team_members(db: Session, team_id: int) -> list[TeamMember]:
    """
    Retrieve all members of a specific team.
    
    Args:
        db: Database session
        team_id: ID of the team
        
    Returns:
        list[TeamMember]: List of team members
        
    Raises:
        HTTPException: 404 if team not found
        HTTPException: 500 if database query fails
    """
    try:
        # Verify team exists
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Return all team members
        members = db.query(TeamMember).filter(TeamMember.team_id == team_id).all()
        return members
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving team members: {str(e)}"
        )


def get_user_teams(db: Session, user_id: int) -> list[Team]:
    """
    Retrieve all teams that a user is member of.
    
    Args:
        db: Database session
        user_id: ID of the user
        
    Returns:
        list[Team]: List of teams the user belongs to
        
    Raises:
        HTTPException: 500 if database query fails
    """
    try:
        return db.query(Team).join(TeamMember).filter(TeamMember.user_id == user_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user teams: {str(e)}"
        )
