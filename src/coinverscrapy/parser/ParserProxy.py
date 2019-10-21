from coinverscrapy.model.proxy.IModuleProxy import IModuleProxy
from coinverscrapy.model.template.IModuleTemplate import IModuleTemplate


class ParserProxy(IModuleProxy, IModuleTemplate):
    def __init__(self, real_parser):
        self.parser = real_parser

    def checkAccess(self):
        print("ParserProxy.checkAccess()")
        return True

    def execute(self):
        print("ParserProxy.execute()")
        if self.checkAccess():
            self.parser.execute()

    def initialize(self):
        print("ParserProxy.initialize()")
        pass

    def run(self):
        print("ParserProxy.run()")
        self.execute()

    def finalize(self):
        print("ParserProxy.finalize()")
        pass
