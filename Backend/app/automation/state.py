from typing import Any, TypedDict

from app.models.restaurant import Restaurant
from app.models.ngo import NGO
from app.models.donation import Donation
from app.models.match import Match
from app.models.need import Need

class AutomationState(TypedDict, total=False):
    """
    Shared state passed between
    LangGraph nodes.
    """

    # Incoming email
    email: dict

    # Router decision
    email_type: str

    # Database objects
    restaurant: Restaurant
    ngo: NGO
    donation: Donation
    need: Need
    match: Match

    # AI extraction
    donation_data: dict
    donation_items: list[dict]
    need_data: dict
    reply_data: dict

    # Shared services
    services: dict[str, Any]