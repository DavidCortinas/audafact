from fastapi import Request, HTTPException
from typing import Optional
from ...core.jwt import decode_token
from ...database import get_db
from ...models import User
from sqlalchemy.orm import Session


async def get_authenticated_user(
    request: Request, db: Session = Depends(get_db)
) -> Optional[User]:
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
