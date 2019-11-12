import os
import sys
import time

import requests

from src.coinverscrapy.model.template.IModuleTemplate import IModuleTemplate


class ScraperProxy(IModuleTemplate):
    def __init__(self, real_scraper, output):
        self.__scraper = real_scraper
        self.output = output

    def initialize(self):
        handle_fs(self.output)

    def run(self):
        self.__scraper.execute()

    def finalize(self):
        try:
            print_progress(0, len(self.output), prefix='Progress:', suffix='Complete', bar_length=50)
            download_files(self.__scraper.get_data(), self.output)
        except IOError as ioe:
            print("error! -> {}".format(ioe))
            print("\n\n")
            print("Faulty URL supplied! -> quitting execution")
            exit(0)


"""
function area
"""


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
        time.sleep(0.1)
        print_progress(i, total_filecount, prefix='Progress:', suffix='Complete', bar_length=50)


def handle_fs(folder_name):
    try:
        os.makedirs(folder_name)
    except FileExistsError:
        for file in os.listdir(folder_name):
            file_path = os.path.join(folder_name, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
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
        sys.stdout.write('\n')
    sys.stdout.flush()
