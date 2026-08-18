from sqlalchemy.orm import Session

from app.models.match import Match

from app.schemas.donation import DonationCreate

from app.services.donation_service import DonationService
# from app.services.matching_service import MatchingService
from app.services.lifecycle_service import LifecycleService

from app.schemas.donation_item import DonationItemCreate
from app.services.donation_item_service import DonationItemService
from app.enums.quantity_unit import QuantityUnit
from app.models.restaurant import Restaurant

from app.automation.exceptions import (
    AutomationValidationError,
)

from app.schemas.need import NeedCreate
from app.services.need_service import NeedService
# from app.enums.urgency import Urgency
from app.models.ngo import NGO
# from app.models.donation import Donation

# from app.models.need import Need
# from app.enums.status import DonationStatus


class AutomationService:

    def __init__(self, db: Session):
        self.db = db

        self.donation_service = DonationService(db)
        self.need_service = NeedService(db)
        self.donation_item_service = DonationItemService(db)
        # self.matching_service = MatchingService(db)
        self.lifecycle_service = LifecycleService(db)

    def create_donation(
        self,
        restaurant: Restaurant,
        donation_data: dict,
        donation_items: list[dict],
    ):
        """
        Create a donation together with all
        donation items.
        """

        """
        Must be executed inside a database transaction.

        Any exception while creating donation items or matches
        should roll back the entire donation creation.
        """

        if not donation_items:
            raise AutomationValidationError(
                "At least one donation item must be provided."
            )

        required_fields = {
            "title": "Donation Title",
            "food_category": "Food Category",
            "is_vegetarian": "Vegetarian Information",
            "cooked_at": "Cooked Time",
            "expiry_time": "Expiry Time",
            "pickup_address": "Pickup Address",
        }
                
        for field, display_name in required_fields.items():
            if donation_data.get(field) in (None, ""):
                
                raise AutomationValidationError(
                    f"{display_name} is missing."
                )
        
        donation_payload = donation_data.copy()

        donation_payload["food_name"] = donation_payload.pop(
            "title"
        )

        try : 
            donation_schema = DonationCreate(
                restaurant_id=restaurant.id,
                **donation_payload,
                # Aggregate donation summary.
                # Quantity represents the number of donation items,
                # not their combined physical quantity.
                quantity=len(donation_items),
                quantity_unit=QuantityUnit.PIECE,
            )
        except Exception:
            raise AutomationValidationError(
                "The donation details could not be understood. Please review the email and send it again."
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

        # self.matching_service.create_matches(
        #     donation,
        # )

        # self.lifecycle_service.notify_next_match(
        #     donation,
        # )

        return donation

    def create_need(
        self,
        ngo: NGO,
        need_data: dict,
    ):
        """
        Create an NGO need.
        """

        required_fields = {
            "preferred_category": "Food Category",
            "vegetarian_only": "Vegetarian Preference",
            "quantity_required": "Quantity",
            "quantity_unit": "Quantity Unit",
            "urgency": "Urgency",
        }

        for field, display_name in required_fields.items():

            if need_data.get(field) in (None, ""):

                raise AutomationValidationError(
                    f"{display_name} is missing."
                )

        try:

            need_schema = NeedCreate(
                ngo_id=ngo.id,
                **need_data,
            )

        except Exception:

            raise AutomationValidationError(
                "The food need could not be understood. Please review the email and send it again."
            )

        need = self.need_service.create(
            need_schema,
        )

        return need

    # def process_new_need(
    #     self,
    #     need: Need,
    # ):
    #     """
    #     Re-run matching for all active donations
    #     after a new NGO need is created.
    #     """

    #     donations = (
    #         self.db.query(Donation)
    #         .filter(
    #             Donation.is_deleted == False,
    #             Donation.status.in_(
    #                 [
    #                     DonationStatus.MATCHING,
    #                     DonationStatus.UNMATCHED,
    #                 ]
    #             )
    #         )
    #         .all()
    #     )

    #     for donation in donations:

    #         self.matching_service.create_matches(
    #             donation,
    #         )

    #         self.lifecycle_service.notify_next_match(
    #             donation,
    #         )

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