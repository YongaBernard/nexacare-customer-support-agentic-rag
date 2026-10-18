from pathlib import Path

from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "data" / "knowledge_base"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"


# ---------------------------------------------------------
# Embedding model
# ---------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


class LocalSentenceTransformerEmbeddings(Embeddings):
    """
    Local embedding implementation using Sentence Transformers.

    The model runs locally on the developer machine.
    No AWS embedding service is required.
    """

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return embedding.tolist()


# ---------------------------------------------------------
# Governance metadata
# ---------------------------------------------------------

DOCUMENT_METADATA = {
    "company_overview.md": {
        "document_owner": "Customer Operations",
        "classification": "Internal - Approved AI Knowledge Source",
        "review_frequency": "Quarterly",
        "version": "1.0",
    },
    "returns_refund_policy.md": {
        "document_owner": "Customer Operations",
        "classification": "Internal - Approved AI Knowledge Source",
        "review_frequency": "Quarterly",
        "version": "1.0",
    },
    "shipping_order_tracking_policy.md": {
        "document_owner": "Logistics & Customer Operations",
        "classification": "Internal - Approved AI Knowledge Source",
        "review_frequency": "Quarterly",
        "version": "1.0",
    },
    "account_billing_policy.md": {
        "document_owner": "Finance & Customer Operations",
        "classification": "Internal - Approved AI Knowledge Source",
        "review_frequency": "Quarterly",
        "version": "1.0",
    },
    "complaints_escalation_policy.md": {
        "document_owner": "Customer Operations",
        "classification": "Internal - Approved AI Knowledge Source",
        "review_frequency": "Quarterly",
        "version": "1.0",
    },
}


# ---------------------------------------------------------
# Load approved knowledge documents
# ---------------------------------------------------------

def load_documents() -> list[Document]:
    documents = []

    for file_path in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
        source_name = file_path.name

        if source_name not in DOCUMENT_METADATA:
            print(f"Skipping unapproved document: {source_name}")
            continue

        content = file_path.read_text(encoding="utf-8")

        metadata = {
            "source": source_name,
            **DOCUMENT_METADATA[source_name],
        }

        documents.append(
            Document(
                page_content=content,
                metadata=metadata,
            )
        )

    return documents


# ---------------------------------------------------------
# Split documents into chunks
# ---------------------------------------------------------

def split_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )

    return splitter.split_documents(documents)


# ---------------------------------------------------------
# Build Chroma vector database
# ---------------------------------------------------------

def build_vector_store(chunks: list[Document]) -> Chroma:
    embeddings = LocalSentenceTransformerEmbeddings(
        EMBEDDING_MODEL_NAME
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="nexacare_knowledge",
    )

    return vector_store


# ---------------------------------------------------------
# Main ingestion workflow
# ---------------------------------------------------------

def main():
    print("=" * 60)
    print("NexaCare Customer Support RAG Ingestion")
    print("=" * 60)

    print("\n[1/4] Loading approved knowledge documents...")

    documents = load_documents()

    print(f"Loaded documents: {len(documents)}")

    if not documents:
        raise RuntimeError(
            "No approved knowledge documents were found."
        )

    print("\n[2/4] Splitting documents into chunks...")

    chunks = split_documents(documents)

    print(f"Generated chunks: {len(chunks)}")

    print("\n[3/4] Generating local embeddings...")

    vector_store = build_vector_store(chunks)

    print("\n[4/4] Storing embeddings in ChromaDB...")

    print(f"Vector database: {CHROMA_DIR}")
    print(f"Collection: nexacare_knowledge")

    print("\n" + "=" * 60)
    print("RAG INGESTION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()