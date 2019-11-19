import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class NumericListEdgecaseHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        match = re.search('([0-9]+\.$)', request)

        if match:
            numbering = ''
            mutated = ''
            try:
                numbering = match.group(1).strip()
                mutated = re.sub(match.re, "", request)
            except IndexError as ie:
                print(ie)
            finally:
                request = numbering + ' ' + mutated
                request = request.rstrip()
                # print('\n{' + request + '}\n\n')

        return super().handle(request)
