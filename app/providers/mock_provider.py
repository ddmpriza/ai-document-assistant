import re

from app.models import DocumentPage, ProviderAnswer
from app.providers.base import LLMProvider


class MockLLMProvider(LLMProvider):
    """
    A deterministic placeholder used before connecting a real LLM.

    It selects pages containing the most question keywords and returns
    excerpts. This validates upload, parsing, storage and citation flow.
    """

    def answer(
        self,
        question: str,
        pages: list[DocumentPage],
    ) -> ProviderAnswer:
        keywords = {
            word.lower()
            for word in re.findall(r"[A-Za-zΑ-Ωα-ω0-9]+", question)
            if len(word) > 3
        }

        ranked: list[tuple[int, DocumentPage]] = []

        for page in pages:
            lower_text = page.text.lower()
            score = sum(lower_text.count(keyword) for keyword in keywords)
            ranked.append((score, page))

        ranked.sort(key=lambda item: item[0], reverse=True)
        selected = [page for score, page in ranked if score > 0][:3]

        if not selected:
            selected = pages[:1]

        excerpts = []
        for page in selected:
            compact_text = " ".join(page.text.split())
            excerpts.append(
                f"Page {page.page_number}: {compact_text[:500]}"
            )

        return ProviderAnswer(
            text=(
                "Mock response based on the most relevant extracted pages. "
                "A real LLM provider will replace this component.\n\n"
                + "\n\n".join(excerpts)
            ),
            source_pages=[page.page_number for page in selected],
        )
