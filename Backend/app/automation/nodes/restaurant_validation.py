from email.utils import parseaddr

from app.automation.state import AutomationState
from app.automation.exceptions import (
    AutomationValidationError,
)

def restaurant_validation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Validate that the sender
    belongs to an approved restaurant.
    """

    restaurant_service = (
        state["services"]["restaurant"]
    )

    sender = parseaddr(
        state["email"]["from"]
    )[1]

    restaurant = (
        restaurant_service.get_by_email(
            sender,
        )
    )

    if restaurant is None:
        raise AutomationValidationError(
            "Unknown restaurant email."
        )

    state["restaurant"] = restaurant

    return state