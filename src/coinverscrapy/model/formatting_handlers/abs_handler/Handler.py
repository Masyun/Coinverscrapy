from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

"""
Root Abstract Handler class. Defines de base methods without implementation of our concrete handlers
"""


class Handler(ABC):

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass
