import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:Anil@localhost:5432/healthcare_db"
    
    # Add more configuration options
    APP_NAME: str = "Facility-Microservice"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Connection pool settings
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    
    # Service URLs with environment variable support
    DOCTOR_SERVICE_URL: str = "http://localhost:8001"
    PATIENT_SERVICE_URL: str = "http://localhost:8002"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()




