from sqlalchemy.orm import Session

from app.models.match import Match

from app.schemas.donation import DonationCreate

from app.services.donation_service import DonationService
from app.services.matching_service import MatchingService
from app.services.lifecycle_service import LifecycleService

from app.schemas.donation_item import DonationItemCreate
from app.services.donation_item_service import DonationItemService
from app.enums.quantity_unit import QuantityUnit
from app.models.restaurant import Restaurant


class AutomationService:

    def __init__(self, db: Session):
        self.db = db

        self.donation_service = DonationService(db)
        self.donation_item_service = DonationItemService(db)
        self.matching_service = MatchingService(db)
        self.lifecycle_service = LifecycleService(db)

    def create_donation(
        self,
        restaurant: Restaurant,
        donation_data: dict,
        donation_items: list[dict],
    ):
        """
        Create a donation together with all
        donation items, then trigger matching.
        """

        """
        Must be executed inside a database transaction.

        Any exception while creating donation items or matches
        should roll back the entire donation creation.
        """

        if not donation_items:
            raise ValueError(
                "Donation must contain at least one donation item."
            )
        
        donation_payload = donation_data.copy()

        donation_payload["food_name"] = donation_payload.pop(
            "title"
        )

        donation_schema = DonationCreate(
            restaurant_id=restaurant.id,
            **donation_payload,
            # Aggregate donation summary.
            # Quantity represents the number of donation items,
            # not their combined physical quantity.
            quantity=len(donation_items),
            quantity_unit=QuantityUnit.PIECE,
        )

        donation = self.donation_service.create(
            donation_schema
        )

        for item in donation_items:

            self.donation_item_service.create(
                DonationItemCreate(
                    donation_id=donation.id,
                    **item,
                )
            )

        self.matching_service.create_matches(
            donation,
        )

        return donation

    def accept_match(
        self,
        match: Match,
    ):
        """
        Process an NGO acceptance received
        through automation.
        """

        return self.lifecycle_service.process_match_accept(
            match
        )

    def complete_match(
        self,
        match: Match,
    ):
        """
        Process donation completion received
        through automation.
        """

        return self.lifecycle_service.process_match_completed(
            match,
        )

    def decline_match(
        self,
        match: Match,
        reason: str,
    ):
        """
        Process an NGO decline received
        through automation.
        """

        return self.lifecycle_service.process_match_decline(
            match,
            reason,
        )