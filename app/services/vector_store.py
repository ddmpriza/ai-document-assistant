from abc import ABC, abstractmethod

from app.models import EmbeddedChunk, RetrievalResult

"""
    Defines how vector embeddings are stored and searched.

    Concrete implementations may use in-memory search,
    FAISS, ChromaDB, or another vector database.
"""

class VectorStore(ABC):
    # Add embedded document chunks to the vector store.
    @abstractmethod                                         # Cannot create objects of the abstract class as long as it has abstract methods that have not been implemented
    def add(self, embedded_chunks: list[EmbeddedChunk]):
        raise NotImplementedError

    # Return the most relevant chunks for a query vector.
    @abstractmethod
    def search(self, query_vector: tuple[float, ...], top_k: int = 5, minimum_score: float = 0.35):                 # list[RetrievalResult]
        raise NotImplementedError