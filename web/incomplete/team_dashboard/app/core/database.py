"""
Database configuration and connection management.

This module sets up SQLAlchemy database connection, session management,
and provides the base class for all data models.
"""

# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings


# Create database engine - the core interface to the database
# pool_pre_ping: Checks connection validity before using
# echo: Logs all SQL statements (useful for debugging)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Check connection before using
    echo=settings.DEBUG   # Log SQL in debug mode
)

# Session factory - used to create individual database sessions
# autocommit=False: Use explicit transactions
# autoflush=False: Control when changes are sent to database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models
# All model classes should inherit from this
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function for FastAPI to provide database sessions.
    
    Yields:
        Session: SQLAlchemy database session
        
    Usage in FastAPI:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
            
    The session is automatically closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables.
    
    This should be called once at application startup.
    In production, consider using Alembic migrations instead.
    """
    
    # Create all tables that don't already exist
    Base.metadata.create_all(bind=engine)
