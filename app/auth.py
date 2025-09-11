from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from app.settings import settings


def require_auth(credentials: HTTPAuthorizationCredentials):
    if credentials.credentials != settings.AUTH_STATIC_BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
