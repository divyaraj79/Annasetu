from sqlalchemy.orm import Session

from app.automation.graph import automation_graph
from app.automation.email_service import EmailService
from app.automation.groq_client import GroqClient
from app.automation.automation_service import AutomationService

from app.services.restaurant_service import RestaurantService
from app.services.match_service import MatchService


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

        self.restaurant_service = RestaurantService(
            db,
        )

        self.match_service = MatchService(
            db,
        )

    def process_email(
        self,
        email: dict,
    ) -> None:
        """
        Process a single unread email.

        LangGraph router determines whether
        it is:
        - Restaurant donation
        - NGO reply
        - Ignore
        """

        state = {
            "email": email,
            "services": {
                "groq": self.groq_client,
                "automation": self.automation_service,
                "restaurant": self.restaurant_service,
                "match": self.match_service,
                "email": self.email_service,
            },
        }

        automation_graph.invoke(state)