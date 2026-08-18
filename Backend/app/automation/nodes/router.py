from app.automation.state import AutomationState

from app.automation.email_templates import (
    DONATION_EMAIL,
    NGO_NOTIFICATION,
    NEED_EMAIL,
)


def router_node(
    state: AutomationState,
) -> AutomationState:
    """
    Determine what kind of email
    entered the automation system.
    """

    subject = (
        state["email"]["subject"]
        .strip()
        .lower()
    )

    if subject == DONATION_EMAIL.lower():
        state["email_type"] = "restaurant"

    elif subject == NEED_EMAIL.lower():
        state["email_type"] = "ngo_need"

    elif subject.startswith(f"re: {NGO_NOTIFICATION.lower()}"):
        state["email_type"] = "ngo_reply"

    else:
        state["email_type"] = "ignore"

    return state