"""
JWT authentication utilities.

This module provides functions for creating and verifying JWT tokens
used for user authentication throughout the API.
"""

# app/core/auth.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException

from app.core.config import settings


# JWT configuration from application settings
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    """
    Create a JWT access token with expiration.
    
    Args:
        data: Dictionary containing token payload (typically user info)
        
    Returns:
        str: Encoded JWT token string
        
    Example:
        token = create_access_token({"sub": "user@example.com", "user_id": 1})
    """
    to_encode = data.copy()
    
    # Add expiration time to token payload
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode the token using JWT_SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify JWT token and return payload if valid.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        dict: Token payload if valid, None if invalid or expired
        
    Raises:
        JWTError: If token is malformed or signature is invalid
    """
    try:
        # Decode and verify the token
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Return None for any JWT-related errors
        return None
