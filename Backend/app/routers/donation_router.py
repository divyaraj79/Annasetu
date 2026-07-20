from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.donation import DonationCreate, DonationResponse, DonationUpdate
from app.services.donation_service import DonationService

from app.auth.dependencies import get_current_user
from app.models.user import User
from app.enums.roles import UserRole
from app.models.restaurant import Restaurant

router = APIRouter(prefix="/donations", tags=["donations"])

@router.post("/", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DonationService(db)

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == donation.restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found.",
        )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != restaurant.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to create this donation.",
        )

    try:
        donation = service.create(donation)

        db.commit()

        db.refresh(donation)

        return donation

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(donation_id: UUID, db: Session = Depends(get_db)):
    service = DonationService(db)
    donation = service.get_by_id(donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    return donation


@router.get("/", response_model=list[DonationResponse])
def get_donations(db: Session = Depends(get_db)):
    service = DonationService(db)
    return service.get_all()


@router.put("/{donation_id}", response_model=DonationResponse)
def update_donation(
    donation_id: UUID,
    donation_data: DonationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DonationService(db)
    donation = service.get_by_id(donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    
    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == donation.restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found.",
        )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != restaurant.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this donation.",
        )

    try:
        updated_donation = service.update(
            donation,
            donation_data,
        )

        db.commit()

        db.refresh(updated_donation)

        return updated_donation

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.delete("/{donation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donation(
    donation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DonationService(db)
    donation = service.get_by_id(donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")

    restaurant = (
        db.query(Restaurant)
        .filter(Restaurant.id == donation.restaurant_id)
        .first()
    )

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found.",
        )

    if (
        current_user.role != UserRole.ADMIN
        and current_user.id != restaurant.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this donation.",
        )

    try:
        service.delete(donation)
        db.commit()

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise

    return None
