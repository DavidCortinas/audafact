from fastapi import APIRouter, HTTPException, Request
from pydantic import EmailStr
from typing import Optional
import random
import string
from audafact_api.core.email import send_verification_email
from audafact_api.core.redis import (
    store_verification_code,
    get_verification_code,
    delete_verification_code,
)
from audafact_api.core.rate_limit import check_rate_limit
from audafact_api.core.logging import logger
from audafact_api.api.schemas.auth import (
    VerificationRequest,
    VerificationResponse,
    SendVerificationRequest,
    ResendVerificationRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def generate_verification_code():
    return "".join(random.choices(string.digits, k=6))


@router.post("/send-verification", response_model=VerificationResponse)
async def send_verification(request: SendVerificationRequest):
    try:
        # Check rate limit (5 requests per hour per email)
        await check_rate_limit(f"send_verification:{request.email}", 5, 3600)

        # Generate and store code
        code = generate_verification_code()
        await store_verification_code(request.email, code)

        # Send email
        await send_verification_email(request.email, code)

        logger.info(f"Verification code sent to {request.email}")
        return {"success": True, "message": "Verification code sent"}
    except HTTPException as he:
        logger.warning(f"Rate limit exceeded for {request.email}")
        raise he
    except Exception as e:
        logger.error(f"Error sending verification code to {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify", response_model=VerificationResponse)
async def verify_code(request: VerificationRequest):
    try:
        # Check rate limit (10 attempts per hour)
        await check_rate_limit(f"verify:{request.email}", 10, 3600)

        stored_code = await get_verification_code(request.email)

        if not stored_code or stored_code.decode() != request.code:
            logger.warning(f"Invalid verification attempt for {request.email}")
            raise HTTPException(status_code=400, detail="Invalid verification code")

        # Clear the verification code
        await delete_verification_code(request.email)

        logger.info(f"Email verified successfully for {request.email}")
        return {"success": True, "message": "Email verified successfully"}
    except Exception as e:
        logger.error(f"Error verifying code for {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resend-code", response_model=VerificationResponse)
async def resend_code(request: ResendVerificationRequest):
    try:
        # Check rate limit (3 resend requests per hour)
        await check_rate_limit(f"resend:{request.email}", 3, 3600)

        code = generate_verification_code()
        await store_verification_code(request.email, code)

        await send_verification_email(request.email, code)

        logger.info(f"Verification code resent to {request.email}")
        return {"success": True, "message": "New verification code sent"}
    except Exception as e:
        logger.error(f"Error resending code to {request.email}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
