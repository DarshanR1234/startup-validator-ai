from typing import TypedDict


class StartupState(TypedDict, total=False):

    # User input
    startup_idea: str
    target_country: str
    target_region: str

    # Agent outputs
    idea_analysis: dict
    market_research: dict
    competitor_analysis: dict
    persona_analysis: dict
    swot_analysis: dict
    pricing_analysis: dict
    mvp_analysis: dict

    # Idea quality gate
    idea_valid: bool
    idea_quality_message: str

    # Evaluation
    evaluation: dict

    # Final deterministic scoring
    scoring_result: dict