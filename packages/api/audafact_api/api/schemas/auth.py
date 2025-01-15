from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List


class SendVerificationRequest(BaseModel):
    email: EmailStr
    trackName: Optional[str] = None
    artistName: Optional[str] = None
    selections: Optional[Dict[str, List[str]]] = None


class VerificationRequest(BaseModel):
    email: EmailStr
    code: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class VerificationResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None
