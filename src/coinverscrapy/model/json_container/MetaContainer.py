class MetaContainer(object):
    def __init__(self, title: str, description: str):
        self.title = title
        self.description = description

    def reprJSON(self):
        return dict(titel=self.title, omschrijving=self.description)
