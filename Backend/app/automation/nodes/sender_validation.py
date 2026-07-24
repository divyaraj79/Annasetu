from email.utils import parseaddr

from app.automation.state import AutomationState


def sender_validation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Ensure the sender belongs
    to the NGO assigned
    to this match.
    """

    sender = parseaddr(
        state["email"]["from"]
    )[1]

    if sender != state["match"].ngo.user.email:
        raise ValueError(
            "Reply does not belong to the assigned NGO."
        )

    return state