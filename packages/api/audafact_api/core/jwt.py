from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException
from ..core.config import settings


def create_access_token(data: dict) -> str:
    """Create short-lived access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)  # 30 minutes
    to_encode.update({"exp": expire, "token_type": "access"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create long-lived refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)  # 30 days
    to_encode.update({"exp": expire, "token_type": "refresh"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str, token_type: Optional[str] = None) -> dict:
    """
    Decode and verify a token
    token_type: Optional verification of "access" or "refresh" token type
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )

        # Verify token type if specified
        if token_type and payload.get("token_type") != token_type:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token type. Expected {token_type} token.",
            )

        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
