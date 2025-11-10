"""
FastAPI dependencies for request processing.

This module contains dependency functions that can be used in route handlers
to inject common functionality like authentication and database sessions.
"""

# app/core/dependencies.py
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import verify_token
from app.models.user_model import User


# HTTP Bearer security scheme for token authentication
security = HTTPBearer(auto_error=False)  # Changed to auto_error=False


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current user from JWT token.
    
    Supports both:
    - Authorization header (for API calls)
    - Cookie (for web templates)
    
    Args:
        request: FastAPI request object
        credentials: HTTP Bearer credentials from Authorization header (optional)
        db: Database session
        
    Returns:
        User: Authenticated user object
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    token = None
    
    # Try to get token from Authorization header first
    if credentials:
        token = credentials.credentials
    else:
        # Fallback to cookie for web requests
        token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    # Verify token validity
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    # Extract user ID from token payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    # Find user in database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


# Optional dependency for routes that work with or without authentication
def get_optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User | None:
    """
    Optional dependency that returns user if authenticated, None otherwise.
    
    Useful for routes that should work for both authenticated and 
    unauthenticated users.
    """
    try:
        return get_current_user(request, credentials, db)
    except HTTPException:
        return None
