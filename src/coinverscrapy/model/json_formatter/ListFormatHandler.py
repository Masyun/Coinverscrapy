from src.coinverscrapy.model.json_formatter.abs_formatter.AbstractHandler import AbstractHandler


class ListFormatHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        if len(request) > 0:
            print('ListFormatHandler: {}'.format(request))

        return super().handle(request)
