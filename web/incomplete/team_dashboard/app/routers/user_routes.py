"""
User management routes for CRUD operations.

This module defines API endpoints for user management, including
creation, retrieval, updating, and deletion of user accounts.
"""

# app/routers/user_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, PasswordChange
from app.services import user_service as UserService
from app.core.database import get_db


# Router instance for user-related endpoints
# prefix="/users" means all routes will be under /users
# tags=["Users"] groups these endpoints in API documentation
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    
    Returns the user data for the currently authenticated user based on the JWT token.
    This endpoint requires a valid JWT token in the Authorization header.
    
    Args:
        current_user: Automatically injected from JWT token
        
    Returns:
        UserResponse: Current user's information
        
    Raises:
        HTTPException: 401 if token is invalid or expired

    Usage example: curl -X GET "http://localhost:8000/users/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
    """
    return current_user


@router.put("/password", response_model=UserResponse)
def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change current user's password.
    
    Validates current password and sets new password.
    
    Args:
        password_data: Current and new password data
        db: Database session dependency
        current_user: Currently authenticated user
        
    Returns:
        UserResponse: Updated user information
        
    Raises:
        HTTPException: 400 if current password is incorrect
        
    Example:
    curl -X PUT http://127.0.0.1:8000/users/password \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN_AQUI" \
  -d '{"current_password": "admin", "new_password": "password"}'

    """
    updated_user = UserService.change_user_password(db, current_user.id, password_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    
    Creates a new user account with the provided information. The password
    is automatically hashed before storage. Validates unique username and email.
    
    Args:
        user_data: User creation data including username, email, and password
        db: Database session dependency
        
    Returns:
        UserResponse: Created user information (excluding password)
        
    Raises:
        HTTPException: 400 if username or email already exists
        HTTPException: 500 if internal server error occurs
        
    Example:
    curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "email": "admin@admin.com", "password": "admin"}'

    """
    user = UserService.create_user(db, user_data)
    return user


@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.
    
    Returns a list of all registered users. User passwords are excluded
    from the response for security.
    
    Args:
        db: Database session dependency
        
    Returns:
        list[UserResponse]: List of all users
        
    Example:
     curl -X GET http://127.0.0.1:8000/users/
    """
    users = UserService.get_all_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by its ID.
    
    Args:
        user_id: ID of the user to retrieve
        db: Database session dependency
        
    Returns:
        UserResponse: User information
        
    Raises:
        HTTPException: 404 if user not found
        
    Example:
    curl -X GET http://127.0.0.1:8000/users/1
    """
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user's information by ID.
    
    Supports partial updates - only provided fields will be modified.
    Validates uniqueness of new username and email if provided.
    
    Args:
        user_id: ID of the user to update
        user_data: Update data (partial updates supported)
        db: Database session dependency
        
    Returns:
        UserResponse: Updated user information
        
    Raises:
        HTTPException: 404 if user not found
        HTTPException: 400 if username or email already taken
        
    Example:
    curl -X PUT http://127.0.0.1:8000/users/1 \
-H "Content-Type: application/json" \
-d '{"username": "Master Updated", "email": "master_new@example.com"}'

    """
    updated_user = UserService.update_user(db, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    
    Permanently removes the user account and associated data.
    Returns 204 No Content on successful deletion.
    
    Args:
        user_id: ID of the user to delete
        db: Database session dependency
        
    Returns:
        None: 204 No Content on success
        
    Raises:
        HTTPException: 404 if user not found
        
    Example:
        curl -X DELETE "http://127.0.0.1:8000/users/1"
    """
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None
