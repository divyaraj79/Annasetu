from app.automation.state import AutomationState


def need_extraction_node(
    state: AutomationState,
) -> AutomationState:
    """
    Extract structured need
    information from an NGO email.
    """

    groq = (
        state["services"]["groq"]
    )

    extracted = groq.extract_need(
        state["email"]["body"]
    )

    state["need_data"] = extracted

    return state