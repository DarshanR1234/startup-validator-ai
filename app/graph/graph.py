import sqlite3
from pathlib import Path

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from app.graph.state import StartupState

from app.graph.nodes import (
    idea_node,
    invalid_idea_node,
    market_node,
    competitor_node,
    persona_node,
    swot_node,
    pricing_node,
    mvp_node,
    evaluation_node,
    scoring_node,
)

from app.agents.idea_quality import is_idea_valid


BASE_DIR = Path(__file__).resolve().parents[2]

CHECKPOINT_DB = (
    BASE_DIR
    / "data"
    / "langgraph_checkpoints.db"
)


def idea_quality_node(
    state: StartupState,
):
    idea_analysis = state.get(
        "idea_analysis",
        {},
    )

    # DEBUG: inspect exactly what IdeaAnalysis produced
    print(
        f"[IDEA ANALYSIS] {idea_analysis}"
    )

    valid, reason = is_idea_valid(
        idea_analysis
    )

    print(
        f"[IDEA QUALITY] valid={valid}"
    )

    if not valid:
        print(
            f"[IDEA QUALITY] rejected: {reason}"
        )

    return {
        "idea_valid": valid,
        "idea_quality_message": reason,
    }


def route_after_idea_quality(
    state: StartupState,
):
    if state.get("idea_valid", False):
        return "market"

    return "invalid"


def build_startup_validation_graph():

    graph = StateGraph(StartupState)

    # --------------------------------------------------
    # Nodes
    # --------------------------------------------------

    graph.add_node(
        "idea",
        idea_node,
    )

    graph.add_node(
        "idea_quality",
        idea_quality_node,
    )

    graph.add_node(
        "invalid_idea",
        invalid_idea_node,
    )

    graph.add_node(
        "market",
        market_node,
    )

    graph.add_node(
        "competitor",
        competitor_node,
    )

    graph.add_node(
        "persona",
        persona_node,
    )

    graph.add_node(
        "swot",
        swot_node,
    )

    graph.add_node(
        "pricing",
        pricing_node,
    )

    graph.add_node(
        "mvp",
        mvp_node,
    )

    graph.add_node(
        "evaluation",
        evaluation_node,
    )

    graph.add_node(
        "scoring",
        scoring_node,
    )

    # --------------------------------------------------
    # Start
    # --------------------------------------------------

    graph.add_edge(
        START,
        "idea",
    )

    graph.add_edge(
        "idea",
        "idea_quality",
    )

    # --------------------------------------------------
    # Idea quality routing
    # --------------------------------------------------

    graph.add_conditional_edges(
        "idea_quality",
        route_after_idea_quality,
        {
            "market": "market",
            "invalid": "invalid_idea",
        },
    )

    # --------------------------------------------------
    # Invalid idea
    # --------------------------------------------------

    graph.add_edge(
        "invalid_idea",
        END,
    )

    # --------------------------------------------------
    # Normal validation pipeline
    # --------------------------------------------------

    graph.add_edge(
        "market",
        "competitor",
    )

    graph.add_edge(
        "competitor",
        "persona",
    )

    graph.add_edge(
        "persona",
        "swot",
    )

    graph.add_edge(
        "swot",
        "pricing",
    )

    graph.add_edge(
        "pricing",
        "mvp",
    )

    graph.add_edge(
        "mvp",
        "evaluation",
    )

    graph.add_edge(
        "evaluation",
        "scoring",
    )

    graph.add_edge(
        "scoring",
        END,
    )

    # --------------------------------------------------
    # Checkpointing
    # --------------------------------------------------

    conn = sqlite3.connect(
        CHECKPOINT_DB,
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(conn)

    return graph.compile(
        checkpointer=checkpointer
    )