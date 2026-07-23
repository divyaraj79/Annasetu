from app.automation.state import AutomationState

from app.automation.email_templates import (
    DONATION_EMAIL,
    NGO_NOTIFICATION,
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
    )

    if subject == DONATION_EMAIL:

        state["email_type"] = "restaurant"

    elif subject.startswith(
        f"Re: {NGO_NOTIFICATION}"
    ):

        state["email_type"] = "ngo"

    else:

        state["email_type"] = "ignore"

    return state