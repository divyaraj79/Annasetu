from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.donation_item import (
    DonationItemCreate,
    DonationItemResponse,
    DonationItemUpdate,
)
from app.services.donation_item_service import DonationItemService

router = APIRouter(prefix="/donation-items", tags=["donation-items"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DonationItemResponse, status_code=status.HTTP_201_CREATED)
def create_donation_item(
    donation_item: DonationItemCreate,
    db: Session = Depends(get_db)
):
    service = DonationItemService(db)

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
    db: Session = Depends(get_db)
):
    service = DonationItemService(db)
    donation_item = service.get_by_id(donation_item_id)
    if not donation_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation item not found")
    
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
def delete_donation_item(donation_item_id: UUID, db: Session = Depends(get_db)):
    service = DonationItemService(db)
    donation_item = service.get_by_id(donation_item_id)
    if not donation_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation item not found")
    
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
