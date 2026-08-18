from app.automation.state import AutomationState

from app.automation.exceptions import (
    AutomationValidationError,
)

from email.utils import parseaddr


def ngo_validation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Validate that the sender belongs
    to an approved NGO.
    """

    ngo_service = (
        state["services"]["ngo"]
    )

    sender = parseaddr(
        state["email"]["from"]
    )[1]

    ngo = ngo_service.get_by_email(
        sender,
    )

    if ngo is None:
        raise AutomationValidationError(
            "No approved NGO is registered with this email address."
        )

    state["ngo"] = ngo

    return state