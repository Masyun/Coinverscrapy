from src.coinverscrapy.model.proxy.IModuleProxy import IModuleProxy
import os
import camelot
import json


class Parser(IModuleProxy):
    def __init__(self, input_location):
        self.data = []
        self.location = input_location

    def execute(self):
        # Main logic for parsing a list of PDF files
        print("Parser.execute()")
        with os.scandir(self.location) as files:
            i = 0 # remove
            for file in files:
                i += 1 # remove
                directory_dict = os.path.split(
                    file.path)  # directory_dict[0] for path to file, directory_dict[1] for file name

                raw_name = directory_dict[1][:-4]  # strip .pdf tag so we can replace it with .json
                tables = camelot.read_pdf(file.path)
                print("PATH --->" + file.path)
                print('tables[0] yields:\n')
                print(tables[0])

                print(tables[0].parsing_report)
                print(tables[0].df)
                tables[0].to_json('json/' + raw_name + '.json', orient='columns')

                # with open(('json/' + raw_name + '.json'), 'w') as json_file:
                #     json.dump(temp, json_file, sort_keys=True, indent=4)

                # following is just a time saver for development - remove after finishing
                print('\n\n')
                if i == 5:
                    return

    def addOne(self, entry):
        self.data.append(entry)

    def getAll(self):
        return self.data.copy()
