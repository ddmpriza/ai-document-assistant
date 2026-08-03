import re                   # Regular Expressions

from app.models import DocumentPage, ProviderAnswer
from app.providers.base import LLMProvider

"""
mock_provider.py

Temporary implementation of an LLM provider.

This class does not use a real AI model.
Instead, it searches the document for pages that contain
the most keywords from the user's question and returns
their text as a mock response.

It allows us to test the complete application flow
before integrating OpenAI or another LLM.
"""
# Mock implementation of the LLM interface used during development
class MockLLMProvider(LLMProvider):
    def answer(
        self,
        question: str,
        pages: list[DocumentPage]
    ):
        # Extract significant keywords from the user's question
        keywords = {
            word.lower()
            for word in re.findall(r"[A-Za-zΑ-Ωα-ω0-9]+", question)
            if len(word) > 3                                        # Very short words are ignored to reduce noise
        }

        # Store each page together with its relevance score
        ranked = []

        # Calculate how relevant every page is by counting how many keywords appear in its text
        for page in pages:
            lower_text = page.text.lower()
            score = sum(lower_text.count(keyword) for keyword in keywords)
            ranked.append((score, page))

        # Sort pages from the highest score to the lowest
        ranked.sort(key=lambda item: item[0], reverse=True)
        # Keep only the three most relevant pages
        selected = [page for score, page in ranked if score > 0][:3]

        if not selected:
            selected = pages[:1]

        excerpts = []
        for page in selected:
            compact_text = " ".join(page.text.split())
            # Remove extra whitespace to create a cleaner response
            excerpts.append(
                f"Page {page.page_number}: {compact_text[:500]}"
            )

        # Return the simulated LLM response together with the pages used as supporting evidence
        return ProviderAnswer(
            text=(
                "Mock response based on the most relevant extracted pages. "
                "A real LLM provider will replace this component.\n\n"
                + "\n\n".join(excerpts)
            ),
            source_pages=[page.page_number for page in selected]
        )
