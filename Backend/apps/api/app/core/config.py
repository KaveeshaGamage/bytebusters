import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Waypoint Delivery Planning System"
    ENV: str = "development"
    
    # Business Clock & Demo Mode (D11)
    DEMO_MODE: bool = True
    DEMO_NOW: str = "2025-07-31T14:00:00+05:30"
    SEED_DELIVERY_DATE: str = "2025-08-01"
    TIMEZONE: str = "Asia/Colombo"
    
    # Database
    DATABASE_URL: str = "sqlite:///./waypoint_dev.db"
    
    # Auth & Security
    SECRET_KEY: str = "waypoint_super_secret_jwt_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:3001,"
        "http://localhost:5173,http://localhost:5174,"
        "http://127.0.0.1:3000,http://127.0.0.1:3001,"
        "http://127.0.0.1:5173,http://127.0.0.1:5174"
    )
    
    # Operational Config Defaults
    DELAY_ALERT_MIN: int = 15
    RELOAD_BUFFER_MIN: int = 0
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
