import os

from dotenv import load_dotenv
from ollama import Client, ResponseError

from app.models import DocumentChunk, EmbeddedChunk
from app.providers.embeddings.base import EmbeddingProvider

"""
Creates embeddings using a model running locally through Ollama.
"""

load_dotenv()

# Generates embeddings using Ollama's local embedding API.
class OllamaEmbeddingProvider(EmbeddingProvider):
    def __init__(
        self,
        client: Client | None = None,
        model: str | None = None
    ):
        # In the real application no client is passed, so a real Ollama client is created.
        # Tests can pass a fake client instead.
        self.client = client or Client(
            host="http://localhost:11434"
        )

        # Priority:
        # 1. Explicit model passed to the constructor
        # 2. OLLAMA_EMBEDDING_MODEL from .env
        # 3. Default model embeddinggemma
        self.model = model or os.getenv(
            "OLLAMA_EMBEDDING_MODEL",
            "embeddinggemma",
        )

    # Generate one embedding vector for each document chunk.
    def embed_chunks(self, chunks: list[DocumentChunk]):            # list[EmbeddedChunk]
        if not chunks:
            return []

        # Create a list of chunk texts to send to the Ollama embedding model.
        chunk_texts = [chunk.text   for chunk in chunks]

        try:
            # Ollama accepts a list of strings and returns one embedding vector for each supplied string.
            response = self.client.embed(
                model=self.model,
                input=chunk_texts,
            )

        except ResponseError as exc:
            raise RuntimeError(
                f"Ollama could not create document embeddings: {exc}"
            ) from exc

        # Extract the embedding vectors from the Ollama response.
        vectors = response["embeddings"]

        # Each chunk must have exactly one corresponding vector.
        if len(vectors) != len(chunks):
            raise RuntimeError(
                "The number of returned embeddings does not match "
                "the number of document chunks."
            )

        embedded_chunks: list[EmbeddedChunk] = []

        # Connect each document chunk with its corresponding embedding vector.
        for chunk, vector in zip(chunks, vectors):
            embedded_chunks.append(
                EmbeddedChunk(
                    chunk=chunk,
                    vector=tuple(vector),
                )
            )

        return embedded_chunks
    # Convert a user question into an embedding vector
    # The resulting vector will later be compared with the document chunk vectors during semantic retrieval.
    def embed_question(self, question: str):                        # tuple[float, ...]
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        try:
            response = self.client.embed(
                model=self.model,
                input=question,
            )

        except ResponseError as exc:
            raise RuntimeError(
                f"Ollama could not create the question embedding: {exc}"
            ) from exc

        return tuple(response["embeddings"][0])