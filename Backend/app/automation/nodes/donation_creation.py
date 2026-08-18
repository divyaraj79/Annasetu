from app.automation.state import AutomationState
from app.automation.exceptions import (
    AutomationValidationError,
)


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

    # created = automation.create_donation(
    #     restaurant=state["restaurant"],
    #     donation_data=state["donation_data"],
    #     donation_items=state["donation_items"],
    # )

    # state["donation"] = created

    # return state

    try:
        created = automation.create_donation(
            restaurant=state["restaurant"],
            donation_data=state["donation_data"],
            donation_items=state["donation_items"],
        )

    except ValueError as exc:
        raise AutomationValidationError(
            str(exc)
        ) from exc

    state["donation"] = created

    return state