from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """MongoDB connection settings"""
    # MongoDB connection
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "admin"
    mongodb_username: Optional[str] = None
    mongodb_password: Optional[str] = None
    
    # Connection pool settings
    mongodb_max_pool_size: int = 100
    mongodb_min_pool_size: int = 10
    mongodb_max_idle_time_ms: int = 300000
    
    # Logging settings
    log_level: str = "INFO"
    
    # Security settings
    api_key: str = "your-secret-api-key"
    
    # Account settings
    account: str = "admin"
    password: str = "your-password-change-in-production"

    # CORS settings
    cors_allow_origin: str = "*"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()
