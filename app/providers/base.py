from abc import ABC, abstractmethod

from app.models import ContextBlock, ProviderAnswer

"""
base.py

Base class for every language model provider.
Every provider should implement the answer() method.

"""
class LLMProvider:
    def answer(self, question, context_blocks):                     # ProviderAnswer
        raise NotImplementedError("Subclasses must implement answer().")
