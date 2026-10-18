from pathlib import Path

from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = PROJECT_ROOT / "chroma_db"


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "nexacare_knowledge"


# ---------------------------------------------------------
# Local embedding implementation
# ---------------------------------------------------------

class LocalSentenceTransformerEmbeddings(Embeddings):
    """
    Generates embeddings locally using Sentence Transformers.
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
# Load vector database
# ---------------------------------------------------------

def get_vector_store() -> Chroma:
    """
    Connects to the existing NexaCare ChromaDB collection.
    """

    embeddings = LocalSentenceTransformerEmbeddings(
        EMBEDDING_MODEL_NAME
    )

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    return vector_store


# ---------------------------------------------------------
# Retrieve relevant documents
# ---------------------------------------------------------

def retrieve_documents(
    query: str,
    k: int = 4,
):
    """
    Retrieve the most relevant knowledge-base chunks.
    """

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=k,
    )

    return documents


# ---------------------------------------------------------
# Display retrieval results
# ---------------------------------------------------------

def main():
    query = input("\nEnter your customer question: ").strip()

    if not query:
        print("No question provided.")
        return

    print("\nSearching NexaCare knowledge base...\n")

    documents = retrieve_documents(query)

    if not documents:
        print("No relevant information found.")
        return

    print("=" * 70)
    print(f"Retrieved {len(documents)} knowledge chunks")
    print("=" * 70)

    for index, document in enumerate(documents, start=1):

        print(f"\nRESULT {index}")
        print("-" * 70)

        print("Source:", document.metadata.get("source"))
        print(
            "Classification:",
            document.metadata.get("classification"),
        )
        print(
            "Document Owner:",
            document.metadata.get("document_owner"),
        )
        print(
            "Version:",
            document.metadata.get("version"),
        )

        print("\nContent:")
        print(document.page_content[:1000])

        print()


if __name__ == "__main__":
    main()