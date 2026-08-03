from io import BytesIO

from pypdf import PdfReader

from app.models import DocumentPage


def extract_pdf_pages(content: bytes) -> list[DocumentPage]:
    """Extract text from a digitally generated PDF, preserving page numbers."""
    try:
        reader = PdfReader(BytesIO(content))
    except Exception as exc:
        raise ValueError("The uploaded file could not be read as a PDF.") from exc

    pages: list[DocumentPage] = []

    for index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(DocumentPage(page_number=index, text=text))

    if not pages:
        raise ValueError(
            "No extractable text was found. Scanned PDFs will require OCR in a later version."
        )

    return pages
