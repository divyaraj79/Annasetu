from app.automation.state import AutomationState

from app.automation.exceptions import (
    AutomationValidationError,
)


def need_creation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Create an NGO need.
    """

    automation = (
        state["services"]["automation"]
    )

    try:

        need = automation.create_need(
            ngo=state["ngo"],
            need_data=state["need_data"],
        )

    except ValueError as exc:

        raise AutomationValidationError(
            str(exc)
        ) from exc

    state["need"] = need

    return state