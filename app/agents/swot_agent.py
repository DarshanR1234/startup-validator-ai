from app.schemas.agent_outputs import SWOTAnalysis
from app.rag.retriever import (
    retrieve_documents,
    format_retrieved_documents,
)
from app.utils.llm_utils import invoke_structured_llm


def analyze_swot(
    startup_idea: str,
    idea_analysis: dict,
    market_research: dict,
    competitor_analysis: dict,
    persona_analysis: dict,
) -> SWOTAnalysis:

    # -----------------------------------------------------
    # 1. Retrieve only relevant SWOT research
    # -----------------------------------------------------

    rag_query = f"""
SWOT analysis for this startup:

{startup_idea}

Focus on:
- startup strengths
- startup weaknesses
- market opportunities
- competitive threats
- startup risks
- product-market fit
"""

    rag_documents = retrieve_documents(
        query=rag_query,
        k=3,
        category="startup_failure",
    )

    rag_context = format_retrieved_documents(
        rag_documents
    )

    # -----------------------------------------------------
    # 2. Extract only SWOT-relevant information
    # -----------------------------------------------------

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

    business_model = idea_analysis.get(
        "business_model",
        "",
    )

    assumptions = idea_analysis.get(
        "assumptions",
        [],
    )

    market_demand = market_research.get(
        "market_demand",
        "",
    )

    target_market = market_research.get(
        "target_market",
        "",
    )

    market_opportunities = market_research.get(
        "opportunities",
        [],
    )

    customer_problems = market_research.get(
        "customer_problems",
        [],
    )

    competitor_list = []

    for competitor in competitor_analysis.get(
        "competitor_list",
        [],
    )[:3]:

        competitor_list.append(
            {
                "name": competitor.get(
                    "name",
                    "",
                ),
                "strengths": competitor.get(
                    "strengths",
                    [],
                ),
                "weaknesses": competitor.get(
                    "weaknesses",
                    [],
                ),
            }
        )

    market_gaps = competitor_analysis.get(
        "market_gaps",
        [],
    )

    competitive_risks = competitor_analysis.get(
        "competitive_risks",
        [],
    )

    personas = []

    for persona in persona_analysis.get(
        "personas",
        [],
    )[:3]:

        personas.append(
            {
                "role": persona.get(
                    "role",
                    "",
                ),
                "pain_points": persona.get(
                    "pain_points",
                    [],
                ),
                "needs": persona.get(
                    "needs",
                    [],
                ),
            }
        )

    # -----------------------------------------------------
    # 3. Compact prompt
    # -----------------------------------------------------

    system_prompt = (
        "You are a startup strategy expert. "
        "Produce an objective SWOT analysis. "
        "Keep every observation concise and startup-specific."
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

BUSINESS MODEL:
{business_model}

KEY ASSUMPTIONS:
{assumptions}

MARKET DEMAND:
{market_demand}

TARGET MARKET:
{target_market}

MARKET OPPORTUNITIES:
{market_opportunities}

CUSTOMER PROBLEMS:
{customer_problems}

COMPETITORS:
{competitor_list}

MARKET GAPS:
{market_gaps}

COMPETITIVE RISKS:
{competitive_risks}

CUSTOMER PERSONAS:
{personas}

RAG RESEARCH:
{rag_context}

TASK:

Create a SWOT analysis.

STRENGTHS:
Internal advantages of this startup.

WEAKNESSES:
Internal limitations or execution challenges.

OPPORTUNITIES:
External market opportunities.

THREATS:
External competitive, technological, regulatory,
market, or business risks.

RULES:

- Each category must contain at least 2 observations.
- Strengths must be internal.
- Weaknesses must be internal.
- Opportunities must be external.
- Threats must be external.
- Avoid duplicates.
- Do not invent statistics.
- Do not invent facts.
- Use RAG only as supporting knowledge.
- Keep observations concise.
"""

    return invoke_structured_llm(
        model_cls=SWOTAnalysis,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )