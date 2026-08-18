from app.automation.state import AutomationState


def need_matching_node(
    state: AutomationState,
) -> AutomationState:
    """
    Matching is triggered by NeedService.create().
    This node is retained for graph compatibility.
    """

    return state