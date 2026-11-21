from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token

from app.schemas.auth import (
    LoginRequest,
    TokenResponse
)

from app.services.auth_service import authenticate_user


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db,
        data.username,
        data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "role": user.role.value,
        "hospital_id": user.hospital_id
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }