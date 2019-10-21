import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from coinverscrapy.model.proxy.IModuleProxy import IModuleProxy


class Scraper(IModuleProxy):

    def __init__(self, URL):
        self.data = []
        self.URL = URL
        self.addOne(1234)
        self.addOne(123)
        self.addOne(143)
        self.addOne(1545)

    def execute(self):
        # Main logic for scraping a webpage - this is where most, if not all logic should be contained
        print("Scraper.execute()")
        print("Provided URL: " + self.URL)
        for entry in range(len(self.data)):
            print(self.data[entry])

        pass

    def extract_files_from_url(self, url):
        pass

    def store_extracted_files(self, output_folder):
        pass

    def addOne(self, entry):
        self.data.append(entry)

    def getAll(self):
        return self.data.copy()
