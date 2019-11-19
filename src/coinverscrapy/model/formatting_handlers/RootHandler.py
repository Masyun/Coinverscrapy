from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class RootHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        return super().handle(request)

