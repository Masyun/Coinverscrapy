import requests
from bs4 import BeautifulSoup as bs
from coinverscrapy.model.proxy.IModuleProxy import IModuleProxy

class Scraper(IModuleProxy):

    def __init__(self, url):
        self.url = url
        self.data = {}

    def execute(self):
        # Main logic for scraping a webpage - this is where most, if not all logic should be contained
        print(f'Executing scraper on {self.get_url()}\n')
        self.data = extract_urls_from_url(self.url)
        pass

    def get_url(self):
        return self.url

    def get_data(self):
        return self.data

"""
function area
"""

def extract_urls_from_url(url):
    """extracts the links to all the PDF files on the webpage and maps them to a logical name(the pdf url)

    Args:
      url : string

    Returns:
      names_urls: map
    """
    r = requests.get(url)

    soup = bs(r.content, "html.parser")
    pdf_urls = []
    for i, link in enumerate(soup.findAll('a')):
        _FULLURL = link.get('href')
        if _FULLURL.endswith('.pdf'):
            pdf_urls.append(_FULLURL)

    return pdf_urls
