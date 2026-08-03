from fastapi import FastAPI, File, HTTPException, UploadFile

from app.providers.mock_provider import MockLLMProvider
from app.schemas import AskRequest, AskResponse, UploadResponse
from app.services.document_store import DocumentStore
from app.services.pdf_parser import extract_pdf_pages

"""
main.py

Entry point of the application.

This file:
- Creates the FastAPI application.
- Registers all API endpoints.
- Coordinates communication between the HTTP layer,
  the document storage service, and the LLM provider.

"""


# FastAPI: web framework for building APIs
# It connects the endpoints defined in this file to the web server and handles incoming requests and outgoing responses
app = FastAPI(
    title="AI Document Assistant",
    description="Upload a PDF and ask questions about its content.",
    version="0.1.0"
)

store = DocumentStore()                     # DocumentStore: service for storing and retrieving documents
                                            # All documents stored in same object in memory, no persistence across restarts
llm_provider = MockLLMProvider()            # MockLLMProvider: mock implementation of a language model provider for answering questions based on document content

# Get endpoint for health check, returns a simple JSON response indicating the service is running
@app.get("/health")
def health_check():                         # dict[str, str]
    return {"status": "ok"}

# Post endpoint for uploading a PDF document by the user
# /documents REST convention
# Response model is UploadResponse, which defines the structure of the response returned to the client 
# FastAPI uses this information to generate API documentation (Swagger UI)
@app.post("/documents", response_model=UploadResponse)
# FASTAPI automatically maps the uploaded file to the `file` parameter of type UploadFile
async def upload_document(file: UploadFile = File(...)):              # UploadResponse
    if file.content_type != "application/pdf":                        # if not PDF
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Read the uploaded PDF into memory - await for asynchronous operation
    content = await file.read()

    try:
        # Extract the text content from the PDF and return a list of pages
        pages = extract_pdf_pages(content)                  
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    # Store the document in the DocumentStore
    # Returns a document object with metadata and pages
    document = store.add(
        filename=file.filename or "uploaded.pdf",
        pages=pages
    )

    return UploadResponse(
        document_id=document.document_id,
        filename=document.filename,
        page_count=len(document.pages),
        character_count=sum(len(page.text) for page in document.pages),
    )

# Post endpoint for asking a question about a previously uploaded document
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):                                # AskResponse
    document = store.get(request.document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    
    # Ask the LLM provider to answer the user's question
    # using the extracted pages of the document.
    llm_response = llm_provider.answer(
        question=request.question,
        pages=document.pages,
    )

    return AskResponse(
        document_id=document.document_id,
        question=request.question,
        answer=llm_response.text,
        source_pages=llm_response.source_pages,
    )
