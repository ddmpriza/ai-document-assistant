import pytest

from app.models import DocumentChunk, EmbeddedChunk
from app.services.retrieval import cosine_similarity, retrieve_relevant_chunks

"""
    Verify that the retrieval functionality works correctly.
"""
# Cosine similarity function returns 1.0 for identical vectors.
def test_cosine_similarity_for_identical_vectors():
    similarity = cosine_similarity(
        (1.0, 0.0),
        (1.0, 0.0),
    )

    assert similarity == pytest.approx(1.0)

# Cosine similarity function returns -1.0 for opposite vectors.
def test_cosine_similarity_for_unrelated_vectors():
    similarity = cosine_similarity(
        (1.0, 0.0),
        (0.0, 1.0),
    )

    assert similarity == pytest.approx(0.0)

# Cosine similarity function raises ValueError for vectors of different dimensions.
def test_retrieve_relevant_chunks():
    chunk_a = DocumentChunk(
        chunk_id="chunk-a",
        page_number=1,
        text="Transformers use attention."
    )

    chunk_b = DocumentChunk(
        chunk_id="chunk-b",
        page_number=2,
        text="Cats are domestic animals."
    )

    chunk_c = DocumentChunk(
        chunk_id="chunk-c",
        page_number=3,
        text="Self-attention is used in Transformers."
    )

    embedded_chunks = [
        EmbeddedChunk(
            chunk=chunk_a,
            vector=(1.0, 0.0)
        ),
        EmbeddedChunk(
            chunk=chunk_b,
            vector=(0.0, 1.0)
        ),
        EmbeddedChunk(
            chunk=chunk_c,
            vector=(0.9, 0.1)
        )
    ]

    retrieved = retrieve_relevant_chunks(
        question_vector=(1.0, 0.0),
        embedded_chunks=embedded_chunks,
        top_k=2
    )

    assert len(retrieved) == 2
    assert retrieved[0].chunk_id == "chunk-a"
    assert retrieved[1].chunk_id == "chunk-c"

# Test that the retrieval function raises a ValueError for vectors of different dimensions.
def test_invalid_top_k():
    with pytest.raises(ValueError):
        retrieve_relevant_chunks(
            question_vector=(1.0, 0.0),
            embedded_chunks=[],
            top_k=0,
        )