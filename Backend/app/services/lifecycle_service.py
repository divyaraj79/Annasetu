from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.match import Match

from app.enums.status import MatchStatus, DonationStatus

from app.services.match_service import MatchService
from app.services.donation_service import DonationService

from app.automation.email_service import EmailService

from datetime import datetime, timezone

class LifecycleService:

    def __init__(self, db: Session):
        self.db = db

        self.match_service = MatchService(db)
        self.donation_service = DonationService(db)

        self.email_service = EmailService()

    def _notify_next_match(
        self,
        donation: Donation,
    ) -> Match | None:
        next_match = (
            self.db.query(Match)
            .filter(
                Match.donation_id == donation.id,
                Match.status == MatchStatus.PENDING,
                Match.is_deleted == False,
            )
            .order_by(Match.attempt_number)
            .first()
        )


        # TODO:
        # Handle case where no eligible
        # matches remain before donation expiry.

        if not next_match:

            self.donation_service.mark_as_unmatched(
                donation,
            )

            self.email_service.send_donation_unmatched(
                donation.restaurant,
            )

            return None
        
        if donation.expiry_time <= datetime.now(
            timezone.utc,
        ):

            self.process_donation_expiry(
                donation,
            )

            return None

        self.match_service.mark_as_notified(
            next_match
        )

        self.email_service.send_match_notification(
            donation,
            next_match,
        )

        return next_match

    def process_match_accept(
        self,
        match: Match,
    ) -> Match:

        match = self.match_service.mark_as_accepted(
            match,
        )

        match.donation.status = DonationStatus.ACCEPTED

        self.email_service.send_donation_accepted(
            match.donation.restaurant,
            match.ngo,
        )

        return match
    
    def process_match_decline(
        self,
        match: Match,
        reason: str,
    ) -> Match | None:
        self.match_service.mark_as_declined(
            match,
            reason,
        )

        return self._notify_next_match(
            match.donation
        )
    
    def process_match_timeout(
        self,
        match: Match,
    ) -> Match | None:

        if match.is_deleted:
            raise ValueError(
                "Match has already been deleted."
            )

        if match.status != MatchStatus.NOTIFIED:
            raise ValueError(
                "Only notified matches can timeout."
            )

        self.match_service.mark_as_declined(
            match,
            "No response received within the allowed time.",
        )

        self.email_service.send_match_timeout(
            match.ngo,
        )

        return self._notify_next_match(
            match.donation,
        )
    
    def process_donation_expiry(
        self,
        donation: Donation,
    ) -> Donation:

        if donation.is_deleted:
            raise ValueError(
                "Donation has already been deleted."
            )

        if donation.status == DonationStatus.EXPIRED:
            raise ValueError(
                "Donation is already expired."
            )

        donation.status = DonationStatus.EXPIRED

        self.donation_service.delete(
            donation,
        )

        return donation