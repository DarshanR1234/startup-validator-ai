from app.rag.ingest import load_pdfs, split_documents
from app.rag.vectorstore import create_vectorstore


def main():

    print("\n===== BUILDING RAG KNOWLEDGE BASE =====")

    print("\n[1/3] Loading PDFs...")
    documents = load_pdfs()

    print(f"Loaded {len(documents)} pages.")

    print("\n[2/3] Creating chunks...")
    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")

    print("\n[3/3] Creating embeddings and ChromaDB...")

    vectorstore = create_vectorstore(chunks)

    print("\n===== RAG KNOWLEDGE BASE READY =====")
    print("Collection: startup_validation_knowledge")
    print("Vector store: data/chroma")

    return vectorstore


if __name__ == "__main__":
    main()