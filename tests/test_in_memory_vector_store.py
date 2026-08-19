from app.models import DocumentChunk, EmbeddedChunk
from app.services.in_memory_vector_store import InMemoryVectorStore

def test_add_embedded_chunks():
    store = InMemoryVectorStore()

    chunk = DocumentChunk(chunk_id="chunk-1", page_number=1, text="Example text")
    embedded_chunk = EmbeddedChunk(chunk=chunk, vector=(1.0, 0.0))

    # Add one embedded chunk and verify that it is stored in memory
    store.add([embedded_chunk])

    assert len(store.embedded_chunks) == 1
    assert store.embedded_chunks[0] == embedded_chunk

def test_search_returns_most_similar_chunk():
    store = InMemoryVectorStore()

    chunk_a = DocumentChunk(chunk_id="chunk-a", page_number=1, text="Relevant text")
    chunk_b = DocumentChunk(chunk_id="chunk-b", page_number=2, text="Unrelated text")

    # Chunk A points in the same direction as the query vector
    # Chunk B is orthogonal and therefore has lower cosine similarity
    store.add([EmbeddedChunk(chunk=chunk_a, vector=(1.0, 0.0)), EmbeddedChunk(chunk=chunk_b, vector=(0.0, 1.0)), ])

    results = store.search(query_vector=(1.0, 0.0), top_k=1, minimum_score=0.0)

    assert len(results) == 1
    assert results[0].chunk.chunk_id == "chunk-a"


def test_search_filters_low_similarity_results():
    store = InMemoryVectorStore()
    chunk = DocumentChunk(chunk_id="chunk-1", page_number=1, text="Unrelated text")

    # An orthogonal vector has cosine similarity 0, so it should be removed by the minimum similarity threshold
    store.add([EmbeddedChunk(chunk=chunk, vector=(0.0, 1.0))])
    results = store.search(query_vector=(1.0, 0.0), minimum_score=0.35)

    assert results == []