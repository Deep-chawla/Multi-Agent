"""
Auth for the chat backend.

This service does NOT own the users table and does NOT talk to the auth
database. It only verifies JWTs that were issued by the auth service
(signup-login-main), which works as long as both services are configured
with the same SECRET_KEY and ALGORITHM.

The 'sub' claim of the access token is treated as the authoritative user id.
"""

from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config.settings import settings

security = HTTPBearer()


@dataclass
class CurrentUser:
    id: str


def verify_access_token(token: str) -> dict | None:
    """Decode and validate an access token issued by the auth service."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None

    if payload.get("type") != "access":
        return None

    return payload


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> CurrentUser:
    token = credentials.credentials

    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return CurrentUser(id=str(user_id))
