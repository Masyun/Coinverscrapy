class Leerdoel(object):

    def __init__(self, title='N.A.', description='N.A.'):
        self.titel = title
        self.omschrijving = description
        self.onderdelen = []

    def set_title(self, value):
        self.titel = value

    def set_description(self, value):
        self.omschrijving = value

    def add_onderdeel(self, value):
        self.onderdelen.append(value)
