class Leerdoel(object):

    def __init__(self, title='N.A.', description='N.A.'):
        self.titel = title
        self.omschrijving = description
        self.onderdelen = []

    def format_unicode(self):
        self.titel = self.titel.encode('utf-8').decode()
        self.omschrijving = self.omschrijving.encode('utf-8').decode()

        for idx, onderdeel in enumerate(self.onderdelen):
            self.onderdelen[idx] = onderdeel.encode('utf-8').decode()

        return self

    def set_title(self, value):
        self.titel = value

    def set_description(self, value):
        self.omschrijving = value

    def add_onderdeel(self, value):
        self.onderdelen.append(value)

    def __str__(self):
        return self.titel
