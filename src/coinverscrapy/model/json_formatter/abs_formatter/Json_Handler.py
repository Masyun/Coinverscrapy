from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


class Json_Handler(ABC):
    @abstractmethod
    def set_next(self, handler: Json_Handler) -> Json_Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass

