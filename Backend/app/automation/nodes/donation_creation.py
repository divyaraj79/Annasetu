from app.automation.state import AutomationState


def donation_creation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Create donation and donation items
    from extracted AI data.
    """

    automation = (
        state["services"]["automation"]
    )

    created = automation.create_donation(
        restaurant=state["restaurant"],
        donation_data=state["donation_data"],
        donation_items=state["donation_items"],
    )

    state["donation"] = created

    return state