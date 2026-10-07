from pathlib import Path
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


DOCUMENTS_DIR = Path("data/documents")


REFERENCE_MARKERS = [
    "references",
    "bibliography",
    "acknowledgments",
    "acknowledgements",
]

MIN_CHUNK_LENGTH = 250


def _clean_page_text(text: str) -> str:
    """
    Clean obvious PDF extraction noise while preserving
    meaningful research content.
    """

    text = text.replace("\x00", " ")

    # Normalize whitespace.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive newlines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _looks_like_reference_section(text: str) -> bool:
    """
    Detect pages/chunks that are primarily bibliography/reference
    material.
    """

    lower = text.lower().strip()

    if not lower:
        return True

    # Strong reference-section indicators.
    first_lines = "\n".join(
        lower.splitlines()[:8]
    )

    for marker in REFERENCE_MARKERS:
        if re.search(
            rf"\b{re.escape(marker)}\b",
            first_lines,
        ):
            return True

    # DOI / URL dominated text.
    words = lower.split()

    if not words:
        return True

    url_count = sum(
        1
        for word in words
        if "http://" in word
        or "https://" in word
        or "www." in word
        or "doi.org/" in word
    )

    if len(words) >= 20 and (
        url_count / len(words) > 0.12
    ):
        return True

    # Typical bibliography patterns.
    citation_patterns = [
        r"\bdoi:\s*10\.",
        r"\b10\.\d{4,9}/[-._;()/:a-z0-9]+\b",
        r"\bet al\.,?\s*\d{4}\b",
        r"\(\d{4}\)\.",
    ]

    citation_hits = sum(
        len(
            re.findall(
                pattern,
                lower,
            )
        )
        for pattern in citation_patterns
    )

    if citation_hits >= 4:
        return True

    return False


def _trim_reference_section(text: str) -> str:
    """
    Remove content after an obvious References/Bibliography heading.
    """

    lines = text.splitlines()

    for index, line in enumerate(lines):

        normalized = re.sub(
            r"[^a-z ]",
            "",
            line.lower(),
        ).strip()

        if normalized in {
            "references",
            "bibliography",
            "acknowledgments",
            "acknowledgements",
        }:
            remaining = "\n".join(
                lines[:index]
            )

            if len(remaining.strip()) >= MIN_CHUNK_LENGTH:
                return remaining.strip()

    return text.strip()


def load_pdfs():

    documents = []

    pdf_files = sorted(
        DOCUMENTS_DIR.rglob("*.pdf")
    )

    print(
        f"Found {len(pdf_files)} PDF files."
    )

    for pdf_file in pdf_files:

        print(
            f"Loading: {pdf_file}"
        )

        try:

            loader = PyPDFLoader(
                str(pdf_file)
            )

            pages = loader.load()

        except Exception as exc:

            print(
                f"[PDF ERROR] {pdf_file}: {exc}"
            )

            continue

        for page in pages:

            raw_text = page.page_content

            cleaned_text = _clean_page_text(
                raw_text
            )

            cleaned_text = _trim_reference_section(
                cleaned_text
            )

            if not cleaned_text:
                continue

            if _looks_like_reference_section(
                cleaned_text
            ):
                print(
                    f"[SKIP REFERENCES] "
                    f"{pdf_file.name} "
                    f"page={page.metadata.get('page', '?')}"
                )
                continue

            page.page_content = cleaned_text

            # Preserve useful provenance.
            page.metadata["file_name"] = (
                pdf_file.name
            )

            page.metadata["category"] = (
                pdf_file.parent.name
            )

            page.metadata["source"] = (
                pdf_file.name
            )

            page.metadata["page"] = (
                page.metadata.get(
                    "page",
                    "",
                )
            )

            documents.append(page)

    return documents


def _is_low_quality_chunk(text: str) -> bool:
    """
    Reject obvious extraction/reference noise.
    """

    text = text.strip()

    if len(text) < MIN_CHUNK_LENGTH:
        return True

    lower = text.lower()

    words = text.split()

    if len(words) < 40:
        return True

    # URL-heavy chunks.
    url_count = sum(
        1
        for word in words
        if "http://" in word
        or "https://" in word
        or "www." in word
        or "doi.org/" in word
    )

    if url_count >= 3:
        return True

    if len(words) > 0 and (
        url_count / len(words) > 0.08
    ):
        return True

    # Reference-like chunks.
    if _looks_like_reference_section(
        text
    ):
        return True

    # Excessive citation brackets.
    bracket_count = (
        text.count("[")
        + text.count("]")
    )

    if bracket_count > 16:
        return True

    # Chunks dominated by citation entries.
    citation_hits = 0

    citation_hits += len(
        re.findall(
            r"\bdoi:\s*10\.",
            lower,
        )
    )

    citation_hits += len(
        re.findall(
            r"\b10\.\d{4,9}/[-._;()/:a-z0-9]+\b",
            lower,
        )
    )

    if citation_hits >= 3:
        return True

    return False


def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            "; ",
            ", ",
            " ",
        ],
    )

    chunks = splitter.split_documents(
        documents
    )

    clean_chunks = []

    for chunk in chunks:

        text = _clean_page_text(
            chunk.page_content
        )

        if _is_low_quality_chunk(
            text
        ):
            continue

        chunk.page_content = text

        clean_chunks.append(
            chunk
        )

    return clean_chunks


if __name__ == "__main__":

    documents = load_pdfs()

    print(
        f"Total quality pages loaded: "
        f"{len(documents)}"
    )

    chunks = split_documents(
        documents
    )

    print(
        f"Total quality chunks created: "
        f"{len(chunks)}"
    )

    if chunks:

        print(
            "\n===== SAMPLE CHUNK ====="
        )

        print(
            chunks[0].page_content[:1000]
        )

        print(
            "\nMetadata:"
        )

        print(
            chunks[0].metadata
        )