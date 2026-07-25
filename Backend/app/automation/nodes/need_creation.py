from app.automation.state import AutomationState


def need_creation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Create an NGO need.
    """

    automation = (
        state["services"]["automation"]
    )

    need = automation.create_need(
        ngo=state["ngo"],
        need_data=state["need_data"],
    )

    state["need"] = need

    return state