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
        length = 0  # current length of the new_vals list
        for line in data:
            if re.search('(^[a-zA-Z]/[a-zA-Z]+/\d.)', line):
                new_vals.append(Leerdoel())
                length = len(new_vals) - 1
                new_vals[length].titel = line

            if re.search('((Deeltaak:)\s*)', line):
                line = re.sub('\s*(De kandidaat kan:)', "", line)
                new_vals[length].omschrijving = line

            if re.search('(\d.\s+)', line):
                # print('3. line: {}'.format(line))
                line = re.sub('\d.\s*', "", line)
                new_vals[length].add_onderdeel(line)

        return new_vals
