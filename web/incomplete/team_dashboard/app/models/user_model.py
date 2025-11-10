"""
User data model and authentication utilities.

This module defines the User model for database storage and provides
password hashing/verification functionality using Argon2.
"""

# app/models/user_model.py
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from passlib.context import CryptContext
from datetime import datetime

from app.core.database import Base


# Password hashing context using Argon2
# Argon2 is a modern, secure hashing algorithm winner of the Password Hashing Competition
pwd_context = CryptContext(
    schemes=["argon2"],  # Use Argon2 for password hashing
    deprecated="auto",   # Automatically handle deprecated schemes
    bcrypt__rounds=12    # Number of hashing rounds (security parameter)
)


class User(Base):
    """
    User model representing application users.
    
    Stores user authentication information and relationships to teams and tasks.
    Provides methods for secure password handling.
    """
    
    __tablename__ = "users"

    # Primary key and unique identifiers
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    
    # Authentication
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    
    # Optional user information
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)

    # Relationships
    # Many-to-Many relationship with Team via TeamMember join table
    teams: Mapped[List["TeamMember"]] = relationship(
        "TeamMember",
        back_populates="user",
        cascade="all, delete-orphan"  # Delete team members when user is deleted
    )

    # One-to-Many relationship with Task (tasks owned by this user)
    tasks: Mapped[List["Task"]] = relationship(
        "Task",
        back_populates="owner",
        cascade="all, delete-orphan"  # Delete tasks when user is deleted
    )

    # Timestamps with timezone
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),  # Uses database server time
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),  # Auto-update on row change
        nullable=False
    )

    # ----------------------------
    # Password utilities
    # ----------------------------

    def set_password(self, plain_password: str):
        """
        Hashes and sets the user's password.
        
        Uses Argon2 for secure password hashing. Automatically handles
        password length limitations of the hashing algorithm.
        
        Args:
            plain_password: The plain text password to hash
            
        Note:
            Argon2 has a maximum input size of 72 bytes for security reasons
        """
        MAX_BCRYPT_BYTES = 72
        # Convert to bytes and truncate if necessary
        password_bytes = plain_password.encode("utf-8")[:MAX_BCRYPT_BYTES]
        # Hash and store the password
        self.password_hash = pwd_context.hash(password_bytes)

    def verify_password(self, plain_password: str) -> bool:
        """
        Verifies a plain password against the stored hash.
        
        Args:
            plain_password: The plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, self.password_hash)
