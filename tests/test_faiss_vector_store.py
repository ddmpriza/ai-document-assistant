from app.models import DocumentChunk, EmbeddedChunk
from app.services.faiss_vector_store import FaissVectorStore

def test_search_returns_most_similar_chunk():
    store = FaissVectorStore(dimension=2)

    chunk_a = DocumentChunk(chunk_id="chunk-a", page_number=1, text="Relevant text")

    chunk_b = DocumentChunk(chunk_id="chunk-b", page_number=2, text="Unrelated text")

    store.add([
        EmbeddedChunk(chunk=chunk_a, vector=(1.0, 0.0)),
        EmbeddedChunk(chunk=chunk_b, vector=(0.0, 1.0))
    ])

    results = store.search(query_vector=(1.0, 0.0), top_k=1, minimum_score=0.0)

    assert len(results) == 1
    assert results[0].chunk.chunk_id == "chunk-a"

def test_search_filters_low_similarity_results():
    store = FaissVectorStore(dimension=2)

    chunk = DocumentChunk(chunk_id="chunk-1", page_number=1, text="Unrelated text")

    store.add([EmbeddedChunk(chunk=chunk, vector=(0.0, 1.0))])

    results = store.search(query_vector=(1.0, 0.0), minimum_score=0.35)

    assert results == []

from app.services.in_memory_vector_store import InMemoryVectorStore


def test_faiss_matches_in_memory_results():
    chunk_a = DocumentChunk(chunk_id="chunk-a", page_number=1, text="Most relevant")

    chunk_b = DocumentChunk(chunk_id="chunk-b", page_number=2, text="Less relevant")

    embedded_chunks = [
        EmbeddedChunk(chunk=chunk_a, vector=(1.0, 0.0)),
        EmbeddedChunk(chunk=chunk_b,vector=(0.8, 0.2))
    ]

    in_memory_store = InMemoryVectorStore()
    in_memory_store.add(embedded_chunks)

    faiss_store = FaissVectorStore(dimension=2)
    faiss_store.add(embedded_chunks)

    query_vector = (1.0, 0.0)

    in_memory_results = in_memory_store.search(query_vector=query_vector, top_k=2, minimum_score=0.0)

    faiss_results = faiss_store.search(query_vector=query_vector, top_k=2, minimum_score=0.0)

    assert [result.chunk.chunk_id for result in faiss_results] == [result.chunk.chunk_id for result in in_memory_results]