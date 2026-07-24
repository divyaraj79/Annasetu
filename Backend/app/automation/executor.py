from sqlalchemy.orm import Session

from app.automation.graph import automation_graph
from app.automation.state import AutomationState

from app.automation.email_service import EmailService
from app.automation.groq_client import GroqClient
from app.automation.automation_service import AutomationService

from app.services.restaurant_service import RestaurantService
from app.services.match_service import MatchService


class GraphExecutor:
    """
    Entry point for LangGraph execution.

    Responsible only for:

    - building graph state
    - injecting services
    - invoking the graph
    """

    def __init__(
        self,
        db: Session,
    ):

        self.db = db
        self.email_service = EmailService()
        self.groq = GroqClient()
        self.automation = AutomationService(db)
        self.restaurant = RestaurantService(db)
        self.match = MatchService(db)

    def execute(
        self,
        email: dict,
    ) -> AutomationState:

        state: AutomationState = {
            "email": email,
            "services": {
                "email": self.email_service,
                "groq": self.groq,
                "automation": self.automation,
                "restaurant": self.restaurant,
                "match": self.match,
            },
        }

        return automation_graph.invoke(
            state
        )