import os

from dotenv import load_dotenv
from openai import OpenAI

from app.models import DocumentPage, ProviderAnswer
from app.providers.base import LLMProvider

"""
openai_provider.py

Implementation of the LLM provider using the OpenAI API.

The provider receives a user question together with the
text extracted from a PDF and asks the language model
to answer using only the supplied document content.
"""

# Load environment variables from the local .env file.
load_dotenv()

# Generates document-based answers using an OpenAI model.
class OpenAIProvider(LLMProvider):
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")           # The API key and model name are read from environment variables
                                                        # so sensitive configuration is not stored inside the source code.

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY was not found. "
                "Add it to the .env file before starting the application."
            )

        # The model can be changed from .env without modifying the code.
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

        # Create the client used to communicate with the OpenAI API.
        self.client = OpenAI(api_key=api_key)

     # Answer a question using the text extracted from the document
    def answer(self, question: str, pages: list[DocumentPage]):
        # Combine the extracted pages while preserving page numbers.
        document_text_parts = []

        for page in pages:
            document_text_parts.append(f" Page {page.page_number} \n{page.text}")

        document_text = "\n\n".join(document_text_parts)

        # Give the model clear instructions not to invent information
        # that is not available in the uploaded document.
        instructions = (
            "You are a document question-answering assistant. "
            "Answer the user's question using only the supplied document. "
            "If the answer is not present in the document, clearly say so. "
            "Keep the response concise and mention the relevant page numbers."
        )

        user_input = (
            f"DOCUMENT:\n{document_text}\n\n"
            f"QUESTION:\n{question}"
        )

        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=user_input,
        )

        # For this first version, return all document pages as possible
        # sources. Precise source-page retrieval will be added later.
        source_pages = [page.page_number for page in pages]

        return ProviderAnswer(
            text=response.output_text,
            source_pages=source_pages,
        )