from langgraph.graph import (
    StateGraph,
    END,
)

from app.automation.state import AutomationState

from app.automation.nodes.router import router_node
from app.automation.nodes.restaurant_validation import (
    restaurant_validation_node,
)
from app.automation.nodes.donation_extraction import (
    donation_extraction_node,
)
from app.automation.nodes.donation_creation import (
    donation_creation_node,
)

# NGO nodes (abhi implement karenge)
from app.automation.nodes.validate import validate_node
from app.automation.nodes.reply import reply_node


def route_email(
    state: AutomationState,
):
    return state["email_type"]


builder = StateGraph(
    AutomationState,
)

# -------------------------
# Nodes
# -------------------------

builder.add_node(
    "router",
    router_node,
)

builder.add_node(
    "restaurant_validation",
    restaurant_validation_node,
)

builder.add_node(
    "donation_extraction",
    donation_extraction_node,
)

builder.add_node(
    "donation_creation",
    donation_creation_node,
)

builder.add_node(
    "validate",
    validate_node,
)

builder.add_node(
    "reply",
    reply_node,
)

# -------------------------
# Entry
# -------------------------

builder.set_entry_point(
    "router",
)

# -------------------------
# Router
# -------------------------

builder.add_conditional_edges(
    "router",
    route_email,
    {
        "restaurant": "restaurant_validation",
        "ngo": "validate",
        "ignore": END,
    },
)

# -------------------------
# Restaurant Flow
# -------------------------

builder.add_edge(
    "restaurant_validation",
    "donation_extraction",
)

builder.add_edge(
    "donation_extraction",
    "donation_creation",
)

builder.add_edge(
    "donation_creation",
    END,
)

# -------------------------
# NGO Flow
# -------------------------

builder.add_edge(
    "validate",
    "reply",
)

builder.add_edge(
    "reply",
    END,
)

automation_graph = builder.compile()