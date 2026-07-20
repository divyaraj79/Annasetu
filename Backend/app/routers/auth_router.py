from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.auth import (
    RegistrationRequest,
    LoginRequest,
    TokenResponse,
)

from app.schemas.user import UserResponse

from app.services.registration_service import RegistrationService
from app.auth.login_service import LoginService

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    registration_data: RegistrationRequest,
    db: Session = Depends(get_db),
):
    service = RegistrationService(db)

    try:
        return service.register(registration_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except Exception:
        raise


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    service = LoginService(db)

    try:
        return service.login(login_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    except Exception:
        raise