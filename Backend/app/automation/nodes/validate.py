from uuid import UUID
from email.utils import parseaddr

from app.automation.state import AutomationState


def validate_node(
    state: AutomationState,
) -> AutomationState:
    """
    Validate an NGO reply before processing it.
    """

    groq = state["services"]["groq"]
    match_service = state["services"]["match"]

    # Extract structured reply from email
    reply = groq.extract_ngo_reply(
        state["email"]["body"]
    )

    # Find match
    match = match_service.get_by_id(
        UUID(reply["match_id"])
    )

    if match is None:
        raise ValueError(
            "Match not found."
        )

    # Validate sender
    sender = parseaddr(
        state["email"]["from"]
    )[1]

    if sender != match.ngo.user.email:
        raise ValueError(
            "Reply does not belong to the assigned NGO."
        )

    # Store for next node
    state["reply"] = reply
    state["match"] = match

    return state