from langgraph.graph import (
    StateGraph,
    END,
)

from app.automation.state import (
    AutomationState,
)

from app.automation.nodes.router import (
    router_node,
)

from app.automation.nodes.restaurant_validation import (
    restaurant_validation_node,
)

from app.automation.nodes.donation_extraction import (
    donation_extraction_node,
)

from app.automation.nodes.donation_creation import (
    donation_creation_node,
)

from app.automation.nodes.mark_read import (
    mark_read_node,
)

from app.automation.nodes.reply_extraction import (
    reply_extraction_node,
)

from app.automation.nodes.match_lookup import (
    match_lookup_node,
)

from app.automation.nodes.sender_validation import (
    sender_validation_node,
)

from app.automation.nodes.reply_action import (
    reply_action_node,
)


def route_email(
    state: AutomationState,
) -> str:

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
    "reply_extraction",
    reply_extraction_node,
)

builder.add_node(
    "match_lookup",
    match_lookup_node,
)

builder.add_node(
    "sender_validation",
    sender_validation_node,
)

builder.add_node(
    "reply_action",
    reply_action_node,
)

builder.add_node(
    "mark_read",
    mark_read_node,
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
        "ngo": "reply_extraction",
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
    "mark_read",
)

builder.add_edge(
    "reply_extraction",
    "match_lookup",
)

builder.add_edge(
    "match_lookup",
    "sender_validation",
)

builder.add_edge(
    "sender_validation",
    "reply_action",
)

builder.add_edge(
    "reply_action",
    "mark_read",
)

builder.add_edge(
    "mark_read",
    END,
)

automation_graph = builder.compile()