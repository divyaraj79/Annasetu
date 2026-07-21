from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.dependencies import require_role
from app.enums.roles import UserRole
from app.models.user import User

from app.schemas.restaurant import RestaurantResponse
from app.schemas.ngo import NGOResponse

from app.services.registration_service import RegistrationService

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get(
    "/restaurants/pending",
    response_model=list[RestaurantResponse],
)
def get_pending_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = RegistrationService(db)

    return service.get_pending_restaurants()


@router.get(
    "/ngos/pending",
    response_model=list[NGOResponse],
)
def get_pending_ngos(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = RegistrationService(db)

    return service.get_pending_ngos()

@router.post(
    "/restaurants/{restaurant_id}/approve",
    response_model=RestaurantResponse,
)
def approve_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = RegistrationService(db)

    try:
        return service.approve_restaurant_registration(
            restaurant_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    

@router.post(
    "/ngos/{ngo_id}/approve",
    response_model=NGOResponse,
)
def approve_ngo(
    ngo_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = RegistrationService(db)

    try:
        return service.approve_ngo_registration(
            ngo_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    

@router.post(
    "/restaurants/{restaurant_id}/reject",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reject_restaurant(
    restaurant_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = RegistrationService(db)

    try:
        service.reject_restaurant_registration(
            restaurant_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return None


@router.post(
    "/ngos/{ngo_id}/reject",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reject_ngo(
    ngo_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN)
    ),
):
    service = RegistrationService(db)

    try:
        service.reject_ngo_registration(
            ngo_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return None