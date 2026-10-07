from app.schemas.agent_outputs import MVPAnalysis
from app.rag.retriever import (
    retrieve_documents,
    format_retrieved_documents,
)
from app.utils.llm_utils import invoke_structured_llm


def recommend_mvp(
    startup_idea: str,
    idea_analysis: dict,
    market_research: dict,
    competitor_analysis: dict,
    persona_analysis: dict,
    swot_analysis: dict,
    pricing_analysis: dict,
) -> MVPAnalysis:

    rag_query = f"""
MVP strategy for:

{startup_idea}

Focus on:
- minimum viable product
- validated learning
- experimentation
- product-market fit
- early user feedback
- feature prioritization
"""

    rag_documents = retrieve_documents(
        query=rag_query,
        k=3,
        category="mvp",
    )

    rag_context = format_retrieved_documents(
        rag_documents
    )

    problem = idea_analysis.get(
        "problem",
        "",
    )

    proposed_solution = idea_analysis.get(
        "proposed_solution",
        "",
    )

    target_customer = idea_analysis.get(
        "target_customer",
        "",
    )

    assumptions = idea_analysis.get(
        "assumptions",
        [],
    )[:4]

    customer_problems = market_research.get(
        "customer_problems",
        [],
    )[:4]

    market_gaps = competitor_analysis.get(
        "market_gaps",
        [],
    )[:3]

    persona_needs = []

    for persona in persona_analysis.get(
        "personas",
        [],
    )[:3]:

        persona_needs.append(
            {
                "role": persona.get(
                    "role",
                    "",
                ),
                "needs": persona.get(
                    "needs",
                    [],
                )[:3],
                "pain_points": persona.get(
                    "pain_points",
                    [],
                )[:3],
            }
        )

    strengths = swot_analysis.get(
        "strengths",
        [],
    )[:3]

    weaknesses = swot_analysis.get(
        "weaknesses",
        [],
    )[:3]

    pricing_model = pricing_analysis.get(
        "pricing_model",
        "",
    )

    recommended_price = pricing_analysis.get(
        "recommended_price",
        "",
    )

    system_prompt = (
        "You are a startup product strategy expert. "
        "Design a small, realistic MVP that validates the "
        "startup's most important assumptions and customer demand. "
        "You MUST provide every required output field."
    )

    user_prompt = f"""
STARTUP IDEA:
{startup_idea}

PROBLEM:
{problem}

PROPOSED SOLUTION:
{proposed_solution}

TARGET CUSTOMER:
{target_customer}

KEY ASSUMPTIONS:
{assumptions}

CUSTOMER PROBLEMS:
{customer_problems}

MARKET GAPS:
{market_gaps}

CUSTOMER NEEDS:
{persona_needs}

SWOT STRENGTHS:
{strengths}

SWOT WEAKNESSES:
{weaknesses}

PRICING MODEL:
{pricing_model}

RECOMMENDED PRICE:
{recommended_price}

MVP RESEARCH:
{rag_context}

TASK:

Design the MVP and return ALL five fields:

1. core_features
2. future_features
3. excluded_features
4. development_priority
5. mvp_rationale

IMPORTANT:

core_features:
- Provide 3 to 6 essential features.
- These must be necessary for the first usable MVP.

future_features:
- Provide 2 to 4 useful features that should be postponed.

excluded_features:
- Provide at least 2 features that should NOT be built in the first MVP.
- Explain what should intentionally be avoided through the feature name.

development_priority:
- Provide 3 to 6 ordered implementation priorities.
- Priority 1 is the highest priority.
- Every item MUST contain a name and integer priority.

mvp_rationale:
- Provide at least 3 concise reasons.
- Every item MUST contain a reason.

RULES:

- EVERY required field must be present.
- NEVER return an empty array for excluded_features.
- NEVER return an empty array for development_priority.
- NEVER return an empty array for mvp_rationale.
- Every feature object MUST contain:
  name
  priority
- Every rationale object MUST contain:
  reason
- Priority must be an integer.
- Lower number means higher implementation priority.
- Keep the MVP small.
- Prioritize features that test the riskiest assumptions.
- Do not add features simply because competitors have them.
- Avoid unnecessary complexity.
- Do not invent statistics.
- Do not invent unsupported technical requirements.
- Keep names and reasons concise.
- Return ONLY the structured JSON output.
"""

    return invoke_structured_llm(
        model_cls=MVPAnalysis,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=1536,
    )