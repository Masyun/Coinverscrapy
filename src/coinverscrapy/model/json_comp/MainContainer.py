from src.coinverscrapy.model.json_comp.GoalsContainer import GoalsContainer
from src.coinverscrapy.model.json_comp.JsonFormat import JsonFormat
from src.coinverscrapy.model.json_comp.MetaContainer import MetaContainer


class MainContainer(JsonFormat):

    def __init__(self):
        self.metainfo = MetaContainer()
        self.goals = GoalsContainer()

    def tojson(self):
        pass
