import os

from dotenv import load_dotenv

from app.providers.base import LLMProvider
from app.providers.mock_provider import MockLLMProvider
from app.providers.ollama_provider import OllamaProvider
from app.providers.openai_provider import OpenAIProvider

"""
factory.py

Creates the LLM provider selected through environment configuration.

Keeping provider selection in one place prevents the API layer from
depending directly on OpenAI, Ollama, or the mock implementation.
"""

# Load configuration values from the local .env file
load_dotenv()

# Create the LLM provider based on the environment variable
# The provider is selected through the LLM_PROVIDER environment variable (mock, openai, or ollama)
def create_llm_provider():                                              # LLMProvider
    # Use the mock provider by default if no provider is configured.
    provider_name = os.getenv("LLM_PROVIDER", "mock").lower().strip()

    if provider_name == "mock":
        return MockLLMProvider()

    if provider_name == "openai":
        return OpenAIProvider()

    if provider_name == "ollama":
        return OllamaProvider()

    raise ValueError(
        f"Unsupported LLM provider: '{provider_name}'. "
        "Supported providers are: mock, openai, ollama."
    )