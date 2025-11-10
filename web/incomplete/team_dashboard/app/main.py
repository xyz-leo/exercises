"""
FastAPI application entry point and configuration.

This module initializes the FastAPI application, configures middleware,
registers all API routers, and sets up application lifecycle events.
"""

# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.database import init_db

# Import all route modules to register them with the application
from app.routers import (
    user_routes,
    team_routes,
    task_routes,
    team_member_routes,
    auth_routes,
)
from app.routers.web import router as web_routes

# Initialize the database connection and create tables
# This should be called once at application startup
# In production, consider using Alembic migrations instead
init_db()

# Create the FastAPI application instance
# This is the main application object that handles all HTTP requests
app = FastAPI(
    title="Team Dashboard API",
    description="A prototype API for managing teams, tasks, and members. Built with FastAPI.",
    version="1.0.0",
)


# Mount static files directory
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


# --- Include all Routers ---
# Each router module handles a specific resource and its endpoints
# The order doesn't matter for routing, but affects documentation grouping
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(team_routes.router)
app.include_router(task_routes.router)
app.include_router(team_member_routes.router)
app.include_router(web_routes)


# --- Root Route ---
@app.get("/")
def root():
    """
    Health check endpoint.
    
    Can be used to verify that the API is running and accessible.
    Returns a simple message indicating the API status.
    
    Returns:
        dict: Simple status message
        
    Example:
        GET /
        Response: {"message": "Team Dashboard API is running successfully."}
    """
    return {"message": "Team Dashboard API is running successfully."}


# --- Application Events ---
# Optional startup and shutdown hooks for resource management

@app.on_event("startup")
def on_startup():
    """
    Code executed when the app starts.
    
    This function is called when the application starts up.
    Good place to initialize connections, load configuration, or setup cache.
    
    Currently used for debug output. In production, you might:
    - Initialize connection pools
    - Load configuration from external sources
    - Setup monitoring and logging
    """
    print("Application startup: resources initialized.")


@app.on_event("shutdown")
def on_shutdown():
    """
    Code executed when the app stops.
    
    This function is called when the application is shutting down.
    Good place to close connections, cleanup resources, or perform graceful shutdown.
    
    Currently used for debug output. In production, you might:
    - Close database connections
    - Cleanup temporary files
    - Notify monitoring systems
    """
    print("Application shutdown: resources released.")
