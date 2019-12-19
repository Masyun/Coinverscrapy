import re
import string


class Leerdoel(object):

    def __init__(self, title='N.A.', description='N.A.'):
        self.titel = title
        self.omschrijving = description
        self.onderdelen = []

    def format_unicode(self):
        self.titel = remove_unicode(self.titel)
        self.omschrijving = remove_unicode(self.omschrijving)

        for idx, onderdeel in enumerate(self.onderdelen):
            self.onderdelen[idx] = remove_unicode(onderdeel)

        return self

    def set_title(self, value):
        self.titel = value

    def set_description(self, value):
        self.omschrijving = value

    def add_onderdeel(self, value):
        self.onderdelen.append(value)

    def __str__(self):
        return self.titel


def remove_unicode(line):
    printable = set(string.printable)
    line = ''.join(filter(lambda x: x in printable, line))
    return line
