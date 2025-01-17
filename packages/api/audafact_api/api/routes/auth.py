from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import User
from ...core.jwt import create_access_token, decode_token, create_refresh_token
from ...core.email import send_verification_email
from ...core.redis import (
    store_verification_code,
    get_verification_code,
    delete_verification_code,
)
from ...core.rate_limit import check_rate_limit
from ...core.logging import logger
from ...api.schemas.auth import (
    VerificationRequest,
    VerificationResponse,
    SendVerificationRequest,
    ResendVerificationRequest,
    UserResponse,
)
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])


def generate_verification_code():
    return "".join(random.choices(string.digits, k=6))


@router.post("/send-verification", response_model=VerificationResponse)
async def send_verification(
    request: SendVerificationRequest, db: Session = Depends(get_db)
):
    try:
        # Check rate limit
        await check_rate_limit(f"send_verification:{request.email}", 5, 3600)

        # Check if user already exists
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            # Create new user
            user = User(email=request.email)
            db.add(user)
            db.commit()
            logger.info(f"New user created: {request.email}")

        # Generate and store code
        code = generate_verification_code()
        await store_verification_code(request.email, code)

        # Send email
        await send_verification_email(request.email, code)

        logger.info(f"Verification code sent to {request.email}")
        return {"success": True, "message": "Verification code sent"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error sending verification code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Add RefreshTokenRequest schema
class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        # Verify that this is a refresh token
        payload = decode_token(request.refresh_token, token_type="refresh")
        user_id = payload.get("sub")

        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create new tokens
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/verify", response_model=VerificationResponse)
async def verify_code(request: VerificationRequest, db: Session = Depends(get_db)):
    try:
        # Check rate limit
        await check_rate_limit(f"verify:{request.email}", 10, 3600)

        stored_code = await get_verification_code(request.email)
        if not stored_code or stored_code.decode() != request.code:
            logger.warning(f"Invalid verification attempt for {request.email}")
            raise HTTPException(status_code=400, detail="Invalid verification code")

        # Get or create user and mark as verified
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            user = User(email=request.email, is_verified=True)
            db.add(user)
        else:
            user.is_verified = True
        db.commit()

        # Clear the verification code
        await delete_verification_code(request.email)

        # Generate JWT token
        token = create_access_token(data={"sub": str(user.id), "email": user.email})

        logger.info(f"Email verified successfully for {request.email}")
        return {
            "success": True,
            "message": "Email verified successfully",
            "token": token,
            "user": UserResponse(
                id=user.id, email=user.email, is_verified=user.is_verified
            ),
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Error verifying code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resend-code", response_model=VerificationResponse)
async def resend_code(
    request: ResendVerificationRequest, db: Session = Depends(get_db)
):
    try:
        # Check rate limit
        await check_rate_limit(f"resend:{request.email}", 3, 3600)

        # Check if user exists
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            user = User(email=request.email)
            db.add(user)
            db.commit()

        code = generate_verification_code()
        await store_verification_code(request.email, code)
        await send_verification_email(request.email, code)

        logger.info(f"Verification code resent to {request.email}")
        return {"success": True, "message": "New verification code sent"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error resending code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
