"""
User service layer for business logic operations.

This module contains the business logic for user management operations,
including creation, retrieval, updating, and deletion of users.
Handles password hashing, validation, and data integrity checks.
"""

# app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, PasswordChange


def create_user(db: Session, user_data: UserCreate) -> User:
    """
    Creates a new user with hashed password.
    
    Performs validation checks for duplicate usernames and emails,
    hashes the password, and persists the user to the database.
    
    Args:
        db: Database session for executing queries
        user_data: User creation data including username, email, and password
        
    Returns:
        User: Newly created user object
        
    Raises:
        HTTPException: 400 if username or email already exists
        HTTPException: 500 if database operation fails
    """
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user instance
        new_user = User(
            username=user_data.username,
            email=user_data.email,
        )
        
        # Hash and set password using model method
        # This ensures consistent password hashing across the application
        new_user.set_password(user_data.password)
        
        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
        
    except HTTPException:
        # Re-raise HTTP exceptions to maintain error response consistency
        raise
    except Exception as e:
        # Rollback transaction on unexpected errors
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


def get_all_users(db: Session) -> list[User]:
    """
    Retrieve all users from database.
    
    Args:
        db: Database session
        
    Returns:
        list[User]: List of all users
        
    Raises:
        HTTPException: 500 if database query fails
    """
    try:
        return db.query(User).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )


def get_user_by_id(db: Session, user_id: int) -> User:
    """
    Retrieve a user by ID.
    
    Args:
        db: Database session
        user_id: ID of the user to retrieve
        
    Returns:
        User: Requested user object
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """
    Update user information.
    
    Supports partial updates - only provided fields will be modified.
    Validates uniqueness of new username and email if provided.
    
    Args:
        db: Database session
        user_id: ID of the user to update
        user_data: Data to update (partial updates supported)
        
    Returns:
        User: Updated user object
        
    Raises:
        HTTPException: 404 if user not found
        HTTPException: 400 if new username or email already taken
        HTTPException: 500 if database operation fails
    """
    try:
        # Find user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Update fields if provided
        update_data = user_data.model_dump(exclude_unset=True)
        
        if "username" in update_data and update_data["username"]:
            # Check if new username is taken by another user
            existing_user = db.query(User).filter(
                User.username == update_data["username"],
                User.id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
            user.username = update_data["username"]
        
        if "email" in update_data and update_data["email"]:
            # Check if new email is taken by another user
            existing_email = db.query(User).filter(
                User.email == update_data["email"],
                User.id != user_id
            ).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            user.email = update_data["email"]
        
        if "password" in update_data and update_data["password"]:
            # Hash and set new password
            user.set_password(update_data["password"])
        
        # Commit changes
        db.commit()
        db.refresh(user)
        
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )


def delete_user(db: Session, user_id: int) -> bool:
    """
    Delete a user by ID.
    
    Args:
        db: Database session
        user_id: ID of the user to delete
        
    Returns:
        bool: True if deletion was successful
        
    Raises:
        HTTPException: 404 if user not found
        HTTPException: 500 if database operation fails
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        db.delete(user)
        db.commit()
        
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )


def get_user_by_email(db: Session, email: str) -> User:
    """
    Retrieve a user by email address.
    
    Used primarily for authentication purposes.
    
    Args:
        db: Database session
        email: Email address to search for
        
    Returns:
        User: User with matching email, or None if not found
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User:
    """
    Retrieve a user by username.
    
    Args:
        db: Database session
        username: Username to search for
        
    Returns:
        User: User with matching username, or None if not found
    """
    return db.query(User).filter(User.username == username).first()


def change_user_password(db: Session, user_id: int, password_data: PasswordChange) -> User:
    """
    Change user password.
    
    Validates current password and sets new password.
    
    Args:
        db: Database session
        user_id: ID of the user to update
        password_data: Current and new password data
        
    Returns:
        User: Updated user object
        
    Raises:
        HTTPException: 404 if user not found
        HTTPException: 400 if current password is incorrect
        HTTPException: 500 if database operation fails
    """
    try:
        # Find user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not user.verify_password(password_data.current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Set new password
        user.set_password(password_data.new_password)
        
        # Commit changes
        db.commit()
        db.refresh(user)
        
        return user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error changing password: {str(e)}"
        )
