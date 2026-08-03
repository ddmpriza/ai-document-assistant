from abc import ABC, abstractmethod

from app.models import DocumentPage, ProviderAnswer

"""
base.py

Base class for every language model provider.
Every provider should implement the answer() method.

"""
class LLMProvider:
    

    def answer(self, question, pages):
        raise NotImplementedError("Subclasses must implement answer().")
