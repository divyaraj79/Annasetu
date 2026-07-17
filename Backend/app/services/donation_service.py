from uuid import UUID

from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class DonationService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donation_data: DonationCreate) -> Donation:
        donation = Donation(**donation_data.model_dump())
        self.db.add(donation)
        self.db.commit()
        self.db.refresh(donation)
        return donation

    def get_by_id(self, donation_id: UUID) -> Donation | None:
        return self.db.query(Donation).filter(Donation.id == donation_id).first()

    def get_all(self) -> list[Donation]:
        return self.db.query(Donation).all()

    def update(self, donation: Donation, donation_data: DonationUpdate) -> Donation:
        for field, value in donation_data.model_dump(exclude_unset=True).items():
            setattr(donation, field, value)
        self.db.commit()
        self.db.refresh(donation)
        return donation

    def delete(self, donation: Donation) -> None:
        self.db.delete(donation)
        self.db.commit()
