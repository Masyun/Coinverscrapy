import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class TaskHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        match = re.search('D\nD', request)
        if match:
            mutated = re.sub(match.re, "D", request)

            request = mutated

        return super().handle(request)