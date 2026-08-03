from io import BytesIO

from pypdf import PdfReader

from app.models import DocumentPage

"""
pdf_parser.py

Utility functions for extracting text from PDF documents.

The current implementation supports digitally generated PDFs.
Support for scanned PDFs (OCR) can be added in a future version.
"""
# Extract the text of every page of the uploaded PDF
# Returns a list of DOcumentPage objects contrainf the page number and the extracted text
def extract_pdf_pages(content: bytes) -> list[DocumentPage]:
    try:
        reader = PdfReader(BytesIO(content))                # Create a PDF reader from the uploaded file stored in memory
    except Exception as exc:
        raise ValueError("The uploaded file could not be read as a PDF.") from exc

    pages: list[DocumentPage] = []

    # Extract the text of every page
    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
            # Ignore completely empty pages
        if text:
            pages.append(DocumentPage(page_number=index, text=text))

    # If no text was extracted, the document is probably scanned - not text found
    if not pages:
        raise ValueError(
            "No extractable text was found. Scanned PDFs will require OCR in a later version."
        )

    return pages
