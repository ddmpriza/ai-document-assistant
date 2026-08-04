from app.models import DocumentPage
from app.services.document_store import DocumentStore

"""
    Verify that a document can be stored successfully.
    This test checks that a document can be added to the DocumentStore and that its properties are correctly set.
    
"""
def test_add_document():
    store = DocumentStore()

    document = store.add(
        filename="example.pdf",
        pages=[
            DocumentPage(
                page_number=1,
                text="Hello World"
            )
        ],
        chunks=[],
        embedded_chunks=[]
    )

    assert document.filename == "example.pdf"

    assert len(document.pages) == 1

    assert document.pages[0].text == "Hello World"

"""
    Verify that a stored document can be retrieved using its id.
"""
def test_get_document():
    store = DocumentStore()

    document = store.add(
        filename="example.pdf",
        pages=[
            DocumentPage(
                page_number=1,
                text="Hello"
            )
        ],
        chunks=[],
        embedded_chunks=[]
    )

    retrieved = store.get(document.document_id)

    assert retrieved is not None

    assert retrieved.document_id == document.document_id

"""
    Verify that unknown document ids should return None.
"""
def test_get_unknown_document():
    store = DocumentStore()

    assert store.get("unknown-id") is None