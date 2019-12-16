import re

from camelot.core import Table
from pandas import Series

from src.coinverscrapy.model.json_container.Leerdoel import Leerdoel

"""
The main JSON container of our desired JSON format
Serialize/Deserialize using Jsonpickle in the parser
"""


class JsonContainer(object):

    def __init__(self, table, file_name):
        self.fileName = file_name.replace('pdfs\\', '')
        self.titel = ''
        self.omschrijving = ''
        self.leerdoelen = [Leerdoel]

        data = self.parse_data(table)

        self.parse_meta(data)
        self.leerdoelen = self.parse_leerdoelen(data)

    def format_unicode(self):
        self.titel = self.titel.encode('utf-8').decode()
        self.omschrijving = self.omschrijving.encode('utf-8').decode()

        try:
            for idx, leerdoel in enumerate(self.leerdoelen):
                self.leerdoelen[idx] = leerdoel.format_unicode()
        except TypeError:
            self.leerdoelen = None

        return self

    def parse_meta(self, data):
        regex = "([A-Za-z\-'\. ]*) as ([A-Za-z\-'\. ]*)"

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

        # match = re.match(regex, self.titel)

        clean_string = re.sub('\W+', '', self.titel)  # make sure there are no forbidden characters in the file name/title
        self.titel = clean_string

        self.omschrijving = data.pop(0)

    def parse_leerdoelen(self, data):
        new_vals = []
        idx = -1
        for line in data:
            try:
                # if re.search('(^[a-zA-Z]+/[a-zA-Z&.]+/\w*.\s*)', line):  # titel
                if re.search('(^[a-zA-Z]+/[a-zA-Z&.]*/[a-zA-Z0-9.]*[\d\s]*)', line):  # titel
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
                return None

        return new_vals

    def parse_data(self, table):
        if type(table) is Series:
            return table.to_frame()[0].tolist()
        elif type(table) is Table:
            return table.df[0].tolist()
        return None
