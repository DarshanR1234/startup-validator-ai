from app.schemas.agent_outputs import CompetitorAnalysis
from app.tools.web_search import search_web
from app.utils.llm_utils import invoke_structured_llm


def analyze_competitors(
    startup_idea: str,
    idea_analysis: dict,
    market_research: dict,
    target_country: str,
    target_region: str,
) -> CompetitorAnalysis:

    location = target_country.strip() or "India"

    if target_region.strip():
        location += f", {target_region.strip()}"

    # -----------------------------------------------------
    # 1. Web research
    # -----------------------------------------------------

    search_results = search_web(
        f"{startup_idea} competitors alternatives {location}",
        max_results=3,
    )

    research_items = []

    for result in search_results:

        title = str(
            result.get("title", "")
        ).strip()

        url = str(
            result.get("url", "")
        ).strip()

        content = str(
            result.get("content", "")
        ).strip()

        if len(content) > 500:
            content = content[:500]

        research_items.append(
            f"TITLE: {title}\n"
            f"URL: {url}\n"
            f"CONTENT: {content}"
        )

    research_context = "\n\n".join(
        research_items
    )

    # -----------------------------------------------------
    # 2. Compact previous-agent context
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

    target_market = market_research.get(
        "target_market",
        "",
    )

    # -----------------------------------------------------
    # 3. Structured output
    # -----------------------------------------------------

    system_prompt = (
        "You are a competitive intelligence analyst. "
        "Use only the supplied research. "
        "Never invent competitors, prices, URLs, or facts."
    )

    user_prompt = f"""
STARTUP:
{startup_idea}

LOCATION:
{location}

CUSTOMER:
{target_customer}

INDUSTRY:
{target_industry}

BUSINESS MODEL:
{business_model}

TARGET MARKET:
{target_market}

WEB RESEARCH:
{research_context}

TASK:

Identify up to 3 real competitors supported by the
research.

For each competitor return:

- name
- product
- pricing
- strengths
- weaknesses
- evidence

Also return:

- market_gaps
- competitive_risks

RULES:

- Only use competitors present in the research.
- Do not invent competitors.
- Do not invent pricing.
- If pricing is unknown, use:
  "Not publicly available"
- Do not invent URLs.
- Evidence must come from the supplied research.
- Avoid duplicate competitors.
- Keep every field concise.
- Return fewer than 3 competitors if necessary.
- market_gaps must contain concise points.
- competitive_risks must contain concise points.
- Return ONLY valid structured output.
"""

    return invoke_structured_llm(
        model_cls=CompetitorAnalysis,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=1536,
        response_mode="json_object",
    )