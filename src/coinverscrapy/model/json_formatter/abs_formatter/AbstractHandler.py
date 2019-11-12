from abc import abstractmethod
from src.coinverscrapy.model.json_formatter.abs_formatter.Json_Handler import Json_Handler


class AbstractHandler(Json_Handler):

    _next_handler: Json_Handler = None

    def set_next(self, handler: Json_Handler) -> Json_Handler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(self, request: any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None