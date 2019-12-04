from abc import abstractmethod
from src.coinverscrapy.model.formatting_handlers.abs_handler.Handler import Handler

"""
Minimal implementation of a handler which just passes the request to the next handler
Any Handler extending from this, should be responsible for handling one task in the string formatting chain
"""


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(self, request: str) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return request
