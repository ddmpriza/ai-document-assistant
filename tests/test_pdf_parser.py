import pytest

from app.services.pdf_parser import extract_pdf_pages
"""
    Verify that invalid PDF data raises a ValueError.
"""

def test_invalid_pdf():
    with pytest.raises(ValueError):
        extract_pdf_pages(b"This is not a PDF")