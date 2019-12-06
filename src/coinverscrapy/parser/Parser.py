import os

import camelot
import jsonpickle
import pandas as pd

from src.coinverscrapy.model.formatting_handlers.CompetenceNewlineHandler import CompetenceNewlineHandler
from src.coinverscrapy.model.formatting_handlers.GenericListHandler import GenericListHandler
from src.coinverscrapy.model.formatting_handlers.NewlineHTMLCompatibilityHandler import NewlineHTMLCompatibilityHandler
from src.coinverscrapy.model.formatting_handlers.NumericListEdgecaseHandler import NumericListEdgecaseHandler
from src.coinverscrapy.model.formatting_handlers.NumericListHandler import NumericListHandler
from src.coinverscrapy.model.formatting_handlers.RootHandler import RootHandler
from src.coinverscrapy.model.formatting_handlers.SubTaskHandler import SubTaskHandler
from src.coinverscrapy.model.json_container.JsonContainer import JsonContainer
from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy


class Parser(IModuleProxy):
    def __init__(self, input_location):
        self._data = []
        self._location = input_location
        self._failures = []

        # Create the root handler
        self.root_handler = RootHandler()

        # Connect the chain of handlers
        self.setup_formatting_handlers()

    def setup_formatting_handlers(self):
        """
        Future implementation of this should be self subscribing handlers with a singleton root handler
        :return:
        """
        self.root_handler \
            .set_next(GenericListHandler()) \
            .set_next(CompetenceNewlineHandler()) \
            .set_next(SubTaskHandler()) \
            .set_next(NumericListHandler()) \
            .set_next(NumericListEdgecaseHandler()) \
            .set_next(NewlineHTMLCompatibilityHandler())\

    def execute(self):
        file_count = len(os.listdir(self._location))
        print_progress(0, file_count, prefix='Progress:', suffix='Complete', bar_length=50)
        with os.scandir(self._location) as files:
            i = 0
            for file in files:
                table = self.format_content(file)
                if table is None:
                    self._failures.append(file.path)
                    break

                # Create the json container
                json_obj = JsonContainer(table[0], file.path)
                if json_obj.leerdoelen is None:
                    self._failures.append(json_obj.fileName)
                # Encode the Json container object to a valid json structure
                result_json = jsonpickle.encode(json_obj, unpicklable=False)

                self._data.append(result_json)
                i += 1
                print_progress(i, file_count, prefix='Progress:', suffix='Complete', bar_length=50)

    def format_content(self, file):
        try:
            tables = camelot.read_pdf(file.path, pages='all', split_text=True)
        except IndexError:
            return None

        for table in tables:  # Each table in the file
            fileline_count = 0

            for line in table.df[0]:
                table.df[0][fileline_count] = self.handle_format(
                    line)  # Call the chain of handlers to handle each string in this file/pdf table
                fileline_count += 1

        if tables.n > 1:
            tables = append_tables(tables)

        return tables

    def handle_format(self, row: str):
        return self.root_handler.handle(row)

    def get_data(self):
        return self._data

    def get_failures(self):
        return self._failures


def append_tables(tables):
    frames = []
    for table in tables:
        frames.append(table.df)

    tables = pd.concat(frames, ignore_index=True)
    return tables


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
    import sys
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n\n')
    sys.stdout.flush()
