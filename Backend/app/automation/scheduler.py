from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.match import Match
from app.models.donation import Donation

from app.enums.status import (
    MatchStatus,
    DonationStatus,
)

from app.services.lifecycle_service import LifecycleService
from app.automation.executor import GraphExecutor
from app.automation.email_service import EmailService

from app.automation.exceptions import (
    AutomationValidationError,
)

from app.automation.email_templates import DONATION_EMAIL
from email.utils import parseaddr


MATCH_RESPONSE_TIMEOUT = timedelta(minutes=30)


class Scheduler:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.lifecycle_service = LifecycleService(db)

        self.email_service = EmailService()
        self.executor = GraphExecutor(db)

    def run_once(self) -> None:
        """
        Execute one scheduler cycle.
        """

        try:

            self._check_match_timeouts()

            self._check_donation_expiry()

            self._process_unread_emails()

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

    def _process_unread_emails(
        self,
    ) -> None:
        """
        Process every unread email.

        LangGraph decides what type of
        email it is.
        """

        emails = (
            self.email_service
            .fetch_unread_emails()
        )

        for email in emails:
            try:
                self.executor.execute(
                    email,
                )

            except AutomationValidationError as exc:
                print(
                    f"Validation failed: {exc.message}"
                )

                # Only restaurant donation
                # validation errors receive a
                # correction email.

                subject = (
                    " ".join(email["subject"].split())
                    .lower()
                )

                if (
                    subject
                    == DONATION_EMAIL.lower()
                ):
                    try:
                        recipient = parseaddr(email["from"])[1]
                        
                        self.email_service.send_donation_validation_failed(
                            recipient=recipient,
                            reason=exc.message,
                        )

                    except Exception as send_exc:
                        print(
                            f"Failed to send correction email: {send_exc}"
                        )

                self.email_service.mark_email_as_read(
                    email["id"],
                )

            except Exception as exc:
                print(
                    f"Email processing failed: {exc}"
                )