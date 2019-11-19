from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler
import re


class NewLineStartHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        match = re.search('e kandidaat kan', request)
        if match:
            mutated = re.sub(match.re, "De kandidaat kan", request)

            request = mutated

        return super().handle(request)
