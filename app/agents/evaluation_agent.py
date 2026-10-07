from app.schemas.agent_outputs import (
    StartupEvaluation,
    EvidenceItem,
)

from app.rag.retriever import retrieve_criterion_evidence
from app.utils.llm_utils import invoke_structured_llm


CRITERIA = [
    "market_demand",
    "customer_need",
    "competition",
    "business_potential",
    "pricing_potential",
    "feasibility",
    "mvp_clarity",
]


CRITERION_CATEGORIES = {
    "market_demand": [
        "market_validation",
        "opportunity_evaluation",
    ],
    "customer_need": [
        "market_validation",
        "opportunity_evaluation",
    ],
    "competition": [
        "market_validation",
        "startup_failure",
    ],
    "business_potential": [
        "opportunity_evaluation",
        "ai_decision_support",
    ],
    "pricing_potential": [
        "pricing",
    ],
    "feasibility": [
        "ai_decision_support",
        "startup_failure",
    ],
    "mvp_clarity": [
        "mvp",
        "opportunity_evaluation",
    ],
}


def _compact_evaluation_context(
    idea_analysis: dict,
    market_research: dict,
    competitor_analysis: dict,
    persona_analysis: dict,
    swot_analysis: dict,
    pricing_analysis: dict,
    mvp_analysis: dict,
) -> dict:

    return {
        "idea": {
            "problem": idea_analysis.get("problem", ""),
            "solution": idea_analysis.get(
                "proposed_solution",
                "",
            ),
            "target_customer": idea_analysis.get(
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
            "assumptions": idea_analysis.get(
                "assumptions",
                [],
            )[:3],
        },

        "market": {
            "demand": market_research.get(
                "market_demand",
                "",
            ),
            "target_market": market_research.get(
                "target_market",
                "",
            ),
            "customer_problems": market_research.get(
                "customer_problems",
                [],
            )[:3],
            "opportunities": market_research.get(
                "opportunities",
                [],
            )[:3],
        },

        "competition": {
            "competitors": [
                {
                    "name": item.get(
                        "name",
                        "",
                    ),
                    "product": item.get(
                        "product",
                        "",
                    ),
                    "pricing": item.get(
                        "pricing",
                        "",
                    ),
                    "strengths": item.get(
                        "strengths",
                        [],
                    )[:2],
                    "weaknesses": item.get(
                        "weaknesses",
                        [],
                    )[:2],
                }
                for item in competitor_analysis.get(
                    "competitor_list",
                    [],
                )[:3]
            ],
            "market_gaps": competitor_analysis.get(
                "market_gaps",
                [],
            )[:3],
            "competitive_risks": competitor_analysis.get(
                "competitive_risks",
                [],
            )[:3],
        },

        "personas": [
            {
                "role": persona.get(
                    "role",
                    "",
                ),
                "business_type": persona.get(
                    "business_type",
                    "",
                ),
                "pain_points": persona.get(
                    "pain_points",
                    [],
                )[:2],
                "needs": persona.get(
                    "needs",
                    [],
                )[:2],
                "willingness_to_pay": persona.get(
                    "willingness_to_pay",
                    "",
                ),
            }
            for persona in persona_analysis.get(
                "personas",
                [],
            )[:3]
        ],

        "swot": {
            "strengths": swot_analysis.get(
                "strengths",
                [],
            )[:3],
            "weaknesses": swot_analysis.get(
                "weaknesses",
                [],
            )[:3],
            "opportunities": swot_analysis.get(
                "opportunities",
                [],
            )[:3],
            "threats": swot_analysis.get(
                "threats",
                [],
            )[:3],
        },

        "pricing": {
            "pricing_model": pricing_analysis.get(
                "pricing_model",
                "",
            ),
            "recommended_price": pricing_analysis.get(
                "recommended_price",
                "",
            ),
            "pricing_tiers": pricing_analysis.get(
                "pricing_tiers",
                [],
            )[:2],
            "pricing_risks": pricing_analysis.get(
                "pricing_risks",
                [],
            )[:3],
        },

        "mvp": {
            "core_features": mvp_analysis.get(
                "core_features",
                [],
            )[:3],
            "development_priority": mvp_analysis.get(
                "development_priority",
                [],
            )[:3],
            "excluded_features": mvp_analysis.get(
                "excluded_features",
                [],
            )[:2],
            "mvp_rationale": mvp_analysis.get(
                "mvp_rationale",
                [],
            )[:2],
        },
    }


def _criterion_queries(
    startup_idea: str,
    context: dict,
) -> dict[str, str]:

    idea = context["idea"]
    market = context["market"]
    competition = context["competition"]
    personas = context["personas"]
    pricing = context["pricing"]
    mvp = context["mvp"]

    return {
        "market_demand": f"""
Market demand for:

Startup:
{startup_idea}

Target market:
{market["target_market"]}

Current demand:
{market["demand"]}

Focus on demand, adoption, growth, and demand
for the proposed solution.
""",

        "customer_need": f"""
Customer need for:

Startup:
{startup_idea}

Problem:
{idea["problem"]}

Target customer:
{idea["target_customer"]}

Customer problems:
{market["customer_problems"]}

Personas:
{personas}

Focus on pain points, unmet needs, and adoption.
""",

        "competition": f"""
Competition for:

Startup:
{startup_idea}

Competitors:
{competition["competitors"]}

Market gaps:
{competition["market_gaps"]}

Competitive risks:
{competition["competitive_risks"]}

Focus on competition, barriers, differentiation,
and incumbent strength.
""",

        "business_potential": f"""
Business potential for:

Startup:
{startup_idea}

Business model:
{idea["business_model"]}

Value proposition:
{idea["value_proposition"]}

Target customer:
{idea["target_customer"]}

Market opportunities:
{market["opportunities"]}

Focus on commercial viability, scalability,
revenue potential, and defensibility.
""",

        "pricing_potential": f"""
Pricing potential for:

Startup:
{startup_idea}

Pricing model:
{pricing["pricing_model"]}

Recommended price:
{pricing["recommended_price"]}

Pricing tiers:
{pricing["pricing_tiers"]}

Personas:
{personas}

Focus on willingness to pay, price sensitivity,
and purchasing behavior.
""",

        "feasibility": f"""
Feasibility for:

Startup:
{startup_idea}

Solution:
{idea["solution"]}

Assumptions:
{idea["assumptions"]}

SWOT weaknesses:
{context["swot"]["weaknesses"]}

SWOT threats:
{context["swot"]["threats"]}

Focus on technical, operational, regulatory,
and implementation difficulty.
""",

        "mvp_clarity": f"""
MVP clarity for:

Startup:
{startup_idea}

Core features:
{mvp["core_features"]}

Development priorities:
{mvp["development_priority"]}

Excluded features:
{mvp["excluded_features"]}

Focus on scope, prioritization, validation,
and early customer learning.
""",
    }


def _filter_low_quality_documents(
    documents: list,
    query: str,
) -> list:
    """
    Filter obviously unusable RAG documents while preserving
    semantically relevant documents returned by vector retrieval.

    Important:
    Semantic retrieval is the primary relevance mechanism.
    Lexical overlap is only a weak secondary signal and must
    not reject otherwise useful documents.
    """

    filtered = []

    query_words = {
        word.lower().strip(".,!?;:()[]{}\"'")
        for word in query.split()
        if len(word.strip(".,!?;:()[]{}\"'")) >= 4
    }

    bad_markers = [
        "references",
        "bibliography",
        "acknowledgment",
        "acknowledgements",
        "issn",
        "isbn",
    ]

    for document in documents:

        if not document or not getattr(
            document,
            "page_content",
            None,
        ):
            continue

        text = " ".join(
            document.page_content.split()
        ).strip()

        # Reject empty or extremely small chunks.
        if len(text) < 180:
            continue

        lower_text = text.lower()

        # --------------------------------------------------
        # 1. Reject obvious bibliography/reference chunks
        # --------------------------------------------------

        if any(
            marker in lower_text
            for marker in bad_markers
        ):
            continue

        # --------------------------------------------------
        # 2. Reject chunks dominated by URLs
        # --------------------------------------------------

        words = text.split()

        url_count = sum(
            1
            for word in words
            if "http://" in word
            or "https://" in word
            or "www." in word
        )

        if words and (
            url_count / len(words) > 0.15
        ):
            continue

        # --------------------------------------------------
        # 3. Weak lexical relevance signal
        # --------------------------------------------------
        # Do NOT reject documents purely because exact
        # query words are missing. Embedding retrieval already
        # handles semantic similarity.

        text_words = {
            word.lower().strip(".,!?;:()[]{}\"'")
            for word in words
            if len(word.strip(".,!?;:()[]{}\"'")) >= 4
        }

        overlap = query_words.intersection(
            text_words
        )

        relevance_ratio = (
            len(overlap)
            / max(len(query_words), 1)
        )

        # --------------------------------------------------
        # 4. Only reject completely unrelated chunks
        # --------------------------------------------------
        #
        # A vector-retrieved document with zero lexical overlap
        # can still be semantically relevant, so keep it.
        #
        # We only reject when the document is extremely short
        # or clearly contains no meaningful research language.
        #

        research_markers = [
            "market",
            "customer",
            "consumer",
            "business",
            "startup",
            "product",
            "pricing",
            "revenue",
            "competition",
            "competitive",
            "demand",
            "adoption",
            "growth",
            "technology",
            "innovation",
            "strategy",
            "mvp",
            "validation",
            "purchase",
            "willingness",
            "problem",
            "solution",
            "risk",
            "feasibility",
        ]

        research_signal_count = sum(
            1
            for marker in research_markers
            if marker in lower_text
        )

        # If there is absolutely no lexical overlap AND
        # essentially no research signal, reject it.
        #
        # This is intentionally much less aggressive than
        # the previous 0.03 query-overlap threshold.

        if (
            relevance_ratio == 0
            and research_signal_count == 0
        ):
            continue

        filtered.append(document)

        print(
            f"[RAG FILTER] kept | "
            f"overlap={relevance_ratio:.3f} | "
            f"research_signals={research_signal_count}"
        )

    return filtered
def _retrieve_criterion_evidence(
    startup_idea: str,
    context: dict,
) -> dict[str, list]:

    queries = _criterion_queries(
        startup_idea,
        context,
    )

    criterion_documents = {}

    for criterion, query in queries.items():

        categories = CRITERION_CATEGORIES.get(
            criterion,
            [],
        )

        try:

            documents = retrieve_criterion_evidence(
                query=query,
                categories=categories,
                k_per_category=1,
            )

            raw_count = len(documents)

            documents = _filter_low_quality_documents(
                documents,
                query,
            )

            print(
                f"[RAG QUALITY] {criterion}: "
                f"{raw_count} retrieved → "
                f"{len(documents)} quality documents"
            )

            criterion_documents[criterion] = documents

            print(
                f"[RAG] {criterion}: "
                f"{len(documents)} documents "
                f"from {categories}"
            )

        except Exception as exc:

            print(
                f"[RAG ERROR] {criterion}: {exc}"
            )

            criterion_documents[criterion] = []

    return criterion_documents


def _format_evidence(
    documents: list,
) -> str:

    formatted = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        metadata = document.metadata or {}

        title = metadata.get(
            "title",
            metadata.get(
                "file_name",
                "Unknown title",
            ),
        )

        content = " ".join(
            document.page_content.split()
        )

        if len(content) > 300:
            content = (
                content[:300]
                .rsplit(" ", 1)[0]
                + "..."
            )

        formatted.append(
            f"""
EVIDENCE {index}
Title: {title}
Content: {content}
"""
        )

    return "\n".join(formatted)


def _attach_relevant_evidence(
    evaluation: StartupEvaluation,
    criterion_documents: dict[str, list],
) -> StartupEvaluation:

    for criterion in CRITERIA:

        criterion_score = getattr(
            evaluation,
            criterion,
        )

        documents = criterion_documents.get(
            criterion,
            [],
        )

        evidence = []

        for document in documents[:2]:

            metadata = document.metadata or {}

            source = str(
                metadata.get(
                    "source",
                    metadata.get(
                        "file_name",
                        metadata.get(
                            "source_file",
                            "",
                        ),
                    ),
                )
            )

            source_title = str(
                metadata.get(
                    "title",
                    metadata.get(
                        "file_name",
                        source,
                    ),
                )
            )

            page = str(
                metadata.get(
                    "page",
                    metadata.get(
                        "page_number",
                        "",
                    ),
                )
            )

            doi = str(
                metadata.get(
                    "doi",
                    "",
                )
            )

            content = " ".join(
                document.page_content.split()
            ).strip()

            if len(content) > 500:
                content = (
                    content[:500]
                    .rsplit(" ", 1)[0]
                    + "..."
                )

            if not content:
                continue

            evidence.append(
                EvidenceItem(
                    claim=content,
                    source_title=source_title,
                    source_type="RAG research",
                    page=page,
                    doi=doi,
                    source=source,
                )
            )

        criterion_score.evidence = evidence

    return evaluation


def evaluate_startup(
    startup_idea: str,
    idea_analysis: dict,
    market_research: dict,
    competitor_analysis: dict,
    persona_analysis: dict,
    swot_analysis: dict,
    pricing_analysis: dict,
    mvp_analysis: dict,
) -> StartupEvaluation:

    compact_context = _compact_evaluation_context(
        idea_analysis,
        market_research,
        competitor_analysis,
        persona_analysis,
        swot_analysis,
        pricing_analysis,
        mvp_analysis,
    )

    criterion_documents = _retrieve_criterion_evidence(
        startup_idea,
        compact_context,
    )

    rag_sections = []

    for criterion, documents in criterion_documents.items():

        if not documents:
            continue

        rag_sections.append(
            f"""
RAG RESEARCH — {criterion}
{_format_evidence(documents)}
"""
        )

    rag_context = "\n".join(
        rag_sections
    )

    system_prompt = (
        "You are a strict startup investment evaluator. "
        "Score the startup itself, not merely the attractiveness "
        "of the industry. A large or growing market does not "
        "automatically mean a strong startup. "
        "Use integer scores from 0 to 10."
    )

    user_prompt = f"""
STARTUP:
{startup_idea}

ANALYSIS:
{compact_context}

RESEARCH:
{rag_context}

Evaluate exactly these seven criteria:

1. market_demand
2. customer_need
3. competition
4. business_potential
5. pricing_potential
6. feasibility
7. mvp_clarity

For each return:

score: integer 0-10
reason: concise
evidence: []

IMPORTANT SCORING FRAMEWORK:

MARKET DEMAND:
Score demand for THIS solution, not just the overall industry.

10 = strong proven demand for this specific solution
7-9 = strong relevant demand
4-6 = moderate or uncertain demand
1-3 = weak demand
0 = no meaningful demand

CUSTOMER NEED:
Score the severity and frequency of the problem.

10 = urgent, frequent, expensive problem
7-9 = clear meaningful problem
4-6 = useful but non-critical problem
1-3 = weak problem
0 = no clear problem

COMPETITION:
Score the startup's competitive position, NOT how many
competitors exist.

10 = strong differentiation and defensibility
7-9 = clear differentiation
4-6 = some differentiation but significant competition
1-3 = commodity/easily copied/strong incumbents
0 = no realistic competitive advantage

BUSINESS POTENTIAL:
Evaluate:
- customer acquisition
- margins
- scalability
- recurring revenue
- defensibility
- operational economics

A large market alone must NOT justify a high score.

PRICING POTENTIAL:
Evaluate whether customers can realistically pay enough
for the business to be attractive after costs.

FEASIBILITY:
Evaluate technical and operational difficulty, regulation,
capital requirements, logistics, and execution risk.

MVP CLARITY:
Evaluate whether the MVP is focused and testable.

COMMODITY / WEAK DIFFERENTIATION RULE:

If the startup mainly resells an ordinary commodity or offers
a service that established competitors already provide with
little meaningful differentiation:

- competition should generally be 1-5
- business_potential should generally be 2-6
- pricing_potential should generally be 2-6
- feasibility should reflect operational/regulatory risk

Do NOT give high scores simply because the underlying market
is large.

OVERALL CALIBRATION:

Weak or commodity startup:
mostly 2-6

Average startup:
mostly 5-7

Strong differentiated startup:
mostly 7-9

Exceptional startup:
can reach 9-10

Do not cluster every startup around 7-8.

Be willing to give low scores when justified.

RULES:

- ALL seven criteria are required.
- Scores must be integers from 0 to 10.
- Reasons must be concise.
- Do not invent statistics.
- Do not invent sources.
- Evidence must be [].
- Return ONLY valid JSON.
"""

    evaluation = invoke_structured_llm(
        model_cls=StartupEvaluation,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=2048,
        response_mode="json_object",
    )

    return _attach_relevant_evidence(
        evaluation,
        criterion_documents,
    )