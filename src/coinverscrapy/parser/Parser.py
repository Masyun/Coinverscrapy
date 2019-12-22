import json
import logging
import os

import camelot
import jsonpickle
import pandas as pd

from src.coinverscrapy.model.formatting_handlers.CompetenceNewlineHandler import CompetenceNewlineHandler
from src.coinverscrapy.model.formatting_handlers.ExcessNewlineHandler import ExcessNewlineHandler
from src.coinverscrapy.model.formatting_handlers.ExcessWhitespaceHandler import ExcessWhitespaceHandler
from src.coinverscrapy.model.formatting_handlers.GenericListHandler import GenericListHandler
from src.coinverscrapy.model.formatting_handlers.SpecialcharReductionFormatter import SpecialcharReductionFormatter
from src.coinverscrapy.model.formatting_handlers.NumericListEdgecaseHandler import NumericListEdgecaseHandler
from src.coinverscrapy.model.formatting_handlers.NumericListHandler import NumericListHandler
from src.coinverscrapy.model.formatting_handlers.RootHandler import RootHandler
from src.coinverscrapy.model.formatting_handlers.SubTaskHandler import SubTaskHandler
from src.coinverscrapy.model.json_container.JsonContainer import JsonContainer
from src.coinverscrapy.model.proxy.ModuleExecutor import ModuleExecutor


class Parser(ModuleExecutor):
    """
    Parser module implementation extending from the ModuleProxy - which gives any of our 'modules' an execute method to keep the main logic neat and consistent.
    This parser does a couple things
    - Handle formatting of the contents of a parsed pdf(restoring errors that originated during the parsing process)
    - Keep track of certain parsing statistics
    - Handle any side-edgecases that may occur(multiple tables in one file)
    - Doing any checks to ensure proper output
    ...

    Attributes
    ----------
    data : list
        list of json_objects retrieved by parsing the pdf files
    location : str
        location to look at for pdfs to be parsed - /pdfs/ in the default case
    failures : list
        a list of all file names that could not have been parsed
    accuracy : int
        current average parsing accuracy(during a run)
    file_count : int
        total number of files found in the input_location

    Methods
    -------
    setup_formatting_handlers(self)
        Sets up the chain of formatting Handlers(model/formatting_handlers)
    """

    def __init__(self, input_location):
        self._data = []
        self._location = input_location
        self._failures = []
        self._accuracy = 0
        self._file_count = len(os.listdir(self._location))

        # Create the root handler
        self.root_handler = RootHandler()

        # Connect the chain of handlers
        self.setup_formatting_handlers()

        jsonpickle.set_preferred_backend('json')
        jsonpickle.set_encoder_options('json', ensure_ascii=False)

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
            .set_next(ExcessNewlineHandler()) \
            .set_next(ExcessWhitespaceHandler())

    def execute(self):
        print_progress(0, self._file_count, prefix='Progress:', suffix='Complete', bar_length=50)
        with os.scandir(self._location) as files:
            i = 0
            for file in files:
                table = self.format_content(file)
                if table is None:
                    self._failures.append(file.path)
                    i += 1
                    print_progress(i, self._file_count, prefix='Progress:', suffix='Complete', bar_length=50)
                    break
                else:
                    # Create the json container
                    json_container = JsonContainer(table[0], file.path) \
                        .format_unicode()

                valid = evaluate_output(json_container)
                if not valid:
                    self._failures.append(json_container.fileName)
                else:
                    # Encode the Json container object to a dict object
                    result_json_str = jsonpickle.encode(json_container, unpicklable=False)
                    result_json_obj = json.loads(result_json_str)
                    self._data.append(result_json_obj)

                i += 1
                print_progress(i, self._file_count, prefix='Progress:', suffix='Complete', bar_length=50)

    def format_content(self, file):
        try:
            tables = camelot.read_pdf(file.path, pages='all', split_text=True)
            self._accuracy += tables[0].parsing_report['accuracy']
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

    def get_average_accuracy(self):
        return round(self._accuracy / self._file_count, 2)

    def get_filecount(self):
        return self._file_count


def append_tables(tables):
    frames = []
    for table in tables:
        frames.append(table.df)

    tables = pd.concat(frames, ignore_index=True)
    return tables


def evaluate_output(container: JsonContainer):
    return container.titel is not None \
           and container.omschrijving is not None \
           and container.leerdoelen is not None


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
