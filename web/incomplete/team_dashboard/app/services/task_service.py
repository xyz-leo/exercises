"""
Task service layer for business logic operations.

This module contains the business logic for task management operations,
including creation, retrieval, updating, and deletion of tasks.
Handles task ownership validation and filtering operations.
"""

# app/services/task_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.task_model import Task
from app.models.team_model import Team
from app.schemas.task_schema import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """
    Create a new task in the database.
    
    Validates that the task owner exists and, if provided, the team exists.
    Ensures data integrity before persisting to the database.
    
    Args:
        db: Database session
        task_data: Task creation data including owner_id and optional team_id
        
    Returns:
        Task: Newly created task object
        
    Raises:
        HTTPException: 400 if owner or team not found
        HTTPException: 500 if database operation fails
    """
    try:
        # Validate that owner exists
        from app.models.user_model import User
        from app.models.team_model import Team
        
        owner = db.query(User).filter(User.id == task_data.owner_id).first()
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task owner not found"
            )
        
        # If team_id provided, validate team exists
        if task_data.team_id is not None:
            team = db.query(Team).filter(Team.id == task_data.team_id).first()
            if not team:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Team not found"
                )
        
        # Create new task
        new_task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            due_date=task_data.due_date,
            owner_id=task_data.owner_id,
            team_id=task_data.team_id
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        return new_task
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating task: {str(e)}"
        )


def get_all_tasks(db: Session) -> list[Task]:
    """
    Retrieve all tasks from database.
    
    Args:
        db: Database session
        
    Returns:
        list[Task]: List of all tasks
        
    Raises:
        HTTPException: 500 if database query fails
    """
    try:
        return db.query(Task).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


def get_task_by_id(db: Session, task_id: int) -> Task:
    """
    Retrieve a task by ID.
    
    Args:
        db: Database session
        task_id: ID of the task to retrieve
        
    Returns:
        Task: Requested task object
        
    Raises:
        HTTPException: 404 if task not found
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    """
    Update task information.
    
    Supports partial updates and validates task ownership logic
    (task must have either owner, team is optional).
    
    Args:
        db: Database session
        task_id: ID of the task to update
        task_data: Data to update (partial updates supported)
        
    Returns:
        Task: Updated task object
        
    Raises:
        HTTPException: 404 if task not found
        HTTPException: 400 if ownership validation fails
        HTTPException: 500 if database operation fails
    """
    try:
        # Find task
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update fields if provided
        update_data = task_data.model_dump(exclude_unset=True)
        
        # Validate owner_id and team_id logic if being updated
        if 'owner_id' in update_data or 'team_id' in update_data:
            new_owner_id = update_data.get('owner_id', task.owner_id)
            new_team_id = update_data.get('team_id', task.team_id)
            
            # Task must have either an owner or a team (not both, not neither)
            if new_owner_id is None and new_team_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Task must have either an owner or a team"
                )
            
        # Apply updates
        for field, value in update_data.items():
            if value is not None:  # Only update if value is provided
                setattr(task, field, value)
        
        # Commit changes
        db.commit()
        db.refresh(task)
        
        return task
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task by ID.
    
    Args:
        db: Database session
        task_id: ID of the task to delete
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: 404 if task not found
        HTTPException: 500 if database operation fails
    """
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        db.delete(task)
        db.commit()
        
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )


def get_tasks_by_owner(db: Session, owner_id: int) -> list[Task]:
    """
    Retrieve all tasks owned by a specific user.
    
    Args:
        db: Database session
        owner_id: ID of the task owner
        
    Returns:
        list[Task]: List of tasks owned by the user
        
    Raises:
        HTTPException: 500 if database query fails
    """
    try:
        return db.query(Task).filter(Task.owner_id == owner_id).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user tasks: {str(e)}"
        )


def get_tasks_by_team(db: Session, team_id: int) -> list[Task]:
    """
    Retrieve all tasks assigned to a specific team.
    
    Args:
        db: Database session
        team_id: ID of the team
        
    Returns:
        list[Task]: List of tasks belonging to the team
        
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
        
        # Return all tasks assigned to this team
        tasks = db.query(Task).filter(Task.team_id == team_id).all()
        return tasks
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving team tasks: {str(e)}"
        )


def get_tasks_by_status(db: Session, status: str, owner_id: int) -> list[Task]:
    """
    Retrieve all tasks with a specific status for a specific owner.
    
    Args:
        db: Database session
        status: Task status to filter by (e.g., "pending", "in_progress", "completed")
        owner_id: ID of the task owner
        
    Returns:
        list[Task]: List of tasks with the specified status owned by the user
        
    Raises:
        HTTPException: 500 if database query fails
    """
    try:
        return db.query(Task).filter(
            Task.status == status,
            Task.owner_id == owner_id
        ).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks by status: {str(e)}"
        )
