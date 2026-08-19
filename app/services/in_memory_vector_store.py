from app.models import EmbeddedChunk, RetrievalResult
from app.services.vector_store import VectorStore
from app.services.retrieval import cosine_similarity


class InMemoryVectorStore(VectorStore):
    def __init__(self):
        self.embedded_chunks: list[EmbeddedChunk] = []

    def add(self,embedded_chunks: list[EmbeddedChunk]):
        self.embedded_chunks.extend(embedded_chunks)

    def search(self, query_vector: tuple[float, ...], top_k: int = 5, minimum_score: float = 0.35):                                                      # list[RetrievalResult]
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        ranked_results: list[RetrievalResult] = []

        for embedded_chunk in self.embedded_chunks:
            score = cosine_similarity(query_vector, embedded_chunk.vector)

            if score >= minimum_score:
                ranked_results.append(RetrievalResult(chunk=embedded_chunk.chunk,score=score))

        ranked_results.sort(
            key=lambda result: result.score,
            reverse=True
        )

        return ranked_results[:top_k]