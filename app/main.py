from fastapi import FastAPI, File, HTTPException, UploadFile

from app.providers.factory import create_llm_provider
from app.models import ContextBlock
from app.models import EmbeddedChunk, RetrievalResult
from app.services.retrieval import retrieve_relevant_chunks
from app.services.text_chunker import create_chunks
from app.providers.embeddings.factory import create_embedding_provider 
from app.schemas import AskRequest, AskResponse, UploadResponse
from app.services.document_store import DocumentStore
from app.services.pdf_parser import extract_pdf_pages
from openai import RateLimitError
from app.services.in_memory_vector_store import InMemoryVectorStore

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

store = DocumentStore()                                 # DocumentStore: service for storing and retrieving documents
                                                        # All documents stored in same object in memory, no persistence across restarts
vector_stores: dict[str, InMemoryVectorStore] = {}      #  Separate vector store per document_id
llm_provider = create_llm_provider()                    # LLMProvider: implementation of the LLM provider for answering questions based on document content
embedding_provider = create_embedding_provider()        # EmbeddingProvider: service for creating embeddings of text

# Get endpoint for health check, returns a simple JSON response indicating the service is running
@app.get("/health")
def health_check():                                     # dict[str, str]
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
        
        # Split the extracted pages into smaller overlapping text sections.
        chunks = create_chunks(pages)

        # Convert every chunk into a semantic vector.
        embedded_chunks = embedding_provider.embed_chunks(chunks)

        # Store the document in the DocumentStore
        # Store both the original pages and the generated chunks
        # Returns a document object with metadata and pages
        document = store.add(
            filename=file.filename or "uploaded.pdf",
            pages=pages,
            chunks=chunks,
            embedded_chunks=embedded_chunks
        )              

        vector_store = InMemoryVectorStore()
        vector_store.add(embedded_chunks)

        vector_stores[document.document_id] = vector_store   
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return UploadResponse(
        document_id=document.document_id,
        filename=document.filename,
        page_count=len(document.pages),
        chunk_count=len(document.chunks),           # Count the number of chunks created from the document pages
        embedding_count=len(document.embedded_chunks),
        character_count=sum(len(page.text) for page in document.pages),
    )

# Post endpoint for asking a question about a previously uploaded document
@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest):                                # AskResponse
    document = store.get(request.document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")
    
    # Ask the LLM provider to answer the user's question
    # using the extracted context blocks of the document.
    try:
        # Convert the user's question into the same vector space
        # used for the stored document chunks.
        question_vector = embedding_provider.embed_question(request.question)

        vector_store = vector_stores.get(document.document_id)

        if vector_store is None:
            raise HTTPException(
                status_code=404,
                detail="Vector store not found for document.",
            )

        # Select only the chunks that are semantically closest to the user's question
        retrieval_results = vector_store.search(
            query_vector=question_vector,
            top_k=5,
            minimum_score=0.15
        )

        if not retrieval_results :
            return AskResponse(
                document_id=document.document_id,
                question=request.question,
                answer=(
                    "I cannot answer this question from the provided document."
                ),
                source_pages=[]
            )

        print("\nRetrieved Chunks:")
        for result in retrieval_results :
            print(result.chunk.chunk_id)
            print(result.chunk.page_number)
            print(result.chunk.text[:200])

        # Convert document-specific chunks into generic context blocks.
        context = []
        for result in retrieval_results:
            chunk = result.chunk

            context.append(
                ContextBlock(
                    text=chunk.text,
                    source_label=(
                        f"Page {chunk.page_number}, "
                        f"chunk {chunk.chunk_id}"
                    ),
                    page_number=chunk.page_number,
                )
            )

        # Send only the retrieved context to the selected LLM.
        llm_response = llm_provider.answer(
            question=request.question,
            context=context,
        )

    except RateLimitError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "The AI service is currently unavailable because "
                "the API quota has been exceeded or billing is not active."
            ),
        ) from exc

    return AskResponse(
        document_id=document.document_id,
        question=request.question,
        answer=llm_response.text,
        source_pages=llm_response.source_pages,
    )
