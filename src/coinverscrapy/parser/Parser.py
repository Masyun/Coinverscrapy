import os

import camelot

from src.coinverscrapy.model.formatting_handlers.CompetenceNewlineHandler import CompetenceNewlineHandler
from src.coinverscrapy.model.formatting_handlers.GenericListHandler import GenericListHandler
from src.coinverscrapy.model.formatting_handlers.NumericListEdgecaseHandler import NumericListEdgecaseHandler
from src.coinverscrapy.model.formatting_handlers.NumericListHandler import NumericListHandler
from src.coinverscrapy.model.formatting_handlers.RootHandler import RootHandler
from src.coinverscrapy.model.formatting_handlers.SubTaskHandler import SubTaskHandler
from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy


# import tabula


class Parser(IModuleProxy):
    def __init__(self, input_location):
        self.location = input_location

        # Create the root handler
        self.root_handler = RootHandler()

        # Connect the chain of handlers
        self.setupHandlers()

    # Chain handlers to your hearts content
    def setupHandlers(self):
        self.root_handler \
            .set_next(GenericListHandler()) \
            .set_next(CompetenceNewlineHandler()) \
            .set_next(SubTaskHandler()) \
            .set_next(NumericListHandler()) \
            .set_next(NumericListEdgecaseHandler())

    def execute(self):
        # Main logic for checking errors during parsing of PDF files
        print("Parser.execute()")
        with os.scandir(self.location) as files:
            for file in files:
                tables = camelot.read_pdf(file.path, pages='all', split_text=True)

                # directory_dict = os.path.split(
                #     file.path)  # directory_dict[0] for path to file, directory_dict[1] for file name
                # raw_name = directory_dict[1][:-4]  # strip .pdf tag so we can replace it with .json

                i = 0
                report_sum = 0
                report_count = 0
                for table in tables:  # Each table in the file
                    report_sum += table.parsing_report['accuracy']
                    report_count += 1
                    fileline_count = 0

                    for line in table.df[0]:
                        table.df[0][fileline_count] = handle(self.root_handler, line)
                        fileline_count += 1

                    print(table.df[0])
                    i += 1
                    if i == 3:
                        print('AVERAGE ACCURACY: {}'.format(calculateAvg(report_sum, report_count)))
                        return

                # with open(('json/' + raw_name + '.json'), 'w') as json_file:
                #     json.dump(raw_json, json_file)


def handle(handler, row: str):
    return handler.handle(row)


def calculateAvg(total, count):
    return total / count
