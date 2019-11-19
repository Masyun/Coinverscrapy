import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class ListFormatHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        is_task_match = re.search('Taak: \n', request)
        # match = re.search('(\\w+ \no[( )\n]*)+', request)

        if is_task_match:
            match = re.search('\\w+\\s*\\no( )*(\\n)*', request)
            if match:
                list_vals = re.sub(' \no ', "", request).splitlines(True)
                list_vals.pop()  # Pop off the pesky final '0' char from the list because regex is error prone doing this

                mutated = ''.join(list_vals)

                request = mutated

        return super().handle(request)
