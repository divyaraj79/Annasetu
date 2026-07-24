from app.automation.state import AutomationState


def mark_read_node(
    state: AutomationState,
) -> AutomationState:
    """
    Mark the processed email as read.
    """

    email_service = (
        state["services"]["email"]
    )

    email_service.mark_email_as_read(
        state["email"]["id"]
    )

    return state