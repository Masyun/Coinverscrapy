import pandas as pd
from camelot.core import Table
from pandas import Series


class JsonContainer(object):

    def __init__(self, table):
        data = None

        if type(table) is Series:
            data = table.to_frame()[0]
        elif type(table) is Table:
            data = table.df[0]

        self.title = data[0]
        self.description = data[1].rstrip()

        stripped = pd.DataFrame(data.drop(labels=[0, 1])).reset_index(drop=True)

        print('After removing meta:')
        print(stripped)

    def reprJSON(self):
        return dict(titel=self.title, omschrijving=self.description)
