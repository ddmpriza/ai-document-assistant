import pytest

from app.models import DocumentPage
from app.services.text_chunker import create_chunks

"""
    Verify that the text chunking functionality works correctly.

"""
# Verify that a short page creates a single chunk.
def test_short_page_creates_one_chunk():
    pages = [
        DocumentPage(
            page_number=1,
            text="This is a short document page.",
        )
    ]

    chunks = create_chunks(
        pages=pages,
        chunk_size=20,
        overlap=5
    )

    assert len(chunks) == 1
    assert chunks[0].page_number == 1
    assert chunks[0].text == "This is a short document page."

# Verify that a long page is split into overlapping chunks correctly.
def test_long_page_creates_overlapping_chunks():
    words = [f"word{i}" for i in range(20)]

    pages = [
        DocumentPage(
            page_number=2,
            text=" ".join(words),
        )
    ]


    chunks = create_chunks(
        pages=pages,
        chunk_size=10,
        overlap=2
    )

    assert len(chunks) == 3
    assert chunks[0].page_number == 2

    # The final two words of the first chunk should also
    # appear at the beginning of the second chunk.
    assert chunks[0].text.split()[-2:] == chunks[1].text.split()[:2]

# Verify that an invalid chunk configuration raises a ValueError.
def test_invalid_chunk_configuration():
    pages = [
        DocumentPage(
            page_number=1,
            text="Example text",
        )
    ]

    with pytest.raises(ValueError):
        create_chunks(
            pages=pages,
            chunk_size=10,
            overlap=10
    )