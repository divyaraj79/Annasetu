from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.match import Match

from app.enums.status import MatchStatus, DonationStatus

from app.services.match_service import MatchService
# from app.services.donation_service import DonationService

from app.automation.email_service import EmailService

from datetime import datetime, timezone

MATCH_COMPLETED_REASON = (
    "Donation completed by another NGO."
)

class LifecycleService:

    def __init__(self, db: Session):
        self.db = db

        self.match_service = MatchService(db)
        # self.donation_service = DonationService(db)

        self.email_service = EmailService()

    def notify_next_match(
        self,
        donation: Donation,
    ) -> Match | None:
        existing_notification = (
            self.db.query(Match)
            .filter(
                Match.donation_id == donation.id,
                Match.status == MatchStatus.NOTIFIED,
                Match.is_deleted == False,
            )
            .first()
        )

        if existing_notification:
            return existing_notification
        
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

            if donation.status == DonationStatus.MATCHING:

                donation.status = DonationStatus.UNMATCHED

                print(
                    f"UNMATCHED EMAIL → "
                    f"restaurant={donation.restaurant.restaurant_name}, "
                    f"recipient={donation.restaurant.user.email}"
                )

                response = self.email_service.send_donation_unmatched(
                    donation.restaurant,
                )

                print(
                    f"UNMATCHED EMAIL GMAIL RESPONSE → "
                    f"{response.get('id')}"
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

    def process_match_completed(
        self,
        match: Match,
    ) -> Match:

        match = self.match_service.mark_as_completed(
            match,
        )

        donation = match.donation

        donation.status = (
            DonationStatus.COMPLETED
        )

        # TODO (v2):
        # Match currently stores only donation_id and ngo_id.
        # It does not store the specific need_id that generated
        # this match, so we cannot determine which NGO Need has
        # been fulfilled.
        #
        # When need_id is added to Match, mark that Need as
        # COMPLETED (or decrement its remaining quantity for
        # partial fulfillment) here.

        for item in donation.donation_items:

            item.status = (
                DonationStatus.COMPLETED
            )

        remaining_matches = (
            self.db.query(Match)
            .filter(
                Match.donation_id == donation.id,
                Match.id != match.id,
                Match.is_deleted == False,
                Match.status.in_(
                    [
                        MatchStatus.PENDING,
                        MatchStatus.NOTIFIED,
                    ]
                ),
            )
            .all()
        )

        for remaining in remaining_matches:

            remaining.status = (
                MatchStatus.DECLINED
            )

            remaining.match_reason = (
                MATCH_COMPLETED_REASON
            )

            remaining.is_deleted = True

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

        return self.notify_next_match(
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

        return self.notify_next_match(
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

        # self.donation_service.delete(
        #     donation,
        # )

        donation.is_deleted = True

        for item in donation.donation_items:
            item.is_deleted = True

        for match in donation.matches:
            match.is_deleted = True

        return donation