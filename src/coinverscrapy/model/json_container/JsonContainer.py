import re

from camelot.core import Table
from pandas import Series

from src.coinverscrapy.model.json_container.Leerdoel import Leerdoel

"""
The main JSON container of our desired JSON format
Serialize/Deserialize using Jsonpickle in the parser
"""


class JsonContainer(object):

    def __init__(self, table, fileName):
        self.fileName = fileName.replace('pdfs\\', '')
        self.titel = ''
        self.omschrijving = ''
        self.leerdoelen = [Leerdoel]

        data = None
        if type(table) is Series:
            data = table.to_frame()[0].tolist()
        elif type(table) is Table:
            data = table.df[0].tolist()

        self.parse_meta(data)
        self.leerdoelen = self.parse_leerdoelen(data)

    def parse_meta(self, data):
        if 'Taak:' in data[1]:  # There is no module line
            self.titel = data.pop(0)
        else:  # there is a module line
            if 'Module' in self.titel:
                self.titel = data.pop(1)
                data.pop(0)
            else:
                self.titel = data.pop(0)
                if 'Taak:' not in data[0]:
                    data.pop(0)

        self.omschrijving = data.pop(0)

    def parse_leerdoelen(self, data):
        new_vals = []
        idx = -1
        for line in data:
            try:
                if re.search('(^[a-zA-Z]+/[a-zA-Z&.]+/\w*.\s*)', line):  # titel
                # if re.search('(^[a-zA-Z]+/[a-zA-Z&.]+/\w)', line):  # titel
                    new_vals.append(Leerdoel())
                    idx = (len(new_vals) - 1)
                    new_vals[idx].titel = line

                if re.search('((Deeltaak:)\s*)', line):  # omschrijving
                    line = re.sub('\s*(De kandidaat kan:)', "", line)
                    new_vals[idx].omschrijving = line

                if re.search('^(\d.\s+)', line):  # leerdoel
                    line = re.sub('\d.\s*', "", line)
                    new_vals[idx].add_onderdeel(line)

            except IndexError:
                self.leerdoelen = None
                break

        return new_vals
