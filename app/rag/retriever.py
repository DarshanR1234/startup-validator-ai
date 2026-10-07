from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "startup_validation_knowledge"


@lru_cache(maxsize=1)
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


@lru_cache(maxsize=1)
def get_vectorstore():
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME,
    )


def _source_key(document):
    metadata = document.metadata or {}

    source = metadata.get(
        "source",
        metadata.get("file_name", "unknown"),
    )

    page = metadata.get(
        "page_label",
        metadata.get("page", ""),
    )

    return (
        str(source),
        str(page),
    )


def retrieve_documents(
    query: str,
    k: int = 5,
    category: str | None = None,
):
    """
    Retrieve diverse documents from Chroma.

    Important:
    - Uses MMR for diversity.
    - Retrieves more candidates than requested.
    - Removes duplicate source/page combinations.
    - Does NOT apply an arbitrary similarity threshold here.
      Relevance filtering is handled by the evaluation layer.
    """

    vectorstore = get_vectorstore()

    fetch_k = max(k * 5, 20)

    search_kwargs = {
        "k": fetch_k,
        "fetch_k": fetch_k,
        "lambda_mult": 0.5,
    }

    if category:
        search_kwargs["filter"] = {
            "category": category
        }

    candidates = vectorstore.max_marginal_relevance_search(
        query,
        **search_kwargs,
    )

    results = []
    seen = set()

    for document in candidates:
        key = _source_key(document)

        if key in seen:
            continue

        seen.add(key)
        results.append(document)

        if len(results) >= k:
            break

    return results


def retrieve_multi_category_documents(
    query: str,
    categories: list[str],
    k_per_category: int = 2,
):
    """
    Retrieve relevant documents from multiple research
    categories independently.
    """

    all_documents = []
    seen = set()

    for category in categories:

        documents = retrieve_documents(
            query=query,
            k=k_per_category,
            category=category,
        )

        for document in documents:

            key = _source_key(document)

            if key in seen:
                continue

            seen.add(key)
            all_documents.append(document)

    return all_documents


def _build_retrieval_query(
    query: str,
    criterion: str,
) -> str:

    focus_terms = {
        "market_demand": [
            "market demand",
            "market adoption",
            "market growth",
            "industry demand",
            "market size",
            "customer demand",
        ],
        "customer_need": [
            "customer needs",
            "customer problems",
            "pain points",
            "unmet needs",
            "user needs",
            "willingness to adopt",
        ],
        "competition": [
            "competitive landscape",
            "competitors",
            "competitive advantage",
            "competitive intensity",
            "market competition",
            "differentiation",
        ],
        "business_potential": [
            "business model",
            "commercial viability",
            "scalability",
            "revenue model",
            "business opportunity",
            "growth potential",
        ],
        "pricing_potential": [
            "SaaS pricing",
            "subscription pricing",
            "willingness to pay",
            "price sensitivity",
            "pricing strategy",
            "value-based pricing",
        ],
        "feasibility": [
            "technical feasibility",
            "technology feasibility",
            "implementation",
            "technical challenges",
            "technology maturity",
            "AI implementation",
        ],
        "mvp_clarity": [
            "minimum viable product",
            "MVP",
            "validated learning",
            "feature prioritization",
            "product-market fit",
            "customer feedback",
        ],
    }

    terms = focus_terms.get(criterion, [])

    return f"""
{query}

CRITERION:
{criterion}

IMPORTANT RESEARCH CONCEPTS:
{", ".join(terms)}

Prioritize research chunks that directly discuss
these concepts.
""".strip()


def _get_source_metadata(document):

    metadata = document.metadata or {}

    return {
        "title": str(
            metadata.get(
                "title",
                metadata.get(
                    "file_name",
                    "Unknown title",
                ),
            )
        ),
        "author": str(
            metadata.get(
                "author",
                "Unknown author",
            )
        ),
        "category": str(
            metadata.get(
                "category",
                "Unknown",
            )
        ),
        "page": str(
            metadata.get(
                "page_label",
                metadata.get(
                    "page",
                    "Unknown",
                ),
            )
        ),
        "doi": str(
            metadata.get(
                "doi",
                "",
            )
        ),
        "source": str(
            metadata.get(
                "source",
                metadata.get(
                    "file_name",
                    "Unknown source",
                ),
            )
        ),
        "file_name": str(
            metadata.get(
                "file_name",
                metadata.get(
                    "source",
                    "Unknown file",
                ),
            )
        ),
    }


def format_retrieved_documents(documents) -> str:

    formatted = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        source = _get_source_metadata(document)

        source_info = (
            f"Title: {source['title']}\n"
            f"Author: {source['author']}\n"
            f"Category: {source['category']}\n"
            f"Page: {source['page']}\n"
            f"Source: {source['source']}"
        )

        if source["doi"]:
            source_info += f"\nDOI: {source['doi']}"

        content = " ".join(
            document.page_content.split()
        )

        if len(content) > 1500:
            content = (
                content[:1500]
                .rsplit(" ", 1)[0]
                + "..."
            )

        formatted.append(
            f"""
--- Retrieved Source {index} ---

{source_info}

Content:
{content}
""".strip()
        )

    return "\n\n".join(formatted)


def retrieve_evaluation_knowledge(
    query: str,
    k_per_category: int = 1,
):
    categories = [
        "opportunity_evaluation",
        "ai_decision_support",
        "startup_failure",
        "market_validation",
        "pricing",
        "mvp",
    ]

    return retrieve_multi_category_documents(
        query=query,
        categories=categories,
        k_per_category=k_per_category,
    )


def retrieve_criterion_evidence(
    query: str,
    categories: list[str],
    k_per_category: int = 2,
):
    """
    Retrieve evidence specifically for one evaluation criterion.

    The criterion is detected from the query and criterion-specific
    research concepts are appended before retrieval.
    """

    criterion = ""

    criteria = [
        "market_demand",
        "customer_need",
        "competition",
        "business_potential",
        "pricing_potential",
        "feasibility",
        "mvp_clarity",
    ]

    for possible_criterion in criteria:
        if possible_criterion in query:
            criterion = possible_criterion
            break

    if criterion:
        query = _build_retrieval_query(
            query=query,
            criterion=criterion,
        )

    return retrieve_multi_category_documents(
        query=query,
        categories=categories,
        k_per_category=k_per_category,
    )


def format_evidence_for_evaluation(
    documents,
) -> str:

    formatted = []

    for index, document in enumerate(
        documents,
        start=1,
    ):

        source = _get_source_metadata(document)

        content = " ".join(
            document.page_content.split()
        )

        if len(content) > 1200:
            content = (
                content[:1200]
                .rsplit(" ", 1)[0]
                + "..."
            )

        formatted.append(
            f"""
RAG SOURCE {index}

Title: {source['title']}
Author: {source['author']}
Category: {source['category']}
Page: {source['page']}
DOI: {source['doi']}
File: {source['file_name']}

Content:
{content}
""".strip()
        )

    return "\n\n".join(formatted)