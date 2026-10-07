from app.schemas.agent_outputs import CustomerPersonaAnalysis
from app.rag.retriever import (
    retrieve_documents,
    format_retrieved_documents,
)
from app.utils.llm_utils import invoke_structured_llm


def generate_customer_personas(
    startup_idea: str,
    idea_analysis: dict,
    market_research: dict,
    competitor_analysis: dict,
) -> CustomerPersonaAnalysis:

    # -----------------------------------------------------
    # 1. Retrieve customer research
    # -----------------------------------------------------

    rag_documents = retrieve_documents(
        query=f"""
Customer personas and customer needs for:

{startup_idea}

Focus on:
- target users
- customer needs
- pain points
- customer discovery
- willingness to pay
""",
        k=2,
        category="mvp",
    )

    rag_context = format_retrieved_documents(
        rag_documents
    )

    # -----------------------------------------------------
    # 2. Extract compact context
    # -----------------------------------------------------

    target_customer = idea_analysis.get(
        "target_customer",
        "",
    )

    target_industry = idea_analysis.get(
        "target_industry",
        "",
    )

    business_model = idea_analysis.get(
        "business_model",
        "",
    )

    market_target = market_research.get(
        "target_market",
        "",
    )

    customer_problems = market_research.get(
        "customer_problems",
        [],
    )[:4]

    market_gaps = competitor_analysis.get(
        "market_gaps",
        [],
    )[:3]

    # -----------------------------------------------------
    # 3. Compact structured-output prompt
    # -----------------------------------------------------

    system_prompt = (
        "You are a customer research expert. "
        "Create concise, realistic customer personas "
        "from the supplied startup information. "
        "Return only the requested structured output."
    )

    user_prompt = f"""
STARTUP:
{startup_idea}

TARGET CUSTOMER:
{target_customer}

INDUSTRY:
{target_industry}

BUSINESS MODEL:
{business_model}

TARGET MARKET:
{market_target}

CUSTOMER PROBLEMS:
{customer_problems}

MARKET GAPS:
{market_gaps}

RESEARCH:
{rag_context}

TASK:

Create exactly 2 customer personas.

For EACH persona provide:

name
role
business_type
goals
pain_points
needs
willingness_to_pay

RULES:

- Keep every field concise.
- Use 2 goals.
- Use 2 pain_points.
- Use 2 needs.
- willingness_to_pay must be a short explanation.
- Do not invent statistics.
- Do not claim verified willingness-to-pay data.
- If price is mentioned, clearly label it as an estimate.
- Keep pricing units mathematically consistent.
- Do not include unnecessary calculations.
- Do not include extra fields.
- Return ONLY the structured output.
"""

    return invoke_structured_llm(
        model_cls=CustomerPersonaAnalysis,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=1024,
        response_mode="json_object",
    )