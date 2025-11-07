from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    PROJECT_NAME: str = "Ultron Learning Assistant API"
    PROJECT_VERSION: str = "0.1.0"
    DESCRIPTION: str = "API for registration, authorization, and chatbot functionality."
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]

    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./app/db/main.db"


    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security
    SESSION_DURATION_MINUTES: int = 60
    LOGIN_RATE_LIMIT_ATTEMPTS: int = 3
    LOGIN_RATE_LIMIT_EXPIRE_SECONDS: int = 300

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
