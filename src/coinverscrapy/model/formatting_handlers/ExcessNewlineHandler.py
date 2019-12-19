from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class ExcessNewlineHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        # Just in case there are unnecessary trailing spaces/newlines

        mutated = request.replace('\n', '')
        request = mutated

        return super().handle(request)
