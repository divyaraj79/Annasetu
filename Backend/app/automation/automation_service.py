from sqlalchemy.orm import Session

from app.models.match import Match

from app.schemas.donation import DonationCreate

from app.services.donation_service import DonationService
from app.services.matching_service import MatchingService
from app.services.lifecycle_service import LifecycleService


class AutomationService:

    def __init__(self, db: Session):
        self.db = db

        self.donation_service = DonationService(db)
        self.matching_service = MatchingService(db)
        self.lifecycle_service = LifecycleService(db)

    def create_donation(
        self,
        donation_data: DonationCreate,
    ):
        """
        Create a donation from structured
        automation input.

        Flow:

        DonationService
                ↓
        MatchingService
        """

        donation = self.donation_service.create(
            donation_data
        )

        self.matching_service.create_matches(
            donation
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