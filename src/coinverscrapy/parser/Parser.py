from coinverscrapy.model.proxy.IModuleProxy import IModuleProxy

class Scraper(IModuleProxy):

    def __init__(self, input_location):
        self.data = []

    def execute(self):
        # Main logic for parsing a list of PDF files
        print("Scraper.execute()")
        pass

    def extract_files_from_url(self):
        pass

    def store_extracted_files(self):
        pass

    def addOne(self, entry):
        self.data.append(entry)

    def getAll(self):
        return self.data.copy()
