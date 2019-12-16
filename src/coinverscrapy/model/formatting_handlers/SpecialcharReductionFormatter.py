import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class SpecialcharReductionFormatter(AbstractHandler):
    def handle(self, request: str) -> str:
        # Just in case there are unnecessary trailing spaces/newlines
        request.rstrip()
        request.lstrip()

        match = re.search('((\s)+)', request)  # Look for any whitespace, newline or tab characters

        if match:
            mutated = re.sub(match.re, "\n", request)  # and replace them with one newline
            request = mutated

        return super().handle(request)
