from app.automation.state import AutomationState

from app.schemas.donation import DonationCreate


def donation_creation_node(
    state: AutomationState,
) -> AutomationState:
    """
    Validate extracted donation data
    and create the donation.
    """

    automation = state["services"]["automation"]

    donation = DonationCreate(
        restaurant_id=state["restaurant"].id,
        **state["donation_data"],
    )

    created = automation.create_donation(
        donation,
    )

    state["donation"] = created

    # Mark email as processed
    state["services"]["email"].mark_email_as_read(
        state["email"]["id"],
    )

    return state