from app.automation.email_service import EmailService
from app.automation.groq_client import GroqClient
from app.automation.automation_service import AutomationService

from app.schemas.donation import DonationCreate

from sqlalchemy.orm import Session

from uuid import UUID

from app.services.restaurant_service import RestaurantService
from app.services.match_service import MatchService
from email.utils import parseaddr


class Workflow:

    def __init__(
        self,
        db: Session,
    ):

        self.email_service = EmailService()
        self.groq_client = GroqClient()
        self.automation_service = AutomationService(
            db,
        )
        self.restaurant_service = RestaurantService(db)
        self.match_service = MatchService(db)

    # --------------------------------------------------
    # Restaurant Workflow
    # --------------------------------------------------

    def process_restaurant_email(
        self,
        email: dict,
    ) -> None:
        """
        Process a restaurant donation email.
        """

        from_email = parseaddr(
            email["from"]
        )[1]

        restaurant = self.restaurant_service.get_by_email(
            from_email,
        )

        if restaurant is None:
            raise ValueError(
                "Unknown restaurant email."
            )

        donation_data = self.groq_client.extract_donation(
            email["body"],
        )

        donation = DonationCreate(
            restaurant_id=restaurant.id,
            **donation_data,
        )

        self.automation_service.create_donation(
            donation,
        )

        self.email_service.mark_email_as_read(
            email["id"],
        )

    # --------------------------------------------------
    # NGO Workflow
    # --------------------------------------------------

    def process_ngo_reply(
        self,
        email: dict,
    ) -> None:
        """
        Process an NGO reply.
        """

        reply = self.groq_client.extract_ngo_reply(
            email["body"],
        )

        match = self.match_service.get_by_id(
            UUID(reply["match_id"])
        )

        if match is None:
            raise ValueError(
                "Match not found."
            )
        
        sender = parseaddr(
            email["from"]
        )[1]

        if sender != match.ngo.user.email:
            raise ValueError(
                "Reply does not belong to the assigned NGO."
            )

        if reply["intent"] == "accept":

            self.automation_service.accept_match(
                match,
            )

        else:

            self.automation_service.decline_match(
                match,
                reply["reason"],
            )

        self.email_service.mark_email_as_read(
            email["id"],
        )