from abc import ABC, abstractmethod

from app.models import DocumentPage, ProviderAnswer


class LLMProvider(ABC):
    @abstractmethod
    def answer(
        self,
        question: str,
        pages: list[DocumentPage],
    ) -> ProviderAnswer:
        """Answer a question using the supplied document pages."""
        raise NotImplementedError
