from uuid import uuid4

from app.models import DocumentPage, StoredDocument


class DocumentStore:
    """Temporary in-memory document store for the first MVP."""

    def __init__(self) -> None:
        self._documents: dict[str, StoredDocument] = {}

    def add(self, filename: str, pages: list[DocumentPage]) -> StoredDocument:
        document = StoredDocument(
            document_id=str(uuid4()),
            filename=filename,
            pages=pages,
        )
        self._documents[document.document_id] = document
        return document

    def get(self, document_id: str) -> StoredDocument | None:
        return self._documents.get(document_id)
