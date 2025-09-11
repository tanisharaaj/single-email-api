from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TEMPORAL_NAMESPACE: str
    TEMPORAL_TASK_QUEUE: str
    TEMPORAL_API_KEY: str
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_TEMPLATE_ID: str
    AUTH_STATIC_BEARER_TOKEN: str
    CORS_ALLOW_ORIGINS: str   # no default here

    class Config:
        env_file = ".env"

settings = Settings()
