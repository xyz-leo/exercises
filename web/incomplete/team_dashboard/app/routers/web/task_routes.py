from fastapi import APIRouter, Depends, Request, Form, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.services.task_service import (
    create_task, get_all_tasks, get_task_by_id, 
    update_task, delete_task, get_tasks_by_owner,
    get_tasks_by_team, get_tasks_by_status
)
from app.schemas.task_schema import TaskCreate, TaskUpdate
from app.models.user_model import User
from app.models.team_model import Team

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/task", response_class=HTMLResponse)
async def tasks_page(
    request: Request,
    filter_type: str = Query("all", alias="filter"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Display tasks page with filtering options.
    Filter types: all, my_tasks, team_tasks, by_status
    """
    try:
        tasks = []
        
        if filter_type == "team_tasks":
            # Get tasks where user is member of the team
            user_team_ids = [tm.team_id for tm in current_user.teams]
            if user_team_ids:
                tasks = db.query(Task).filter(Task.team_id.in_(user_team_ids)).all()
        elif filter_type.startswith("status:"):
            status = filter_type.split(":")[1]
            tasks = get_tasks_by_status(db, status, current_user.id)
        else:
            tasks = get_tasks_by_owner(db, current_user.id)

        
        # Get user's teams for the create task form
        user_teams = [tm.team for tm in current_user.teams]
        
        return templates.TemplateResponse(
            "tasks/tasks.html",
            {
                "request": request,
                "tasks": tasks,
                "current_user": current_user,
                "user_teams": user_teams,
                "filter_type": filter_type,
                "status_options": ["pending", "in_progress", "completed", "cancelled"]
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "tasks/tasks.html",
            {
                "request": request,
                "error": f"Error loading tasks: {str(e)}",
                "tasks": [],
                "current_user": current_user,
                "user_teams": [],
                "filter_type": filter_type
            }
        )


@router.get("/task/create", response_class=HTMLResponse)
async def create_task_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display task creation form"""
    try:
        user_teams = [tm.team for tm in current_user.teams]
        
        return templates.TemplateResponse(
            "tasks/create-task.html",
            {
                "request": request,
                "current_user": current_user,
                "user_teams": user_teams,
                "status_options": ["pending", "in_progress", "completed", "cancelled"]
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "tasks/create-task.html",
            {
                "request": request,
                "error": f"Error loading form: {str(e)}",
                "current_user": current_user,
                "user_teams": []
            }
        )


@router.post("/task/create")
async def create_task_submit(
    request: Request,
    title: str = Form(...),
    description: str = Form(None),
    status: str = Form("pending"),
    due_date: str = Form(None),
    team_id: str = Form(None),  # string to handle empty/None
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle task creation form submission"""
    try:
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            due_date_obj = datetime.fromisoformat(due_date)
        
        # Parse team_id if provided
        team_id_int = None
        if team_id and team_id != "none":
            team_id_int = int(team_id)
            # Verify user has access to this team
            user_team_ids = [tm.team_id for tm in current_user.teams]
            if team_id_int not in user_team_ids:
                raise HTTPException(
                    status_code=400,
                    detail="You don't have access to this team"
                )
        
        # Create task data
        task_data = TaskCreate(
            title=title,
            description=description,
            status=status,
            due_date=due_date_obj,
            owner_id=current_user.id,
            team_id=team_id_int
        )
        
        # Create the task
        new_task = create_task(db, task_data)
        
        # Redirect to tasks page
        response = RedirectResponse(url="/task", status_code=302)
        return response
        
    except HTTPException as e:
        user_teams = [tm.team for tm in current_user.teams]
        return templates.TemplateResponse(
            "tasks/create-task.html",
            {
                "request": request,
                "error": e.detail,
                "current_user": current_user,
                "user_teams": user_teams,
                "status_options": ["pending", "in_progress", "completed", "cancelled"],
                "form_data": request.form()  # Preserve form data
            }
        )
    except Exception as e:
        user_teams = [tm.team for tm in current_user.teams]
        return templates.TemplateResponse(
            "tasks/create-task.html",
            {
                "request": request,
                "error": f"Error creating task: {str(e)}",
                "current_user": current_user,
                "user_teams": user_teams,
                "status_options": ["pending", "in_progress", "completed", "cancelled"],
                "form_data": request.form()  # Preserve form data
            }
        )


@router.get("/task/{task_id}", response_class=HTMLResponse)
async def task_detail_page(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display task details"""
    try:
        task = get_task_by_id(db, task_id)
        
        # Check if user has access to this task
        has_access = (
            task.owner_id == current_user.id or
            (task.team_id and any(tm.team_id == task.team_id for tm in current_user.teams))
        )
        
        if not has_access:
            raise HTTPException(
                status_code=403,
                detail="You don't have access to this task"
            )
        
        return templates.TemplateResponse(
            "tasks/task-detail.html",
            {
                "request": request,
                "task": task,
                "current_user": current_user
            }
        )
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "tasks/task-detail.html",
            {
                "request": request,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "tasks/task-detail.html",
            {
                "request": request,
                "error": f"Error loading task: {str(e)}"
            }
        )


@router.get("/task/{task_id}/edit", response_class=HTMLResponse)
async def edit_task_page(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Display task edit form"""
    try:
        task = get_task_by_id(db, task_id)
        
        # Check if user can edit this task (owner or team moderator)
        can_edit = (
            task.owner_id == current_user.id or
            (task.team_id and any(
                tm.team_id == task.team_id and tm.role == "moderator" 
                for tm in current_user.teams
            ))
        )
        
        if not can_edit:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to edit this task"
            )
        
        user_teams = [tm.team for tm in current_user.teams]
        
        return templates.TemplateResponse(
            "tasks/edit-task.html",
            {
                "request": request,
                "task": task,
                "current_user": current_user,
                "user_teams": user_teams,
                "status_options": ["pending", "in_progress", "completed", "cancelled"]
            }
        )
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "tasks/edit-task.html",
            {
                "request": request,
                "error": e.detail
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "tasks/edit-task.html",
            {
                "request": request,
                "error": f"Error loading task: {str(e)}"
            }
        )


@router.post("/task/{task_id}/edit")
async def edit_task_submit(
    request: Request,
    task_id: int,
    title: str = Form(...),
    description: str = Form(None),
    status: str = Form(...),
    due_date: str = Form(None),
    team_id: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle task edit form submission"""
    try:
        task = get_task_by_id(db, task_id)
        
        # Check if user can edit this task
        can_edit = (
            task.owner_id == current_user.id or
            (task.team_id and any(
                tm.team_id == task.team_id and tm.role == "moderator" 
                for tm in current_user.teams
            ))
        )
        
        if not can_edit:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to edit this task"
            )
        
        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            due_date_obj = datetime.fromisoformat(due_date)
        
        # Parse team_id if provided
        team_id_int = None
        if team_id and team_id != "none":
            team_id_int = int(team_id)
            # Verify user has access to this team
            user_team_ids = [tm.team_id for tm in current_user.teams]
            if team_id_int not in user_team_ids:
                raise HTTPException(
                    status_code=400,
                    detail="You don't have access to this team"
                )
        
        # Create update data
        update_data = TaskUpdate(
            title=title,
            description=description,
            status=status,
            due_date=due_date_obj,
            team_id=team_id_int
        )
        
        # Update the task
        updated_task = update_task(db, task_id, update_data)
        
        # Redirect to task detail
        response = RedirectResponse(url=f"/task/{task_id}", status_code=302)
        return response
        
    except HTTPException as e:
        user_teams = [tm.team for tm in current_user.teams]
        return templates.TemplateResponse(
            "tasks/edit-task.html",
            {
                "request": request,
                "error": e.detail,
                "task": task,
                "current_user": current_user,
                "user_teams": user_teams,
                "status_options": ["pending", "in_progress", "completed", "cancelled"]
            }
        )
    except Exception as e:
        user_teams = [tm.team for tm in current_user.teams]
        return templates.TemplateResponse(
            "tasks/edit-task.html",
            {
                "request": request,
                "error": f"Error updating task: {str(e)}",
                "task": task,
                "current_user": current_user,
                "user_teams": user_teams,
                "status_options": ["pending", "in_progress", "completed", "cancelled"]
            }
        )


@router.post("/task/{task_id}/delete")
async def delete_task_submit(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle task deletion"""
    try:
        task = get_task_by_id(db, task_id)
        
        # Check if user can delete this task (owner or team moderator)
        can_delete = (
            task.owner_id == current_user.id or
            (task.team_id and any(
                tm.team_id == task.team_id and tm.role == "moderator" 
                for tm in current_user.teams
            ))
        )
        
        if not can_delete:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to delete this task"
            )
        
        # Delete the task
        delete_task(db, task_id)
        
        # Redirect to tasks page
        response = RedirectResponse(url="/task", status_code=302)
        return response
        
    except HTTPException as e:
        return templates.TemplateResponse(
            "tasks/task-detail.html",
            {
                "request": request,
                "error": e.detail,
                "task": task
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "tasks/task-detail.html",
            {
                "request": request,
                "error": f"Error deleting task: {str(e)}",
                "task": task
            }
        )
