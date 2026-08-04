from uuid import uuid4

from app.models import DocumentChunk, DocumentPage, EmbeddedChunk, StoredDocument

"""
document_store.py

Stores uploaded documents in memory.
Temporary in-memory storage for uploaded documents.

This service stores uploaded documents during the lifetime
of the application, allowing users to upload a document
first and ask questions about it later.

"""
# Stores uploaded documents in memory during application runtime
class DocumentStore:
    # Dictionary used as an in-memory database.
    def __init__(self):
        self._documents: dict[str, StoredDocument] = {}

    # Store a new document and generate a unique identifier.
    def add(self, 
            filename: str, 
            pages: list[DocumentPage], 
            chunks: list[DocumentChunk],
            embedded_chunks: list[EmbeddedChunk]
        ):                                          # StoredDocument
        document = StoredDocument(
            document_id=str(uuid4()),               # Generate a unique ID so every uploaded document can be retrieved later
            filename=filename,
            pages=pages,
            chunks=chunks,
            embedded_chunks=embedded_chunks
        )
        # Save the document using its unique ID as the dictionary key
        self._documents[document.document_id] = document
        return document
    
    # Retrieve a document by its unique identifier
    def get(self, document_id: str) -> StoredDocument | None:       # Returns either a document or nothing
        return self._documents.get(document_id)
