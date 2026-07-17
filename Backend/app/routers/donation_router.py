from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.donation import DonationCreate, DonationResponse, DonationUpdate
from app.services.donation_service import DonationService

router = APIRouter(prefix="/donations", tags=["donations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
def create_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    service = DonationService(db)
    return service.create(donation)


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
def update_donation(donation_id: UUID, donation_data: DonationUpdate, db: Session = Depends(get_db)):
    service = DonationService(db)
    donation = service.get_by_id(donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    return service.update(donation, donation_data)


@router.delete("/{donation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_donation(donation_id: UUID, db: Session = Depends(get_db)):
    service = DonationService(db)
    donation = service.get_by_id(donation_id)
    if not donation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Donation not found")
    service.delete(donation)
    return None
