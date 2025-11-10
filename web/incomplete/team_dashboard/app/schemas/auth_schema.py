"""
Authentication request and response schemas.

This module defines Pydantic models for authentication-related API operations,
including login requests and token responses.
"""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """
    Schema for user login requests.
    
    Used in the /auth/login endpoint to validate and parse login credentials.
    """
    email: EmailStr  # User's email address (validated as proper email format)
    password: str    # User's password (plain text, will be verified against hash)


class TokenResponse(BaseModel):
    """
    Schema for JWT token responses.
    
    Returned by the /auth/login endpoint upon successful authentication.
    Contains the access token and token type for Bearer authentication.
    """
    access_token: str  # JWT token for authenticated requests
    token_type: str    # Always "bearer" for Bearer token authentication
