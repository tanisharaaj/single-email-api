from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Temporal
    TEMPORAL_NAMESPACE: str
    TEMPORAL_TASK_QUEUE: str
    TEMPORAL_API_KEY: str

    # SendGrid
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    SENDGRID_TEMPLATE_ID: str

    # Auth
    AUTH_STATIC_BEARER_TOKEN: str

    class Config:
        env_file = ".env"


settings = Settings()
