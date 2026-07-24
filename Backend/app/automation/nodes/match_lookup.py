from uuid import UUID

from app.automation.state import AutomationState


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
        raise ValueError(
            "Match not found."
        )

    state["match"] = match

    return state