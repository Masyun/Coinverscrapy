from coinverscrapy.model.proxy.IModuleProxy import IModuleProxy
from coinverscrapy.model.template.IModuleTemplate import IModuleTemplate


class ScraperProxy(IModuleProxy, IModuleTemplate):
    def __init__(self, real_scraper):
        self.scraper = real_scraper

    def checkAccess(self):
        print("ScraperProxy.checkAccess()")
        return True

    def execute(self):
        print("ScraperProxy.execute()")
        if self.checkAccess():
            self.scraper.execute()

    def initialize(self):
        print("ScraperProxy.initialize()")
        pass

    def run(self):
        print("ScraperProxy.run()")
        self.execute()

    def finalize(self):
        print("ScraperProxy.finalize()")
        pass
