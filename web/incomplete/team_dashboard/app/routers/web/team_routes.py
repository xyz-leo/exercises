from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.services.team_service import (
    create_team, get_all_teams, get_team_by_id, 
    update_team, delete_team, get_user_teams,
    get_team_members
)
from app.services.team_member_service import remove_member
from app.schemas.team_schema import TeamCreate, TeamUpdate
from app.models.user_model import User
from app.models.team_model import Team
from app.models.team_member_model import TeamMember
from app.models.task_model import Task  # Add this import

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/team", response_class=HTMLResponse)
async def teams_page(
    request: Request,
    filter_type: str = Query("all", alias="filter"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Display teams page with filtering options.
    Filter types: all, my_teams
    """
    try:
        teams = []
        
        if filter_type == "my_teams":
            teams = get_user_teams(db, current_user.id)
        else:  # "all" or default
            teams = get_all_teams(db)
        
        # Check if user is moderator for each team
        for team in teams:
            team.is_moderator = any(
                tm.user_id == current_user.id and tm.is_moderator 
                for tm in team.members
            )
        
        return templates.TemplateResponse(
            "teams/teams.html",
            {
                "request": request,
                "teams": teams,
                "current_user": current_user,
                "filter_type": filter_type
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "teams/teams.html",
            {
                "request": request,
                "error": f"Error loading teams: {str(e)}",
                "teams": [],
                "current_user": current_user,
                "filter_type": filter_type
            }
        )


@router.get("/team/create", response_class=HTMLResponse)
async def create_team_page(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Display team creation form"""
    return templates.TemplateResponse(
        "teams/create-team.html",
        {
            "request": request,
            "current_user": current_user
        }
    )


@router.post("/team/create")
async def create_team_submit(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle team creation form submission"""
    try:
        # Create team data
        team_data = TeamCreate(name=name)
        
        # Create the team (creator becomes moderator automatically)
        new_team = create_team(db, team_data, current_user.id)
        
        # Redirect to teams page
        response = RedirectResponse(url="/team", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "teams/create-team.html",
            {
                "request": request,
                "error": e.detail,
                "current_user": current_user,
                "form_data": dict(await request.form())
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "teams/create-team.html",
            {
                "request": request,
                "error": f"Error creating team: {str(e)}",
                "current_user": current_user,
                "form_data": dict(await request.form())
            }
        )


@router.get("/team/{team_id}", response_class=HTMLResponse)
async def team_detail_page(
    request: Request,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display team details"""
    try:
        team = get_team_by_id(db, team_id)
        
        # Get team members
        members = get_team_members(db, team_id)
        
        # Check if user is member of this team
        is_member = any(tm.user_id == current_user.id for tm in team.members)
        is_moderator = any(
            tm.user_id == current_user.id and tm.is_moderator 
            for tm in team.members
        )
        
        if not is_member:
            raise HTTPException(
                status_code=403,
                detail="You are not a member of this team"
            )
        
        # Get team tasks
        team_tasks = db.query(Task).filter(Task.team_id == team_id).all()
        
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "team": team,
                "members": members,
                "tasks": team_tasks,
                "current_user": current_user,
                "is_moderator": is_moderator
            }
        )
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "error": f"Error loading team: {str(e)}"
            }
        )


@router.get("/team/{team_id}/edit", response_class=HTMLResponse)
async def edit_team_page(
    request: Request,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display team edit form"""
    try:
        team = get_team_by_id(db, team_id)
        
        # Check if user is moderator of this team
        is_moderator = any(
            tm.user_id == current_user.id and tm.is_moderator 
            for tm in team.members
        )
        
        if not is_moderator:
            raise HTTPException(
                status_code=403,
                detail="Only team moderators can edit the team"
            )
        
        return templates.TemplateResponse(
            "teams/edit-team.html",
            {
                "request": request,
                "team": team,
                "current_user": current_user
            }
        )
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "teams/edit-team.html",
            {
                "request": request,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "teams/edit-team.html",
            {
                "request": request,
                "error": f"Error loading team: {str(e)}"
            }
        )


@router.post("/team/{team_id}/edit")
async def edit_team_submit(
    request: Request,
    team_id: int,
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle team edit form submission"""
    try:
        team = get_team_by_id(db, team_id)
        
        # Check if user is moderator of this team
        is_moderator = any(
            tm.user_id == current_user.id and tm.is_moderator 
            for tm in team.members
        )
        
        if not is_moderator:
            raise HTTPException(
                status_code=403,
                detail="Only team moderators can edit the team"
            )
        
        # Create update data
        update_data = TeamUpdate(name=name)
        
        # Update the team
        updated_team = update_team(db, team_id, update_data)
        
        # Redirect to team detail
        response = RedirectResponse(url=f"/team/{team_id}", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "teams/edit-team.html",
            {
                "request": request,
                "error": e.detail,
                "team": team,
                "current_user": current_user
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "teams/edit-team.html",
            {
                "request": request,
                "error": f"Error updating team: {str(e)}",
                "team": team,
                "current_user": current_user
            }
        )


@router.post("/team/{team_id}/delete")
async def delete_team_submit(
    request: Request,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle team deletion"""
    try:
        team = get_team_by_id(db, team_id)
        
        # Check if user is moderator of this team
        is_moderator = any(
            tm.user_id == current_user.id and tm.is_moderator 
            for tm in team.members
        )
        
        if not is_moderator:
            raise HTTPException(
                status_code=403,
                detail="Only team moderators can delete the team"
            )
        
        # Delete the team
        delete_team(db, team_id)
        
        # Redirect to teams page
        response = RedirectResponse(url="/team", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "error": e.detail,
                "team": team
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "error": f"Error deleting team: {str(e)}",
                "team": team
            }
        )


@router.post("/team/{team_id}/leave")
async def leave_team_submit(
    request: Request,
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle team leave request"""
    try:
        team = get_team_by_id(db, team_id)
        
        # Check if user is member of this team
        user_membership = db.query(TeamMember).filter(
            TeamMember.team_id == team_id,
            TeamMember.user_id == current_user.id
        ).first()
        
        if not user_membership:
            raise HTTPException(
                status_code=400,
                detail="You are not a member of this team"
            )
        
        # Check if user is the last moderator
        if user_membership.is_moderator:
            moderator_count = db.query(TeamMember).filter(
                TeamMember.team_id == team_id,
                TeamMember.is_moderator == True
            ).count()
            
            if moderator_count == 1:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot leave team as the only moderator. Assign another moderator first or delete the team."
                )
        
        # Remove user from team - note: using remove_member function from team_member_service
        # The function signature is: remove_member(db, team_id, remover_id, user_id)
        # For leaving, the remover is the same as the user leaving
        remove_member(db, team_id, current_user.id, current_user.id)
        
        # Redirect to teams page
        response = RedirectResponse(url="/team", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "error": e.detail,
                "team": team
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "teams/team-detail.html",
            {
                "request": request,
                "error": f"Error leaving team: {str(e)}",
                "team": team
            }
        )
