import os

from dotenv import load_dotenv
from ollama import Client, ResponseError

from app.models import DocumentPage, ProviderAnswer
from app.providers.base import LLMProvider

"""
ollama_provider.py

Implementation of the LLM provider using a locally running Ollama model.

The document content remains on the local machine and no external
AI API key or paid service is required.
"""

load_dotenv()               # Load environment variables from the local .env file.

# Generates document-based answers using a local Ollama model.
class OllamaProvider(LLMProvider):
    def __init__(self):
        # The model name can be changed through the .env file.
        self.model = os.getenv("OLLAMA_MODEL", "gemma3:1b")

        # Ollama runs a local HTTP service on port 11434.
        self.client = Client(host="http://localhost:11434")

    # Answer a question using the text extracted from the document
    def answer(self, question: str, pages: list[DocumentPage]):

        # Combine all extracted pages while preserving their page numbers.
        document_parts = []

        for page in pages:
            document_parts.append(
                f"Page {page.page_number}\n{page.text}"
            )

        document_text = "\n\n".join(document_parts)

        system_message = (
            "You are a document question-answering assistant. "
            "Answer the user's question using only the supplied document. "
            "If the answer is not available in the document, say so clearly. "
            "Keep the answer concise and mention relevant page numbers."
        )

        user_message = (
            f"DOCUMENT:\n{document_text}\n\n"
            f"QUESTION:\n{question}"
        )

        try:
            response = self.client.chat(                    # Send the system and user messages to the Ollama model for processing
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_message,
                    },
                    {
                        "role": "user",
                        "content": user_message,
                    },
                ],
            )

        except ResponseError as exc:
            raise RuntimeError(
                f"Ollama could not generate an answer: {exc}"
            ) from exc

        answer_text = response["message"]["content"]        # Extract the answer text from the Ollama model's response

        # Return the answer along with the page numbers of the source pages used to generate the answer
        return ProviderAnswer(
            text=answer_text,
            source_pages=[
                page.page_number
                for page in pages
            ]
        )