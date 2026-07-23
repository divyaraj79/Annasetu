from app.automation.state import AutomationState


def reply_node(
    state: AutomationState,
) -> AutomationState:
    """
    Process NGO reply (accept / decline).
    """

    automation = state["services"]["automation"]

    reply = state["reply"]
    match = state["match"]

    intent = reply["intent"].lower()

    if intent == "accept":

        automation.accept_match(
            match,
        )

    elif intent == "decline":

        automation.decline_match(
            match,
            reply.get("reason"),
        )

    else:

        raise ValueError(
            f"Unknown reply intent: {intent}"
        )

    state["services"]["email"].mark_email_as_read(
        state["email"]["id"],
    )

    return state