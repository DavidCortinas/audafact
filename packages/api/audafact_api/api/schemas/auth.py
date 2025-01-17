from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID


class SendVerificationRequest(BaseModel):
    email: EmailStr


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class VerificationRequest(BaseModel):
    email: EmailStr
    code: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True


class VerificationResponse(BaseModel):
    success: bool
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[UserResponse] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
