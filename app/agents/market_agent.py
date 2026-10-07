# app/agents/market_agent.py

from app.schemas.agent_outputs import MarketResearch
from app.tools.web_search import search_web
from app.rag.retriever import (
    retrieve_documents,
    format_retrieved_documents,
)
from app.utils.llm_utils import invoke_structured_llm


def research_market(
    startup_idea: str,
    idea_analysis: dict,
    target_country: str,
    target_region: str,
) -> MarketResearch:

    location = target_country.strip() or "India"

    if target_region.strip():
        location += f", {target_region.strip()}"

    # -----------------------------------------------------
    # 1. RAG research
    # -----------------------------------------------------

    rag_query = f"""
Evaluate the market opportunity for:

{startup_idea}

Target market: {location}

Focus on:
market demand, customer need, market opportunity,
industry trends, and growth drivers.
"""

    rag_documents = retrieve_documents(
        query=rag_query,
        k=3,
    )

    rag_context = format_retrieved_documents(
        rag_documents
    )

    # Keep RAG context small
    rag_context = rag_context[:2500]

    # -----------------------------------------------------
    # 2. Current web research
    # -----------------------------------------------------

    search_query = (
        f"{startup_idea} market demand industry trends "
        f"customers growth opportunities in {location}"
    )

    search_results = search_web(
        search_query,
        max_results=3,
    )

    web_context = "\n\n".join(
        [
            (
                f"Title: {result.get('title', '')}\n"
                f"URL: {result.get('url', '')}\n"
                f"Content: {result.get('content', '')[:700]}"
            )
            for result in search_results
        ]
    )

    # -----------------------------------------------------
    # 3. Compact previous-agent context
    # -----------------------------------------------------

    idea_context = {
        "problem": idea_analysis.get(
            "problem",
            "",
        ),
        "solution": idea_analysis.get(
            "proposed_solution",
            "",
        ),
        "industry": idea_analysis.get(
            "target_industry",
            "",
        ),
        "customer": idea_analysis.get(
            "target_customer",
            "",
        ),
        "business_model": idea_analysis.get(
            "business_model",
            "",
        ),
        "value_proposition": idea_analysis.get(
            "key_value_proposition",
            "",
        ),
    }

    # -----------------------------------------------------
    # 4. Compact LLM prompt
    # -----------------------------------------------------

    system_prompt = (
        "You are a startup market research expert. "
        "Analyze the target market using the supplied "
        "startup information and research. "
        "Return ONLY valid JSON."
    )

    user_prompt = f"""
STARTUP:
{startup_idea}

TARGET MARKET:
{location}

IDEA ANALYSIS:
{idea_context}

RAG RESEARCH:
{rag_context}

WEB RESEARCH:
{web_context}

Return these seven fields:

market_demand
industry_trends
target_market
growth_drivers
customer_problems
opportunities
evidence

Rules:

- market_demand must be a concise assessment.
- industry_trends must be a short list.
- target_market must describe the target customers.
- growth_drivers must be a short list.
- customer_problems must be a short list.
- opportunities must be a short list.
- evidence must contain concise claims and sources.
- Use only information supported by the supplied research.
- Do not invent statistics.
- Do not invent companies.
- Do not invent sources.
- Keep every item concise.
- Keep evidence to at most 3 items.
- Return ALL seven fields.
"""

    return invoke_structured_llm(
        model_cls=MarketResearch,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=2048,
    )