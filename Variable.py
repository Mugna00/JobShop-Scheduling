# classe delle Variabili
class Variable:
    def __init__(self, jobs):
        self.__name = []
        self.__time = []
        self.__X = []
        self.__len = 0
        for i in range(len(jobs)):
            if jobs[i].name == "":
                self.__name.append('Job' + str(jobs[i].id))
            else:
                self.__name.append(jobs[i].name)
            self.__time.append(jobs[i].time)
            self.__X.append(-1)
            jobs[i].id = self.__len
            self.__len = self.__len + 1

    def getVariable(self, i):
        return self.__X[i]

    def getVariableName(self, i):
        return self.__name[i]

    def getVariableTime(self, i):
        return self.__time[i]

    def setVariable(self, i, value):
        self.__X[i] = value

    def getLen(self):
        return self.__len
