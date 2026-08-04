from dataclasses import dataclass           # Create data classes for the document and its pages

"""
models.py

This file defines the core data models used by the application.

These classes represent the main objects that move through the system:
- A single page extracted from a document.
- A stored document.
- A response returned by the LLM provider.
- A smaller text section created from a document page.
"""
# Represents a single page extracted from a PDF document, including its page number and text content
@dataclass(frozen=True)                     # immutable data class for a page of a document
class DocumentPage:
    page_number: int
    text: str

# Represents a smaller text section created from a document page
# The page number is preserved so retrieved information can later be linked back to its original source.
@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    page_number: int
    text: str
# Represents a piece of context supplied to an LLM.
# The provider does not need to know whether the content came from a PDF, OCR, a database, or another source.
@dataclass(frozen=True)
class ContextBlock:
    text: str
    source_label: str
    page_number: int | None = None  # Optional page number to indicate the source of the context block, if applicable

# Connects a document chunk with its numeric embedding vector.
# The vector represents the semantic meaning of the chunk and will later be used for similarity search.
@dataclass(frozen=True)
class EmbeddedChunk:
    chunk: DocumentChunk
    vector: tuple[float, ...]

# Represents a document stored in the DocumentStore, including its metadata and the list of pages extracted from the PDF
@dataclass(frozen=True)                     # immutable data class for a stored document, contains metadata and a list of pages
class StoredDocument:
    document_id: str
    filename: str
    pages: list[DocumentPage]
    chunks: list[DocumentChunk]
    embedded_chunks: list[EmbeddedChunk]    # Keeps the connection between the document chunks and their corresponding numeric embedding vectors for semantic search

# Represents the answer provided by the LLM provider, including the answer text and the source pages used to generate the answer
@dataclass(frozen=True)                     # immutable data class for the answer provided by the LLM provider, the answer text and the source pages used to generate the answer
class ProviderAnswer:
    text: str
    source_pages: list[int]

# Represents a document chunk along with its similarity score to a given question vector.
@dataclass(frozen=True)
class RetrievalResult:
    chunk: DocumentChunk
    score: float