from app.automation.state import AutomationState


def donation_extraction_node(
    state: AutomationState,
) -> AutomationState:
    """
    Extract structured donation
    information using Groq.
    """

    groq = state["services"]["groq"]

    extracted = groq.extract_donation(
        state["email"]["body"]
    )

    state["donation_items"] = extracted.pop(
        "items",
        [],
    )

    state["donation_data"] = extracted

    return state