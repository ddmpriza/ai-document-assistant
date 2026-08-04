from abc import ABC, abstractmethod                 

from app.models import DocumentChunk, EmbeddedChunk

"""
base.py

Defines the common interface for embedding providers.

Embedding providers convert text into numeric vectors that can later
be compared during semantic retrieval.
"""

# Common interface implemented by every embedding provider.
class EmbeddingProvider(ABC):
    # Generate one embedding vector for each document chunk.
    @abstractmethod                 # abstract method that must be implemented by subclasses
    def embed_chunks(self, chunks: list[DocumentChunk]):                                          # list[EmbeddedChunk]
        raise NotImplementedError

    # Generate an embedding vector for a user question.
    @abstractmethod                 # abstract method that must be implemented by subclasses 
    def embed_question(self, question: str):     # tuple[float, ...]
        raise NotImplementedError