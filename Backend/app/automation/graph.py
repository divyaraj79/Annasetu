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


def route_email(
    state: AutomationState,
) -> str:

    return state["email_type"]


builder = StateGraph(
    AutomationState,
)

builder.add_node(
    "router",
    router_node,
)

builder.set_entry_point(
    "router",
)

builder.add_conditional_edges(
    "router",
    route_email,
    {
        "restaurant": END,
        "ngo": END,
        "ignore": END,
    },
)

automation_graph = builder.compile()