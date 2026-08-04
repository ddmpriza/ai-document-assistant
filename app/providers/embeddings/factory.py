import os

from dotenv import load_dotenv

from app.providers.embeddings.base import EmbeddingProvider
from app.providers.embeddings.ollama_provider import (
    OllamaEmbeddingProvider,
)

"""
factory.py

Creates the embedding provider selected through environment configuration.

Keeping provider selection in one place prevents the API layer from
depending directly on Ollama or other embedding providers.
"""

load_dotenv()

# Create the configured embedding provider.
# Currently supported: ollama
def create_embedding_provider() -> EmbeddingProvider:
    # The provider is selected through the EMBEDDING_PROVIDER environment variable
    provider_name = os.getenv(
        "EMBEDDING_PROVIDER",
        "ollama"
    ).lower().strip()

    if provider_name == "ollama":
        return OllamaEmbeddingProvider()

    raise ValueError(
        f"Unsupported embedding provider: '{provider_name}'. "
        "Supported providers are: ollama."
    )