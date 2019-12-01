import json
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
        self.location = input_location

        # Create the root handler
        self.root_handler = RootHandler()

        # Connect the chain of handlers
        self.setupFormattingHandlers()

    def setupFormattingHandlers(self):
        self.root_handler \
            .set_next(GenericListHandler()) \
            .set_next(CompetenceNewlineHandler()) \
            .set_next(SubTaskHandler()) \
            .set_next(NumericListHandler()) \
            .set_next(NumericListEdgecaseHandler()) \
            .set_next(NewlineHTMLCompatibilityHandler())

    def execute(self):
        with os.scandir(self.location) as files:
            for file in files:
                table = self.format_content(file)[0]
                # print(table.df[0])

                # Create the json container
                json_obj = JsonContainer(table)
                # Encode the Json container object to a valid json structure
                result_json = jsonpickle.encode(json_obj, unpicklable=False)

                print('Json:\n{}'.format(result_json, indent=4))
                print('\n\n')

                # result_json = json.dumps(json_obj.reprJSON(), cls=JsonEncoder, indent=4)
        #         # tables[0].to_json('json/' + raw_name + '.json')
        #         # with open(('json/' + raw_name + '.json'), 'w') as json_file:
        #         #     json.dump(tables[0], json_file)

    def format_content(self, file):
        tables = camelot.read_pdf(file.path, pages='all', split_text=True)

        directory_dict = os.path.split(
            file.path)  # directory_dict[0] for path to file, directory_dict[1] for file name
        raw_name = directory_dict[1][:-4]  # strip .pdf tag so we can replace it with .json

        for table in tables:  # Each table in the file
            fileline_count = 0

            for line in table.df[0]:
                table.df[0][fileline_count] = self.handle_format(
                    line)  # Call the chain of handlers to handle each string in this file
                fileline_count += 1

        if tables.n > 1:
            tables = append_tables(tables)

        return tables

    def handle_format(self, row: str):
        return self.root_handler.handle(row)


def append_tables(tables):
    frames = []
    for table in tables:
        frames.append(table.df)

    tables = pd.concat(frames, ignore_index=True)
    return tables


def calculateAvg(total, count):
    return total / count
