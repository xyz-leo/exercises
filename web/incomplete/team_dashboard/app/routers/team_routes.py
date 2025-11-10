"""
Team management routes for CRUD operations and team membership.

This module defines API endpoints for team management, including
creation, retrieval, updating, deletion of teams, and team member operations.
"""

# api/routers/team_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.team_schema import TeamCreate, TeamUpdate, TeamResponse
from app.schemas.team_member_schema import TeamMemberRead
from app.services import team_service as TeamService
from app.core.database import get_db


# Temporary: Get the first available user ID
# This is a temporary solution until full authentication is implemented
def get_current_user_id(db: Session = Depends(get_db)):
    """
    Temporary function to get a valid user ID until authentication is implemented.
    
    Returns the ID of the first user in the database. In a production system,
    this would be replaced with proper JWT token authentication.
    
    Args:
        db: Database session
        
    Returns:
        int: User ID of the first user in the database
        
    Raises:
        HTTPException: 400 if no users exist in the database

    Example:

    """
    from app.models.user_model import User
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users found. Please create a user first."
        )
    return user.id


# Router instance for team-related endpoints
router = APIRouter(prefix="/teams", tags=["Teams"])


@router.post("/", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_data: TeamCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Create a new team.
    
    Creates a new team with the provided name. The creator is automatically
    added as a moderator of the team. Validates team name uniqueness.
    
    Args:
        team_data: Team creation data (name)
        db: Database session dependency
        current_user_id: ID of the user creating the team (from dependency)
        
    Returns:
        TeamResponse: Created team information
        
    Raises:
        HTTPException: 400 if team name already exists
        
    Example:
    curl -X POST "http://127.0.0.1:8000/teams/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Development Team"}'
    """
    return TeamService.create_team(db, team_data, creator_id=current_user_id)


@router.get("/", response_model=list[TeamResponse])
def get_all_teams(db: Session = Depends(get_db)):
    """
    Retrieve all teams.
    
    Returns a list of all teams in the system.
    
    Args:
        db: Database session dependency
        
    Returns:
        list[TeamResponse]: List of all teams
        
    Example:
    curl -X GET http://127.0.0.1:8000/teams
    """
    return TeamService.get_all_teams(db)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team_by_id(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific team by ID.
    
    Args:
        team_id: ID of the team to retrieve
        db: Database session dependency
        
    Returns:
        TeamResponse: Team information
        
    Raises:
        HTTPException: 404 if team not found
        
    Example:
    curl -X GET http://127.0.0.1:8000/teams/1
    """
    return TeamService.get_team_by_id(db, team_id)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(team_id: int, team_data: TeamUpdate, db: Session = Depends(get_db)):
    """
    Update a team's details.
    
    Supports partial updates. Currently only supports updating the team name.
    Validates that the new team name is unique.
    
    Args:
        team_id: ID of the team to update
        team_data: Update data (partial updates supported)
        db: Database session dependency
        
    Returns:
        TeamResponse: Updated team information
        
    Raises:
        HTTPException: 404 if team not found
        HTTPException: 400 if new team name already taken
        
    Example:
    curl -X PUT "http://127.0.0.1:8000/teams/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Advanced Development Team"}'
    """
    return TeamService.update_team(db, team_id, team_data)


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    """
    Delete a team by ID.
    
    Permanently removes the team and all associated team members.
    Team tasks are unassigned (team_id set to null) but not deleted.
    
    Args:
        team_id: ID of the team to delete
        db: Database session dependency
        
    Returns:
        None: 204 No Content on success
        
    Raises:
        HTTPException: 404 if team not found
        
    Example:
    curl -X DELETE "http://127.0.0.1:8000/teams/1"
    """
    TeamService.delete_team(db, team_id)
    return None


@router.get("/{team_id}/members", response_model=list[TeamMemberRead])
def get_team_members(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all members of a specific team.
    
    Returns a list of all users who are members of the specified team,
    including their moderator status and join date.
    
    Args:
        team_id: ID of the team
        db: Database session dependency
        
    Returns:
        list[TeamMemberRead]: List of team members
        
    Raises:
        HTTPException: 404 if team not found
        
    Example:
    curl -X GET "http://127.0.0.1:8000/teams/1/members"
    """
    return TeamService.get_team_members(db, team_id)


@router.get("/user/{user_id}", response_model=list[TeamResponse])
def get_user_teams(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all teams that a user is member of.
    
    Args:
        user_id: ID of the user
        db: Database session dependency
        
    Returns:
        list[TeamResponse]: List of teams the user belongs to
        
    Example:
    curl -X GET "http://127.0.0.1:8000/teams/user/1" \
     -H "Content-Type: application/json"
    """
    return TeamService.get_user_teams(db, user_id)
