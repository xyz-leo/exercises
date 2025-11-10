"""
Task management routes for CRUD operations and filtering.

This module defines API endpoints for task management, including
creation, retrieval, updating, deletion of tasks, and various filtering options.
"""

# app/routers/task_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskRead
from app.services import task_service as TaskService
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user_model import User

# Router instance for task-related endpoints
# prefix="/tasks" means all routes will be under /tasks
# tags=["Tasks"] groups these endpoints in API documentation
router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    Creates a new task with the provided information. A task must have either
    an owner_id (personal task) with or not team_id (team task).
    Validates that the owner and team (if provided) exist.
    
    Args:
        task_data: Task creation data including title, description, status, etc.
        db: Database session dependency
        
    Returns:
        TaskRead: Created task information including system-generated fields
        
    Raises:
        HTTPException: 400 if owner or team not found, or invalid task assignment
        HTTPException: 500 if internal server error occurs
        
    Example:
    curl -X POST "http://127.0.0.1:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Study FastAPI documentation", 
       "status": "in_progress",
       "owner_id": 1, "team_id": 1
     }'

    """
    return TaskService.create_task(db, task_data)


@router.get("/", response_model=list[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    """
    Retrieve all tasks.
    
    Returns a list of all tasks in the system, including both personal
    and team tasks.
    
    Args:
        db: Database session dependency
        
    Returns:
        list[TaskRead]: List of all tasks
        
    Example:
    curl -X GET http://127.0.0.1:8000/tasks/
    """
    return TaskService.get_all_tasks(db)


@router.get("/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific task by ID.
    
    Args:
        task_id: ID of the task to retrieve
        db: Database session dependency
        
    Returns:
        TaskRead: Task information
        
    Raises:
        HTTPException: 404 if task not found
        
    Example:
    curl -X GET http://127.0.0.1:8000/tasks/1
    """
    return TaskService.get_task_by_id(db, task_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task by ID.
    
    Supports partial updates - only provided fields will be modified.
    Validates task ownership logic (task must have either owner OR team).
    
    Args:
        task_id: ID of the task to update
        task_data: Update data (partial updates supported)
        db: Database session dependency
        
    Returns:
        TaskRead: Updated task information
        
    Raises:
        HTTPException: 404 if task not found
        HTTPException: 400 if ownership validation fails
        
    Example:
    curl -X PUT "http://127.0.0.1:8000/tasks/7" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "123123Learn FastAPI",
       "description": "123123Study FastAPI documentation", 
       "status": "completed", "team_id": 3
     }'
    """
    return TaskService.update_task(db, task_id, task_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.
    
    Permanently removes the task from the system.
    Returns 204 No Content on successful deletion.
    
    Args:
        task_id: ID of the task to delete
        db: Database session dependency
        
    Returns:
        None: 204 No Content on success
        
    Raises:
        HTTPException: 404 if task not found
        
    Example:
    curl -X DELETE "http://127.0.0.1:8000/tasks/2"
    """
    TaskService.delete_task(db, task_id)
    return None


@router.get("/user/{user_id}", response_model=list[TaskRead])
def get_tasks_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all tasks owned by a specific user.
    
    Returns tasks where the specified user is the owner, regardless of
    whether the tasks are personal or assigned to a team.
    
    Args:
        user_id: ID of the user (task owner)
        db: Database session dependency
        
    Returns:
        list[TaskRead]: List of tasks owned by the user
        
    Example:
    curl -X GET http://127.0.0.1:8000/tasks/user/1	
    """
    return TaskService.get_tasks_by_owner(db, user_id)


@router.get("/team/{team_id}", response_model=list[TaskRead])
def get_tasks_by_team(team_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all tasks assigned to a specific team.
    
    Returns tasks that are assigned to the specified team.
    These tasks may have different owners within the team.
    
    Args:
        team_id: ID of the team
        db: Database session dependency
        
    Returns:
        list[TaskRead]: List of tasks assigned to the team
        
    Example:
    curl -X GET "http://127.0.0.1:8000/tasks/team/1"
    """
    return TaskService.get_tasks_by_team(db, team_id)

@router.get("/status/{status}", response_model=list[TaskRead])
def get_tasks_by_status(
    status: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all tasks with a specific status for the current user.
    
    Filters tasks by their current status (e.g., "pending", "in_progress", "completed")
    and ensures only the current user's tasks are returned.
    
    Args:
        status: Task status to filter by
        db: Database session dependency
        current_user: Authenticated user
        
    Returns:
        list[TaskRead]: List of tasks with the specified status owned by the current user
        
    Example:
        curl -X GET http://127.0.0.1:8000/tasks/status/in_progress
        GET /tasks/status/pending
        GET /tasks/status/in_progress  
        GET /tasks/status/completed
    """
    return TaskService.get_tasks_by_status(db, status, current_user.id)
