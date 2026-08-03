from pydantic import BaseModel, Field       # Define Pydantic models for request and response validation (JSON)

"""
schemas.py

Defines the request and response models used by the API.

These schemas describe the JSON exchanged between
clients and the FastAPI application.

They are also used to generate automatic API documentation
(Swagger/OpenAPI) and validate incoming data.
"""
# Response returned after a document is uploaded.
class UploadResponse(BaseModel):
    document_id: str
    filename: str
    page_count: int
    character_count: int

# JSON sent by the client when asking a question.
class AskRequest(BaseModel):
    document_id: str
    # Validate the question length before the endpoint is executed.
    question: str = Field(min_length=3, max_length=500)     

# JSON returned after the LLM answers the question.
class AskResponse(BaseModel):
    document_id: str
    question: str
    answer: str
    source_pages: list[int]
