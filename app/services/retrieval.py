import math

from app.models import EmbeddedChunk, RetrievalResult

"""
retrieval.py

Finds the document chunks that are most semantically similar
to a user's question.

The current implementation uses cosine similarity directly
in Python. A faster vector index such as FAISS can replace it later.
"""
# Measure how similar two vectors are based on their direction.
# The result usually ranges from -1 to 1, with 1 very similar, 0 unrelated, and -1 opposite directions.
def cosine_similarity(vector_a: tuple[float, ...], vector_b: tuple[float, ...]):                                  # float
    if len(vector_a) != len(vector_b):
        raise ValueError(
            "Vectors must have the same dimensions."
        )

    # Calculate the dot product and magnitudes of the two vectors.
    dot_product = sum(
        value_a * value_b
        for value_a, value_b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(value * value for value in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(value * value for value in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        raise ValueError(
            "Cosine similarity cannot be calculated for a zero vector."
        )

    return dot_product / (magnitude_a * magnitude_b)

# Find the document chunks that are most semantically similar to a user's question.
def retrieve_relevant_chunks(
    question_vector: tuple[float, ...],
    embedded_chunks: list[EmbeddedChunk],
    top_k: int = 5,
    minimum_score: float = 0.35
):                                                                  # list[RetrievalResult]
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero.")

    ranked_results: list[RetrievalResult] = []

    # Calculate the similarity score between the question vector and each document chunk vector.
    for embedded_chunk in embedded_chunks:
        score = cosine_similarity(question_vector, embedded_chunk.vector)

        # Keep track of the similarity score and the corresponding document chunk.
        if score >= minimum_score:
            ranked_results.append(
                RetrievalResult(
                    chunk=embedded_chunk.chunk,
                    score=score,
                )
            )


    # Highest similarity scores should appear first.
    ranked_results.sort(
        key=lambda result: result.score,
        reverse=True
    )

    return ranked_results[:top_k]