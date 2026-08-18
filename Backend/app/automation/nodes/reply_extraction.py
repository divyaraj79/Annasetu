from app.automation.state import AutomationState


def reply_extraction_node(
    state: AutomationState,
) -> AutomationState:
    """
    Extract NGO reply using Groq.
    """

    groq = state["services"]["groq"]

    state["reply_data"] = groq.extract_ngo_reply(
        state["email"]["body"]
    )

    return state