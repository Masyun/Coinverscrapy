import requests
from bs4 import BeautifulSoup as bs
from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy


class Scraper(IModuleProxy):
    def __init__(self, url):
        self.url = url
        self.data = {}

    def execute(self):
        # Main logic for scraping a webpage - this is where most, if not all logic should be contained
        print(f'Executing scraper on {self.get_url()}\n')
        self.data = extract_urls_from_url(self.url)

    def get_url(self):
        return self.url

    def get_data(self):
        return self.data


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
        try:
            if _FULLURL.endswith('.pdf'):
                pdf_urls.append(_FULLURL)
        except AttributeError as ae:
            print ("Supplied URL doesn't contain any PDF files! quitting")
            exit(0)
    return pdf_urls
