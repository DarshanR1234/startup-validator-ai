from app.agents.idea_agent import analyze_startup_idea
from app.agents.market_agent import research_market
from app.agents.competitor_agent import analyze_competitors
from app.agents.persona_agent import generate_customer_personas
from app.agents.swot_agent import analyze_swot
from app.agents.pricing_agent import recommend_pricing
from app.agents.mvp_agent import recommend_mvp
from app.agents.evaluation_agent import evaluate_startup


from app.scoring.scoring_engine import calculate_validation_score

from app.graph.state import StartupState


def idea_node(state: StartupState) -> dict:

    result = analyze_startup_idea(
        state["startup_idea"]
    )

    return {
        "idea_analysis": result.model_dump()
    }


def invalid_idea_node(
    state: StartupState,
) -> dict:
    """
    Return a safe response when the startup idea
    does not contain enough information for validation.
    """

    message = state.get(
        "idea_quality_message",
        "Startup idea is too vague to evaluate reliably.",
    )

    return {
        "scoring_result": {
            "overall_score": 0,
            "verdict": "Insufficient Information",
            "summary": message,
            "key_strengths": [],
            "key_weaknesses": [
                "Problem is not clearly specified.",
                "Proposed solution is not clearly specified.",
                "Target customer is not clearly specified.",
            ],
            "opportunities": [],
            "threats": [],
        }
    }


def market_node(state: StartupState) -> dict:

    result = research_market(
        state["startup_idea"],
        state["idea_analysis"],
        state.get("target_country", "India"),
        state.get("target_region", ""),
    )

    return {
        "market_research": result.model_dump()
    }


def competitor_node(state: StartupState) -> dict:

    result = analyze_competitors(
        state["startup_idea"],
        state["idea_analysis"],
        state["market_research"],
        state.get("target_country", "India"),
        state.get("target_region", ""),
    )

    return {
        "competitor_analysis": result.model_dump()
    }


def persona_node(state: StartupState) -> dict:

    result = generate_customer_personas(
        state["startup_idea"],
        state["idea_analysis"],
        state["market_research"],
        state["competitor_analysis"],
    )

    return {
        "persona_analysis": result.model_dump()
    }


def swot_node(state: StartupState) -> dict:

    result = analyze_swot(
        state["startup_idea"],
        state["idea_analysis"],
        state["market_research"],
        state["competitor_analysis"],
        state["persona_analysis"],
    )

    return {
        "swot_analysis": result.model_dump()
    }


def pricing_node(state: StartupState) -> dict:

    result = recommend_pricing(
        state["startup_idea"],
        state["idea_analysis"],
        state["market_research"],
        state["competitor_analysis"],
        state["persona_analysis"],
        state.get("target_country", "India"),
        state.get("target_region", ""),
    )

    return {
        "pricing_analysis": result.model_dump()
    }


def mvp_node(state: StartupState) -> dict:

    result = recommend_mvp(
        state["startup_idea"],
        state["idea_analysis"],
        state["market_research"],
        state["competitor_analysis"],
        state["persona_analysis"],
        state["swot_analysis"],
        state["pricing_analysis"],
    )

    return {
        "mvp_analysis": result.model_dump()
    }


def evaluation_node(state: StartupState) -> dict:

    result = evaluate_startup(
        state["startup_idea"],
        state["idea_analysis"],
        state["market_research"],
        state["competitor_analysis"],
        state["persona_analysis"],
        state["swot_analysis"],
        state["pricing_analysis"],
        state["mvp_analysis"],
    )

    return {
        "evaluation": result.model_dump()
    }


def scoring_node(state: StartupState) -> dict:

    from app.schemas.agent_outputs import StartupEvaluation

    evaluation = StartupEvaluation.model_validate(
        state["evaluation"]
    )

    result = calculate_validation_score(
        evaluation
    )

    return {
        "scoring_result": result
    }