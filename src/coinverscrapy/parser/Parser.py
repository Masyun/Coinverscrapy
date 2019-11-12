import re

from src.coinverscrapy.model.json_formatter.ListFormatHandler import ListFormatHandler
from src.coinverscrapy.model.json_formatter.NewLineStartHandler import NewLineStartHandler
from src.coinverscrapy.model.json_formatter.abs_formatter import Json_Handler
from src.coinverscrapy.model.json_formatter.abs_formatter.AbstractHandler import AbstractHandler
from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy
import os
import camelot
import json
# import tabula


class Parser(IModuleProxy):
    def __init__(self, input_location):
        self.location = input_location

        self.listformat_handler = ListFormatHandler()
        self.newline_handler = NewLineStartHandler()

        self.setupHandlers()


    def setupHandlers(self): # Pay attention to the escape slashes with every new set_next() call
        self.listformat_handler\
            .set_next(self.newline_handler)

    def execute(self):
        # Main logic for parsing a list of PDF files
        print("Parser.execute()")
        with os.scandir(self.location) as files:
            for file in files:
                tables = camelot.read_pdf(file.path, pages='all', line_scale=50, split_text=True)
                # print("tables: {}".format(json.dumps(tables, indent=4)))

                directory_dict = os.path.split(file.path)  # directory_dict[0] for path to file, directory_dict[1] for file name
                raw_name = directory_dict[1][:-4]  # strip .pdf tag so we can replace it with .json

                for table in tables:  # Each table in the file
                    # print(table.parsing_report['page'])
                    # print(table)
                    # print(table.parsing_report)
                    print(table.df)
                    # print('---------------------\n')
                    # table.df.to_json('json/' + raw_name + '.json')

                    # print('json_string: \n{}'.format(json_string))
                    # raw_json = json.dumps(json_string, indent=4)
                    json_dict = table.df.to_json(orient="records")
                    print(table.df[0])
                    self.handle(table.df[0])


                    # i = 0
                    # for index, row in table.df:
                    #     self.handleFormatting(row)
                    #     print(row)
                    #
                    #     i += 1
                    #
                    #     if i == 10:
                    #         return
                        # if row[0].startswith("D\n"): # Swap position of 'D\n' with last \n in line
                        #     print('row: \n{}'.format(row))

                        # if row[0]

                # with open(('json/' + raw_name + '.json'), 'w') as json_file:
                #     json.dump(raw_json, json_file)

    def handle(self, row: str):
        return self.listformat_handler.handle(row)





# def formatSubTest(self, line_content, string1):
#     regex = re.compile(r'(%s)(.*)([1-9]{2})' % string1)
#     return regex.sub(r'\3\2\1', line_content)
