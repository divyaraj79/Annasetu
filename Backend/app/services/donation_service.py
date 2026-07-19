from uuid import UUID
from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.restaurant import Restaurant
from app.schemas.donation import DonationCreate, DonationUpdate
from app.enums.verification_status import VerificationStatus
from app.enums.status import DonationStatus


class DonationService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, donation_data: DonationCreate) -> Donation:
        # Check if restaurant exists
        restaurant = (
            self.db.query(Restaurant)
            .filter(Restaurant.id == donation_data.restaurant_id)
            .first()
        )

        if not restaurant:
            raise ValueError("Restaurant not found.")

        # Restaurant must not be deleted
        if restaurant.is_deleted:
            raise ValueError("Restaurant is deleted.")

        # Restaurant must be approved
        if restaurant.verification_status != VerificationStatus.APPROVED:
            raise ValueError("Restaurant is not approved.")

        # Quantity validation
        if donation_data.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")

        # Expiry validation
        if donation_data.cooked_at:

            if donation_data.expiry_time <= donation_data.cooked_at:
                raise ValueError("Expiry time must be after cooked time.")

            if donation_data.expiry_time > donation_data.cooked_at + timedelta(hours=10):
                raise ValueError(
                    "Food expiry cannot exceed 10 hours after cooking."
                )

        donation = Donation(
            **donation_data.model_dump(),
            status=DonationStatus.CREATED,
        )

        # TODO:
        # Geocode pickup_address and automatically
        # populate latitude and longitude.

        # TODO:
        # Trigger LangGraph workflow after
        # successful donation creation.

        self.db.add(donation)

        self.db.flush()

        self.db.refresh(donation)

        return donation

    def get_by_id(self, donation_id: UUID) -> Donation | None:
        return self.db.query(Donation).filter(Donation.id == donation_id).first()

    def get_all(self) -> list[Donation]:
        return self.db.query(Donation).all()

    def update(
        self,
        donation: Donation,
        donation_data: DonationUpdate,
    ) -> Donation:

        # Do not allow completed donations to be modified
        if donation.status == DonationStatus.COMPLETED:
            raise ValueError("Completed donations cannot be updated.")

        update_data = donation_data.model_dump(exclude_unset=True)

        # Quantity validation
        if (
            "quantity" in update_data
            and update_data["quantity"] <= 0
        ):
            raise ValueError("Quantity must be greater than zero.")

        # Validate cooked_at and expiry_time
        cooked_at = update_data.get("cooked_at", donation.cooked_at)
        expiry_time = update_data.get("expiry_time", donation.expiry_time)

        if cooked_at is not None and expiry_time is not None:
            if expiry_time <= cooked_at:
                raise ValueError(
                    "Expiry time must be after cooked time."
                )

            if expiry_time - cooked_at > timedelta(hours=10):
                raise ValueError(
                    "Maximum food life cannot exceed 10 hours."
                )

        # TODO:
        # After authentication is implemented,
        # ensure only the donation owner
        # (or an admin) can update this donation.
        #
        # If pickup_address changes,
        # automatically geocode the address
        # and update latitude & longitude.

        for field, value in update_data.items():
            setattr(donation, field, value)

        self.db.flush()

        self.db.refresh(donation)

        return donation

    def delete(self, donation: Donation) -> None:
        self.db.delete(donation)
        self.db.flush()
