"""
Application configuration and settings management.

This module handles all environment-based configuration using Pydantic Settings.
It loads configuration from environment variables and .env file, providing
type-safe access to application settings throughout the codebase.
"""

# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """
    Application settings configuration.
    
    All settings can be overridden by environment variables or .env file.
    Uses Pydantic for validation and type conversion.
    """
    
    # Database connection URL - required for application startup
    DATABASE_URL: str
    
    # Debug mode - enables additional logging and debugging features
    DEBUG: bool = False
    
    # Base directory for the project - automatically calculated
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
 
    # JWT Configuration
    JWT_SECRET_KEY: str = "dev-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",           # Load from .env file
        env_file_encoding="utf-8", # File encoding
    )


# Global settings instance - import this throughout the application
settings = Settings()


# Debug utility - can be run directly to check configuration
if __name__ == "__main__":
    """
    Debug utility to print current configuration.
    
    Run with: python -m app.core.config
    Useful for verifying environment variables are loaded correctly.
    """
    print("=== Current Configuration ===")
    print("DATABASE_URL:", settings.DATABASE_URL)
    print("DEBUG:", settings.DEBUG)
    print("BASE_DIR:", settings.BASE_DIR)
    print("JWT_SECRET_KEY:", settings.JWT_SECRET_KEY)  
    print("ALGORITHM:", settings.ALGORITHM)
    print("ACCESS_TOKEN_EXPIRE_MINUTES:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)
