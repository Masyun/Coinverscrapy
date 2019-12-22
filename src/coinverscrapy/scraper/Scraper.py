import requests
from bs4 import BeautifulSoup as bs
from src.coinverscrapy.model.proxy.ModuleExecutor import ModuleExecutor


class Scraper(ModuleExecutor):
    """
    Parser module implementation extending from the ModuleProxy - which gives any of our 'modules' an execute method to keep the main logic neat and consistent.


    ...

    Attributes
    ----------
    url : str
        the url passed in by the user - to be scraped for pdf files(or links, rather)
    data : list
        a list containing all the urls of the pdf files - extracted from the html

    Methods
    -------
    extract_urls_from_url(url: str)
        populates the data field with urls of the pdf files from the given url
    """

    def __init__(self, url):
        self.url = url
        self.data = []

    def execute(self):
        # Main logic for scraping a webpage - this is where most, if not all logic should be contained
        self.data = extract_urls_from_url(self.get_url())

    def get_url(self):
        return self.url

    def get_data(self):
        return self.data


def extract_urls_from_url(url):
    """extracts the links to all the PDF files on the webpage and maps them to a logical name(the pdf url)

    Args:
      url : string

    Returns:
      names_urls: list
    """
    r = requests.get(url)

    soup = bs(r.content, "html.parser")
    pdf_urls = []
    for i, link in enumerate(soup.findAll('a')):
        _FULLURL = link.get('href')
        try:
            if _FULLURL.endswith('.pdf'):
                pdf_urls.append(_FULLURL)
        except AttributeError:
            print("Supplied URL doesn't contain any PDF files! quitting")
            exit(0)
    return pdf_urls
