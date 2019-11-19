import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class NumericListHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        match = re.search('([0-9]+\.([\s\n$]*([^0-9|a-z|A-Z|$])))', request)

        if match:
            numbering = ''
            mutated = ''
            try:
                # print(match.group(1))
                numbering = match.group(1).strip()
                mutated = re.sub(match.re, "", request)
                # print(mutated)
            except IndexError as ie:
                print(ie)
            finally:
                request = numbering + ' ' + mutated
                # print('\n\n\n{' + request + '}\n')

            # temp_line = re.sub(match.re, "", request)

        return super().handle(request)
