import numpy as np
import faiss

from app.models import EmbeddedChunk
from app.services.vector_store import VectorStore
from app.models import EmbeddedChunk, RetrievalResult


class FaissVectorStore(VectorStore):
    def __init__(self, dimension: int):
        self.dimension = dimension                          # Preserves the length of the embedding vectors
        self.index = faiss.IndexFlatIP(dimension)           # Creates a FAISS index that performs an exact search using inner product
        self.embedded_chunks: list[EmbeddedChunk] = []      # Maintains the connection

    def add(self, embedded_chunks: list[EmbeddedChunk]):
        vectors = np.array(                                 # Creates table 2 vectors × 2 dimensions
            [chunk.vector for chunk in embedded_chunks],
            dtype="float32"
        )

        faiss.normalize_L2(vectors)                         #  Make length 1

        self.index.add(vectors)

        self.embedded_chunks.extend(embedded_chunks)

    def search(self, query_vector: tuple[float, ...], top_k: int = 5, minimum_score: float = 0.35):
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query = np.array([query_vector], dtype="float32")

        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, top_k)               # Ask for 5 nearest

        results: list[RetrievalResult] = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            if score < minimum_score:
                continue

            results.append(
                RetrievalResult(
                    chunk=self.embedded_chunks[index].chunk,
                    score=float(score),
                )
            )

        return results