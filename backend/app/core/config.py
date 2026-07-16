import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Settings
    PROJECT_NAME: str = "LLM Shield Platform"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    
    # Database Settings (Supabase)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    
    # Secure Email API (Resend)
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "mock_key_for_dev")
    
    # JWT Security Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super_secret_dev_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()