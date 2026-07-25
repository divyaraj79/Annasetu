from app.automation.state import AutomationState


def need_matching_node(
    state: AutomationState,
) -> AutomationState:
    """
    Trigger matching after a new
    NGO need is created.
    """

    automation = (
        state["services"]["automation"]
    )

    automation.process_new_need(
        state["need"],
    )

    return state