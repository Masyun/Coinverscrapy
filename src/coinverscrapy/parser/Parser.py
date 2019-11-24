import json
import os

import camelot
import pandas as pd
from camelot.core import TableList

from src.coinverscrapy.model.formatting_handlers.CompetenceNewlineHandler import CompetenceNewlineHandler
from src.coinverscrapy.model.formatting_handlers.GenericListHandler import GenericListHandler
from src.coinverscrapy.model.formatting_handlers.NumericListEdgecaseHandler import NumericListEdgecaseHandler
from src.coinverscrapy.model.formatting_handlers.NumericListHandler import NumericListHandler
from src.coinverscrapy.model.formatting_handlers.RootHandler import RootHandler
from src.coinverscrapy.model.formatting_handlers.SubTaskHandler import SubTaskHandler
from src.coinverscrapy.model.json_container.JsonContainer import JsonContainer
from src.coinverscrapy.model.json_container.JsonEncoder import JsonEncoder
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
            .set_next(NumericListEdgecaseHandler())

    def execute(self):
        with os.scandir(self.location) as files:
            for file in files:
                table = self.formatContent(file)[0]

                print(type(table))
                json_obj = JsonContainer(table)

                result_json = json.dumps(json_obj.reprJSON(), cls=JsonEncoder, indent=4)

                print(result_json)
                print('\n\n')

        #         # tables[0].to_json('json/' + raw_name + '.json')
        #         # with open(('json/' + raw_name + '.json'), 'w') as json_file:
        #         #     json.dump(tables[0], json_file)

    def formatContent(self, file):
        tables = camelot.read_pdf(file.path, pages='all', split_text=True)

        directory_dict = os.path.split(
            file.path)  # directory_dict[0] for path to file, directory_dict[1] for file name
        raw_name = directory_dict[1][:-4]  # strip .pdf tag so we can replace it with .json

        for table in tables:  # Each table in the file
            fileline_count = 0

            for line in table.df[0]:
                table.df[0][fileline_count] = handle(self.root_handler,
                                                     line)  # Call the chain of handlers to handle each string in this file
                fileline_count += 1

        if tables.n > 1:
            tables = appendTables(tables)

        return tables


def appendTables(tables):
    frames = []
    for table in tables:
        frames.append(table.df)

    tables = pd.concat(frames, ignore_index=True)
    return tables



def handle(handler, row: str):
    return handler.handle(row)


def calculateAvg(total, count):
    return total / count
