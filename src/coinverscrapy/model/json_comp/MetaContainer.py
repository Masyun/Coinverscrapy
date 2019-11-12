from src.coinverscrapy.model.json_comp.JsonFormat import JsonFormat


class MetaContainer(JsonFormat):
    def __init__(self):
        self._title = ''
        self._description = ''

    def getTitle(self):
        return self._title

    def getDescription(self):
        return self._description

    def setTitle(self, value):
        self._title = value

    def setDescription(self, value):
        self._description = value

    def tojson(self):
        return 'from super container call'
