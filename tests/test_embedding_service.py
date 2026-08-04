from app.models import DocumentChunk
from app.providers.embeddings.ollama_provider import OllamaEmbeddingProvider

"""
    Verify that the embedding service can embed text chunks.
    This test checks that the embedding service correctly converts text chunks into semantic vectors.
"""

# A fake embedding client that simulates the behavior of the Ollama client for testing purposes.
class FakeEmbeddingClient:
    # Simulates the behavior of the Ollama client for testing purposes.
    def embed(self, model, input):
        if isinstance(input, str):
            return {"embeddings": [[0.1, 0.2, 0.3]]}

        return {
            "embeddings": [[float(index), 0.2, 0.3]     for index, _ in enumerate(input)]
        }

# Test that the embedding service can embed document chunks correctly.
def test_embed_chunks():
    service = OllamaEmbeddingProvider(
        client=FakeEmbeddingClient(),
        model="test-model"
    )

    chunks = [
        DocumentChunk(
            chunk_id="chunk-1",
            page_number=1,
            text="Transformers use attention."
        ),
        DocumentChunk(
            chunk_id="chunk-2",
            page_number=2,
            text="Embeddings represent semantic meaning."
        ),
    ]

    embedded_chunks = service.embed_chunks(chunks)

    assert len(embedded_chunks) == 2
    assert embedded_chunks[0].chunk.chunk_id == "chunk-1"
    assert embedded_chunks[0].vector == (0.0, 0.2, 0.3)

# Test that the embedding service can embed a question correctly.
def test_embed_question():
    service = OllamaEmbeddingProvider(
        client=FakeEmbeddingClient(),
        model="test-model",
    )

    vector = service.embed_question(
        "What is self-attention?"
    )

    assert vector == (0.1, 0.2, 0.3)