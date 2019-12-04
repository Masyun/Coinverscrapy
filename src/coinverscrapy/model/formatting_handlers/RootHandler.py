from src.coinverscrapy.model.formatting_handlers.abs_handler.AbstractHandler import AbstractHandler

"""
Root handler is basically the same as an abstractHandler, except its instantializable
Used to start the chain of handlers
A future solution to this could be a Singleton root handler with self-subscribing handler implementation
"""
class RootHandler(AbstractHandler):
    def handle(self, request: str) -> str:
        return super().handle(request)
