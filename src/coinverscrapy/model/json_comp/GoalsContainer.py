from src.coinverscrapy.model.json_comp.JsonFormat import JsonFormat
from src.coinverscrapy.model.json_comp.MetaContainer import MetaContainer


class GoalsContainer(MetaContainer):

    def __init__(self):
        super().__init__()
        self.__goals = []

    def getGoals(self):
        return self.__goals

    def setGoals(self, value):
        self.__goals = value

    def addGoal(self, value):
        self.__goals.append(value)

    def tojson(self):
        return 'from subclass: /\n'.join('call to super: ').join(super().tojson())




