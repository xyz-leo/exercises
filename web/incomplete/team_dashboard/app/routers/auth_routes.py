"""
Authentication routes for user login and token management.

This module defines API endpoints for user authentication, including
JWT token generation and validation.
"""

# app/routers/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import create_access_token
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.models.user_model import User

# Router instance for authentication endpoints
# prefix="/auth" means all routes will be under /auth
# tags=["Authentication"] groups these endpoints in API documentation
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Verifies user credentials (email and password) and returns a JWT token
    for authenticated requests. The token includes user ID and email in its payload.
    
    Args:
        credentials: LoginRequest containing email and password
        db: Database session dependency
        
    Returns:
        TokenResponse: JWT access token and token type
        
    Raises:
        HTTPException: 401 if email or password is invalid
        
    Example:
    curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@admin.com", "password": "admin"}'

    """
    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # Verify user exists and password is correct
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create access token with user information in payload
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
