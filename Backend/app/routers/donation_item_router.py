from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.donation_item import (
    DonationItemCreate,
    DonationItemResponse,
    DonationItemUpdate,
)
from app.services.donation_item_service import DonationItemService

from app.auth.dependencies import get_current_user

from app.models.user import User
from app.enums.roles import UserRole

from app.models.donation import Donation
from app.models.restaurant import Restaurant

router = APIRouter(prefix="/donation-items", tags=["donation-items"])

@router.post("/", response_model=DonationItemResponse, status_code=status.HTTP_201_CREATED)
def create_donation_item(
    donation_item: DonationItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DonationItemService(db)

    donation = (
        db.query(Donation)
        .filter(Donation.id == donation_item.donation_id)
        .first()
    )

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found.",
        )

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
            detail="You are not authorized to modify this donation.",
        )

    try:
        created_donation_item = service.create(donation_item)

        db.commit()

        db.refresh(created_donation_item)

        return created_donation_item

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.get("/{donation_item_id}", response_model=DonationItemResponse)
def get_donation_item(donation_item_id: UUID, db: Session = Depends(get_db)):
    service = DonationItemService(db)
    donation_item = service.get_by_id(donation_item_id)
    if not donation_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation item not found")
    return donation_item


@router.get("/", response_model=list[DonationItemResponse])
def get_donation_items(db: Session = Depends(get_db)):
    service = DonationItemService(db)
    return service.get_all()


@router.put("/{donation_item_id}", response_model=DonationItemResponse)
def update_donation_item(
    donation_item_id: UUID,
    donation_item_data: DonationItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DonationItemService(db)
    donation_item = service.get_by_id(donation_item_id)
    if not donation_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation item not found")
    
    donation = (
        db.query(Donation)
        .filter(Donation.id == donation_item.donation_id)
        .first()
    )

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found.",
        )

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
            detail="You are not authorized to modify this donation.",
        )

    try:
        updated_donation_item = service.update(donation_item, donation_item_data)

        db.commit()

        db.refresh(updated_donation_item)

        return updated_donation_item

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        db.rollback()
        raise


@router.delete("/{donation_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donation_item(
    donation_item_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = DonationItemService(db)
    donation_item = service.get_by_id(donation_item_id)
    if not donation_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation item not found")
    
    donation = (
        db.query(Donation)
        .filter(Donation.id == donation_item.donation_id)
        .first()
    )

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found.",
        )

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
            detail="You are not authorized to modify this donation.",
        )

    try:
        service.delete(donation_item)

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
