from uuid import UUID

from app.automation.state import AutomationState
from app.automation.exceptions import AutomationValidationError


def match_lookup_node(
    state: AutomationState,
) -> AutomationState:
    """
    Fetch the match referenced
    by the NGO email.
    """

    match_service = (
        state["services"]["match"]
    )

    match = match_service.get_by_id(
        UUID(
            state["reply_data"]["reference_id"]
        )
    )

    if match is None:
        raise AutomationValidationError(
            "Invalid or unknown Reference ID."
        )

    state["match"] = match

    return state