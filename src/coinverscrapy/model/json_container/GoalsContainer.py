class GoalsContainer(object):

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.goals = []

    def getGoals(self):
        return self.goals

    def setGoals(self, value):
        self.goals = value

    def addGoal(self, value):
        self.goals.append(value)

    def reprJSON(self):
        return dict(title=self.title, description=self.description, goals=self.goals)




