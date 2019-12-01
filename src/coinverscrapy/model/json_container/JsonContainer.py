import re

from camelot.core import Table
from pandas import Series

from src.coinverscrapy.model.json_container.Leerdoel import Leerdoel


class JsonContainer(object):

    def __init__(self, table):
        self.titel = ''
        self.omschrijving = ''
        self.leerdoelen = [Leerdoel]

        data = None
        if type(table) is Series:
            data = table.to_frame()[0].tolist()
        elif type(table) is Table:
            data = table.df[0].tolist()

        self.parse_meta(data)
        self.leerdoelen = self.parse_goals(data)

    def parse_meta(self, data):
        if 'Taak:' in data[1]:  # There is no module line
            self.titel = data.pop(0)
        else:  # there is a module line
            self.titel = data.pop(1)
            data.pop(0)

        self.omschrijving = data.pop(0)

    def parse_goals(self, data):
        new_vals = []
        for line in data:
            # print('line: {}'.format(line))
            if re.search('(^[a-zA-Z]/[a-zA-Z]+/\w.)', line):
                # print(len(new_vals))
                new_vals.append(Leerdoel())
                # print('Appent one, len: {}'.format(len(new_vals)))
                new_vals[len(new_vals) - 1].titel = line

            if re.search('((Deeltaak:)\s*)', line):
                # print(len(new_vals))
                line = re.sub('\s*(De kandidaat kan:)', "", line)
                new_vals[len(new_vals) - 1].omschrijving = line

            if re.search('(\d.\s+)', line):
                print('3. line: {}'.format(line))
                # print(len(new_vals))
                line = re.sub('\d.\s*', "", line)
                new_vals[len(new_vals) - 1].add_onderdeel(line)

        return new_vals
