from app.automation.email_client import EmailClient
from app.automation.email_templates import (
    DONATION_EMAIL,
    NGO_NOTIFICATION,
    RESTAURANT_REGISTRATION_APPROVED,
    DONATION_ACCEPTED,
    DONATION_UNMATCHED,
    MATCH_TIMEOUT,
    NGO_REGISTRATION_APPROVED,
    ngo_registration_approved_template,
    registration_approved_template,
    ngo_notification_template,
    donation_accepted_template,
    donation_unmatched_template,
    match_timeout_template,
)

from app.models.donation import Donation
from app.models.match import Match
from app.models.ngo import NGO
from app.models.restaurant import Restaurant


class EmailService:

    def __init__(self):

        self.email_client = EmailClient()

    # --------------------------------------------------
    # Incoming Emails
    # --------------------------------------------------

    def fetch_restaurant_emails(
        self,
    ) -> list[dict]:
        """
        Fetch unread restaurant
        donation emails.
        """

        emails = (
            self.email_client.fetch_unread_messages()
        )

        return [
            email
            for email in emails
            if email["subject"].strip() == DONATION_EMAIL
        ]

    def fetch_ngo_replies(
        self,
    ) -> list[dict]:
        """
        Fetch unread NGO reply emails.
        """

        emails = (
            self.email_client.fetch_unread_messages()
        )

        return [
            email
            for email in emails
            if email["subject"].strip().startswith(
                f"Re: {NGO_NOTIFICATION}"
            )
        ]

    # --------------------------------------------------
    # Outgoing Emails
    # --------------------------------------------------

    def send_restaurant_registration_approval(
        self,
        restaurant: Restaurant,
    ) -> dict:

        return self.email_client.send_email(
            recipient=restaurant.user.email,
            subject=RESTAURANT_REGISTRATION_APPROVED,
            body=registration_approved_template(),
        )
    
    def send_ngo_registration_approval(
        self,
        ngo: NGO,
    ) -> dict:

        return self.email_client.send_email(
            recipient=ngo.user.email,
            subject=NGO_REGISTRATION_APPROVED,
            body=ngo_registration_approved_template(),
        )

    def send_match_notification(
        self,
        donation: Donation,
        match: Match,
    ) -> dict:

        return self.email_client.send_email(
            recipient=match.ngo.user.email,
            subject=NGO_NOTIFICATION,
            body=ngo_notification_template(
                donation,
                match,
            ),
        )

    def send_donation_accepted(
        self,
        restaurant: Restaurant,
        ngo: NGO,
    ) -> dict:

        return self.email_client.send_email(
            recipient=restaurant.user.email,
            subject=DONATION_ACCEPTED,
            body=donation_accepted_template(
                ngo,
            ),
        )

    def send_donation_unmatched(
        self,
        restaurant: Restaurant,
    ) -> dict:

        return self.email_client.send_email(
            recipient=restaurant.user.email,
            subject=DONATION_UNMATCHED,
            body=donation_unmatched_template(),
        )

    def send_match_timeout(
        self,
        ngo: NGO,
    ) -> dict:

        return self.email_client.send_email(
            recipient=ngo.user.email,
            subject=MATCH_TIMEOUT,
            body=match_timeout_template(),
        )
    
    def mark_email_as_read(
        self,
        message_id: str,
    ) -> None:

        self.email_client.mark_as_read(
            message_id
        )

    def fetch_unread_emails(
        self,
    ) -> list[dict]:
        """
        Fetch every unread email.

        LangGraph will determine
        what type of email it is.
        """

        return (
            self.email_client.fetch_unread_messages()
        )