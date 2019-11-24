import re

from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler


class GenericListEdgecaseHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        # match = re.search('( \n[ ]*)', request)
        #
        # if match:
        #     mutated = ''
        #     try:
        #         mutated = re.sub(match.re, "", request).strip()
        #         print('\nMiddleNewlineHandler{' + mutated + '}\n\n')
        #         print(match)
        #     except IndexError as ie:
        #         print(ie)
        #     finally:
        #         request = '' + mutated
        #         request = request
        #
        # print('Mutated: ' + request)
        return super().handle(request)
