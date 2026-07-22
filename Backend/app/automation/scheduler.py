from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.donation import Donation

from app.enums.status import (
    MatchStatus,
    DonationStatus,
)

from app.services.lifecycle_service import LifecycleService
from app.automation.workflow import Workflow


MATCH_RESPONSE_TIMEOUT = timedelta(minutes=30)


class Scheduler:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.lifecycle_service = LifecycleService(db)

        self.workflow = Workflow(db)

    def run_once(self) -> None:
        """
        Execute one scheduler cycle.
        """

        try:

            self._check_match_timeouts()

            self._check_donation_expiry()

            self._process_restaurant_emails()

            self._process_ngo_replies()

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

    def _check_match_timeouts(self) -> None:
        """
        Process all notified matches whose
        response timeout has elapsed.
        """

        now = datetime.now(timezone.utc)

        matches = (
            self.db.query(Match)
            .filter(
                Match.status == MatchStatus.NOTIFIED,
                Match.is_deleted == False,
            )
            .all()
        )

        for match in matches:

            if (
                match.notified_at
                and now - match.notified_at >= MATCH_RESPONSE_TIMEOUT
            ):

                self.lifecycle_service.process_match_timeout(
                    match
                )

    def _check_donation_expiry(self) -> None:
        """
        Process all donations whose
        expiry time has passed.
        """

        now = datetime.now(timezone.utc)

        donations = (
            self.db.query(Donation)
            .filter(
                Donation.is_deleted == False,
                Donation.status != DonationStatus.EXPIRED,
            )
            .all()
        )

        for donation in donations:

            if donation.expiry_time <= now:

                self.lifecycle_service.process_donation_expiry(
                    donation
                )

    def _process_restaurant_emails(
        self,
    ) -> None:
        """
        Process unread restaurant emails.
        """

        emails = (
            self.workflow.email_service
            .fetch_restaurant_emails()
        )

        for email in emails:

            self.workflow.process_restaurant_email(
                email
            )

    def _process_ngo_replies(
        self,
    ) -> None:
        """
        Process unread NGO replies.
        """

        emails = (
            self.workflow.email_service
            .fetch_ngo_replies()
        )

        for email in emails:
            self.workflow.process_ngo_reply(
                email,
            )