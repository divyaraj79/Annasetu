from app.automation.state import AutomationState
from app.automation.exceptions import (
    AutomationValidationError,
)


def reply_action_node(
    state: AutomationState,
) -> AutomationState:
    """
    Execute NGO action.
    """

    automation = (
        state["services"]["automation"]
    )

    reply = state["reply_data"]

    if reply["intent"] == "accept":

        automation.accept_match(
            state["match"],
        )

    elif reply["intent"] == "decline":

        automation.decline_match(
            state["match"],
            reply["reason"],
        )

    elif reply["intent"] == "completed":

        automation.complete_match(
            state["match"],
        )

    else:
        raise AutomationValidationError(
            f"Unsupported NGO intent: {reply['intent']}"
        )

    return state