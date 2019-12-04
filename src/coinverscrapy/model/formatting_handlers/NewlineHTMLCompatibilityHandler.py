import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class NewlineHTMLCompatibilityHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        # Just in case there are unnecessary trailing spaces/newlines
        request.rstrip()
        request.lstrip()

        match = re.search('((\n)+)', request)

        if match:
            mutated = re.sub(match.re, "<br>", request)
            request = mutated

        return super().handle(request)
