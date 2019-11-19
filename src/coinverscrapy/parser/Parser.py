import os

import camelot

from src.coinverscrapy.model.formatting_handlers.ListFormatHandler import ListFormatHandler
from src.coinverscrapy.model.formatting_handlers.TaskHandler import NewLineStartHandler
from src.coinverscrapy.model.formatting_handlers.RootHandler import RootHandler
from src.coinverscrapy.model.formatting_handlers.SubTaskHandler import TaskHandler
from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy
import pandas as pd

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
        self.root_handler\
            .set_next(ListFormatHandler())\
            .set_next(NewLineStartHandler())\
            .set_next(TaskHandler())

    def execute(self):
        # Main logic for parsing a list of PDF files
        print("Parser.execute()")
        with os.scandir(self.location) as files:
            for file in files:
                tables = camelot.read_pdf(file.path, pages='all', line_scale=50, split_text=True)
                # print("tables: {}".format(json.dumps(tables, indent=4)))

                directory_dict = os.path.split(file.path)  # directory_dict[0] for path to file, directory_dict[1] for file name
                raw_name = directory_dict[1][:-4]  # strip .pdf tag so we can replace it with .json
                i = 0
                reportSum = 0
                reportCount = 0
                for table in tables:  # Each table in the file
                    reportSum += table.parsing_report['accuracy']
                    reportCount += 1
                    fileline_count = 0

                    for line in table.df[0]:
                        # print('BEFORE: \n{}'.format(table.df[0][fileline_count]))
                        table.df[0][fileline_count] = handle(self.root_handler, line)
                        # print('AFTER: \n{}'.format(table.df[0][fileline_count]))
                        fileline_count += 1
                        # print(formattedline)

                    print(table.df[0])
                    i += 1
                    if i == 3:
                        print('AVERAGE ACCURACY: {}'.format(calculateAvg(reportSum, reportCount)))
                        return

                # with open(('json/' + raw_name + '.json'), 'w') as json_file:
                #     json.dump(raw_json, json_file)

def handle(handler, row: str):
    return handler.handle(row)


def calculateAvg(total, count):
    return total/count





# def formatSubTest(self, line_content, string1):
#     regex = re.compile(r'(%s)(.*)([1-9]{2})' % string1)
#     return regex.sub(r'\3\2\1', line_content)
