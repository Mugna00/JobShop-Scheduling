# Classe dei Vicoli
class Constraint:
    def __init__(self, jobs):
        self.__C = {}
        self.__CDis = {}
        self.__time = {}
        self.__Constraint = {}
        self.__ConstraintD = {}
        for i in range(len(jobs)):
            self.__Constraint[jobs[i].id] = []
            self.__time[jobs[i].id] = jobs[i].time
            for k in range(len(jobs[i].precedence)):
                self.setConstraint(jobs[i].precedence[k].id, jobs[i].id,
                                   jobs[i].precedence[k].time)
                self.__Constraint[jobs[i].id].append(jobs[i].precedence[k].id)
        for i in range(len(jobs)):
            self.__ConstraintD[jobs[i].id] = []
            for k in range(len(jobs[i].disjunctive)):
                self.setConstraintD(jobs[i].id, jobs[i].disjunctive[k].id, jobs[i].time,
                                    jobs[i].disjunctive[k].time)
                self.__ConstraintD[jobs[i].id].append(jobs[i].disjunctive[k].id)

    def setConstraint(self, i, j, time):
        self.__C[(i, j)] = lambda a, b: a + time <= b
        self.__C[(j, i)] = lambda b, a: b >= a + time

    def setConstraintD(self, i, j, time_i, time_j):
        self.__CDis[i, j] = lambda a, b: a + time_i <= b or b + time_j <= a

    def getConstraintList(self, i):
        return self.__Constraint[i]

    def getConstraint(self, i, j):
        try:
            return self.__C[i, j]
        except:
            try:
                return self.__CDis[i, j]
            except:
                return None

    def getPrecedence(self, i, j):
        try:
            return self.__C[i, j]
        except:
            return None

    def getTime(self, i):
        try:
            return self.__time[i]
        except:
            return None

    # Restituisce gli archi
    def getArc(self):
        arc = []
        for i in self.__Constraint:
            for j in self.__Constraint[i]:
                arc.append((i, j))
                arc.append((j, i))
        for i in self.__ConstraintD:
            for j in self.__ConstraintD[i]:
                arc.append((i, j))
                arc.append((j, i))
        return arc
