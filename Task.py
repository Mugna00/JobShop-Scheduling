# Classe delle attività
class Task:
    def __init__(self, time, precedence, name=''):
        self.time = time
        self.precedence = precedence
        self.name = name
        self.id = -1
        self.disjunctive = []

    def addDisjunctive(self, disjunctive):
        self.disjunctive.append(disjunctive)

    def addPrecedence(self, precedence):
        self.precedence.append(precedence)
