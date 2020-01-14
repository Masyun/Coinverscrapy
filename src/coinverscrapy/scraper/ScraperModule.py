import os
import sys

import requests

from src.coinverscrapy.model.template.ModuleTemplate import ModuleTemplate


class ScraperModule(ModuleTemplate):
    """
    Scraper proxy layer - responsible for handling any pre- and postconditions that may need to be met before executing the scraper itself.
    This is achieved by extending from the ModuleTemplate class, providing an initialize, run and finalize implementation.
    By calling the parent start() method, these implementations get executed in order.
    This class
    - creates the necessary folder in the filesystem
    - runs the scraper.execute method
    - then download the files by calling the scraper.get_data() containing all the urls


    ...

    Attributes
    ----------
    _scraper : Scraper
        an instance of a scraper
    output : str
        the path specifying the output directory of the downloaded pdfs

    Methods
    -------
    download_files(urls, output_folder)
        Does a GET request to the (pdf)urls from the scraper and saves the content to the ./pdfs/ directory
    handle_fs(folder_name)
        Creates the output ./pdfs/ folder in the project directory
    """

    def __init__(self, real_scraper, output):
        self._scraper = real_scraper
        self.output = output

    def initialize(self):
        handle_fs(self.output)

    def run(self):
        print("Scraping url for pdfs...")
        self._scraper.execute()

    def finalize(self):
        try:
            print_progress(0, len(self.output), prefix='Progress:', suffix='Complete', bar_length=50)
            download_files(self._scraper.get_data(), self.output)
        except IOError as ioe:
            print("error! -> {}".format(ioe))
            exit(0)


def download_files(urls, output_folder):
    total_filecount = len(urls)
    i = 0

    for url in urls:
        rq = requests.get(url)
        file_name = url[url.rfind('/'):]
        with open(output_folder + file_name, "w+b") as file:
            file.write(rq.content)
            file.close()
        i += 1
        print_progress(i, total_filecount, prefix='Progress:', suffix='Complete', bar_length=50)


def handle_fs(folder_name):
    # Hacky way to bypass windows' permission error when trying to create the required folders
    for retry in range(10):
        try:
            os.makedirs(folder_name)
            break
        except PermissionError as pe:
            print("{} Retrying folder creation".format(pe))
        except FileExistsError:
            break

    for file in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def print_progress(iteration, total, prefix='', suffix='', decimals=0, bar_length=100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n\n')
    sys.stdout.flush()
