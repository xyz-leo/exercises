"""
Team member management routes for membership operations.

This module defines API endpoints for managing team memberships, including
adding members to teams, updating roles, and retrieving membership information.
All operations include proper permission validation.
"""

# app/routers/team_member_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.team_member_schema import TeamMemberCreate, TeamMemberRead, TeamMemberUpdate
from app.services import team_member_service as TeamMemberService
from app.core.database import get_db


# Temporary: Get current user ID (same as teams)
# This is a temporary solution until full authentication is implemented
def get_current_user_id(db: Session = Depends(get_db)):
    """
    Temporary function to get a valid user ID until authentication is implemented.
    
    Returns the ID of the first user in the database. In a production system,
    this would be replaced with proper JWT token authentication that extracts
    the user ID from the JWT token payload.
    
    Args:
        db: Database session
        
    Returns:
        int: User ID of the first user in the database
        
    Raises:
        HTTPException: 400 if no users exist in the database
    """
    from app.models.user_model import User
    user = db.query(User).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No users found. Please create a user first."
        )
    return user.id


# Router instance for team member-related endpoints
router = APIRouter(prefix="/team-members", tags=["Team Members"])


@router.post("/teams/{team_id}/members", response_model=TeamMemberRead, status_code=status.HTTP_201_CREATED)
def add_member_to_team(
    team_id: int,
    member_data: TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Add a user to a team. Only team moderators can add members.
    
    Adds a user to the specified team with the provided role (moderator or regular member).
    The requesting user must be a moderator of the team to perform this action.
    
    Args:
        team_id: ID of the team to add the member to
        member_data: Membership data including user_id and is_moderator flag
        db: Database session dependency
        current_user_id: ID of the user making the request (from dependency)
        
    Returns:
        TeamMemberRead: Created team membership information
        
    Raises:
        HTTPException: 403 if current user is not a moderator
        HTTPException: 404 if team or user not found
        HTTPException: 400 if user already in team
        
    Example:
    curl -X POST "http://127.0.0.1:8000/team-members/teams/1/members" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 2,
       "team_id": 1,
       "is_moderator": false
     }'
    """
    return TeamMemberService.add_member(db, team_id, current_user_id, member_data)


@router.get("/", response_model=list[TeamMemberRead])
def get_all_team_members(db: Session = Depends(get_db)):
    """
    Retrieve all team members from all teams.
    
    Returns a comprehensive list of all team memberships across all teams.
    This endpoint provides a system-wide view of team memberships.
    
    Args:
        db: Database session dependency
        
    Returns:
        list[TeamMemberRead]: List of all team members
        
    Example:
    curl -X GET "http://127.0.0.1:8000/team-members/" \
     -H "Content-Type: application/json"
    """
    return TeamMemberService.get_all_members(db)


@router.get("/{member_id}", response_model=TeamMemberRead)
def get_team_member_by_id(member_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single team member by ID.
    
    Args:
        member_id: ID of the team member record (membership ID)
        db: Database session dependency
        
    Returns:
        TeamMemberRead: Team membership information
        
    Raises:
        HTTPException: 404 if team member not found
        
    Example:
    curl -X GET "http://127.0.0.1:8000/team-members/1" \
     -H "Content-Type: application/json"
    """
    return TeamMemberService.get_member_by_id(db, member_id)


@router.get("/teams/{team_id}/members", response_model=list[TeamMemberRead])
def get_members_of_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retrieve all members of a specific team. Only team members can access this.
    
    Returns a list of all users who are members of the specified team.
    The requesting user must be a member of the team to access this information.
    
    Args:
        team_id: ID of the team
        db: Database session dependency
        current_user_id: ID of the user making the request (from dependency)
        
    Returns:
        list[TeamMemberRead]: List of team members
        
    Raises:
        HTTPException: 403 if user is not a member of the team
        
    Example:
    curl -X GET "http://127.0.0.1:8000/team-members/teams/1/members" \
     -H "Content-Type: application/json"
    """
    return TeamMemberService.get_team_members(db, team_id, current_user_id)


@router.put("/teams/{team_id}/members/{user_id}/role", response_model=TeamMemberRead)
def update_member_role(
    team_id: int,
    user_id: int,
    update_data: TeamMemberUpdate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Update a member's role (moderator status). Only moderators can change roles.
    
    Allows team moderators to promote or demote other members' moderator status.
    The requesting user must be a moderator of the team to perform this action.
    
    Args:
        team_id: ID of the team
        user_id: ID of the user whose role is being updated
        update_data: Update data containing is_moderator flag
        db: Database session dependency
        current_user_id: ID of the user making the request (from dependency)
        
    Returns:
        TeamMemberRead: Updated team membership information
        
    Raises:
        HTTPException: 403 if current user is not a moderator
        HTTPException: 404 if member not found
        
    Example:
    curl -X PUT "http://127.0.0.1:8000/team-members/teams/1/members/2/role" \
     -H "Content-Type: application/json" \
     -d '{
       "is_moderator": true
     }'
    """
    return TeamMemberService.update_member_role(db, team_id, current_user_id, user_id, update_data)


@router.delete("/teams/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_member_from_team(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Remove a user from a team. Only moderators can remove members.
    
    Removes the specified user from the team. The requesting user must be
    a moderator of the team to perform this action.
    
    Args:
        team_id: ID of the team
        user_id: ID of the user to remove from the team
        db: Database session dependency
        current_user_id: ID of the user making the request (from dependency)
        
    Returns:
        None: 204 No Content on success
        
    Raises:
        HTTPException: 403 if current user is not a moderator
        HTTPException: 404 if member not found in team
        
    Example:
    curl -X DELETE "http://127.0.0.1:8000/team-members/teams/3/members/1"
    """
    TeamMemberService.remove_member(db, team_id, current_user_id, user_id)
    return None
