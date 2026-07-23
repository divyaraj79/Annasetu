from app.automation.state import AutomationState


def donation_extraction_node(
    state: AutomationState,
) -> AutomationState:
    """
    Extract structured donation
    information using Groq.
    """

    groq = state["services"]["groq"]

    state["donation_data"] = (
        groq.extract_donation(
            state["email"]["body"]
        )
    )

    return state