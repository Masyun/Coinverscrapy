import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class ExcessWhitespaceHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        # Just in case there are unnecessary trailing spaces/newlines
        match = re.search('(\s+)', request)
        if match:
            mutated = re.sub(match.re, " ", request)
            request = mutated

        return super().handle(request)
