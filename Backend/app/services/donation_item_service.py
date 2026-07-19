from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.donation import Donation
from app.models.donation_item import DonationItem
from app.schemas.donation_item import DonationItemCreate, DonationItemUpdate
from app.enums.status import DonationStatus


class DonationItemService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donation_item_data: DonationItemCreate) -> DonationItem:
        # Check Donation exists
        donation = (
            self.db.query(Donation)
            .filter(Donation.id == donation_item_data.donation_id)
            .first()
        )

        if not donation:
            raise ValueError("Donation not found.")

        # Donation must not be deleted
        if donation.is_deleted:
            raise ValueError("Donation is deleted.")

        # Donation should not be completed
        if donation.status == DonationStatus.COMPLETED:
            raise ValueError("Completed donations cannot be updated.")

        # Donation should not be cancelled
        if donation.status == DonationStatus.CANCELLED:
            raise ValueError("Cancelled donations cannot be updated.")

        # Donation should not be expired
        if donation.status == DonationStatus.EXPIRED:
            raise ValueError("Expired donations cannot be updated.")

        # Quantity validation
        if donation_item_data.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        # Food name empty space removal
        food_name = donation_item_data.food_name.strip()

        if not food_name:
            raise ValueError("Food name cannot be empty.")

        donation_item_data.food_name = food_name
        
        # Prevent duplicate food items (case-insensitive)
        existing_item = (
            self.db.query(DonationItem)
            .filter(
                DonationItem.donation_id == donation_item_data.donation_id,
                func.lower(DonationItem.food_name)
                == donation_item_data.food_name.lower(),
            )
            .first()
        )

        if existing_item:
            raise ValueError(
                f'"{donation_item_data.food_name}" already exists for this donation.'
            )

        donation_item = DonationItem(
            **donation_item_data.model_dump()
        )

        self.db.add(donation_item)

        self.db.commit()

        self.db.refresh(donation_item)

        return donation_item

    def get_by_id(self, donation_item_id: UUID) -> DonationItem | None:
        return (
            self.db.query(DonationItem)
            .filter(DonationItem.id == donation_item_id)
            .first()
        )

    def get_all(self) -> list[DonationItem]:
        return self.db.query(DonationItem).all()

    def update(
        self,
        donation_item: DonationItem,
        donation_item_data: DonationItemUpdate,
    ) -> DonationItem:

        # Check Donation exists
        donation = (
            self.db.query(Donation)
            .filter(Donation.id == donation_item.donation_id)
            .first()
        )

        if not donation:
            raise ValueError("Donation not found.")

        # Completed donations cannot be modified        
        if donation.is_deleted:
            raise ValueError("Donation is deleted.")

        if donation.status == DonationStatus.COMPLETED:
            raise ValueError(
                "Completed donations cannot be updated."
            )

        if donation.status == DonationStatus.CANCELLED:
            raise ValueError(
                "Cancelled donations cannot be updated."
            )

        if donation.status == DonationStatus.EXPIRED:
            raise ValueError(
                "Expired donations cannot be updated."
            )

        update_data = donation_item_data.model_dump(exclude_unset=True)

        if "food_name" in update_data:
            food_name = update_data["food_name"].strip()

            if not food_name:
                raise ValueError("Food name cannot be empty.")

            existing_item = (
                self.db.query(DonationItem)
                .filter(
                    DonationItem.donation_id == donation_item.donation_id,
                    func.lower(DonationItem.food_name) == food_name.lower(),
                    DonationItem.id != donation_item.id,
                )
                .first()
            )

            if existing_item:
                raise ValueError(
                    f'"{food_name}" already exists for this donation.'
                )

            update_data["food_name"] = food_name

        # Quantity validation
        if (
            "quantity" in update_data
            and update_data["quantity"] <= 0
        ):
            raise ValueError("Quantity must be greater than zero.")

        for field, value in update_data.items():
            setattr(donation_item, field, value)

        self.db.commit()

        self.db.refresh(donation_item)

        return donation_item

    def delete(self, donation_item: DonationItem) -> None:
        self.db.delete(donation_item)
        self.db.commit()
