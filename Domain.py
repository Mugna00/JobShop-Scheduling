import copy


# classe dei Domini
class Domain:
    def __init__(self, jobs):
        self.__D = []
        temp_max = 0
        for i in range(len(jobs)):
            temp_max += int(jobs[i].time)
        for i in range(len(jobs)):
            self.__D.append(list(range(temp_max)))

    def getDomain(self):
        return copy.deepcopy(self.__D)
