import os
import requests
import time

import sys
from coinverscrapy.model.template.IModuleTemplate import IModuleTemplate


class ScraperProxy(IModuleTemplate):
    def __init__(self, real_scraper, output):
        self.scraper = real_scraper
        self.output = '../../' + output

    def checkAccess(self):
        return True

    def initialize(self):
        if self.checkAccess():
            handle_fs(self.output)

    def run(self):
        self.scraper.execute()

    def finalize(self):
        download_files(self.scraper.get_data(), self.output)


"""
function area
"""

def download_files(urls, output_folder):
    total_filecount = len(urls)
    i = 0
    print_progress(0, total_filecount, prefix='Progress:', suffix='Complete', bar_length=50)
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
    print("Checking output directory(creating if it doesn't exist)...")
    print("output directory: " + folder_name)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print("Created directory")
    else:
        print("Output directory already populated! deleting...")
        for filename in os.listdir(folder_name):
                os.unlink(folder_name + '/' + filename)

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
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
