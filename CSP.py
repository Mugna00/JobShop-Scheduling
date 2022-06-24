from Variable import *
from Domain import *
from Constraint import *


class CSP:

    def __init__(self, jobs):
        self.jobs = jobs
        self.X = Variable(jobs)
        self.D = Domain(jobs)
        self.C = Constraint(jobs)


class Backtracking:
    def __init__(self, csp, nWorker):
        self.csp = csp
        self.nWorker = nWorker
        s = self.backtracking_search()
        self.solution = self.getBestSolution(s)

    def backtracking_search(self):
        assignment = self.setAssignment()
        return self.backtracking(assignment, self.csp.D.getDomain())

    def setAssignment(self):
        assignment = {}
        for i in range(self.nWorker):
            assignment[i] = {}  # lavoratore i
            # assignment[i][-1] = 0, 0  # id_operation, start_time, end_time
        return assignment

    def backtracking(self, assignment, domain):
        solution = []
        if self.assignmentIsComplete(assignment):
            solution.append(assignment)
            return solution
        var = self.selectUnassignedVariable(assignment)
        var = self.orderDomainValues(var, domain)
        for x in var:
            app_assignment = copy.deepcopy(assignment)
            app_domain = copy.deepcopy(domain)
            self.addAssignment(assignment, x, domain)
            if self.AC_3(domain):
                result = self.backtracking(assignment, domain)
                assignment = copy.deepcopy(app_assignment)
                domain = copy.deepcopy(app_domain)
                if result is not False:
                    for y in result:
                        solution.append(y)
            else:
                return False
        return solution

    def addAssignment(self, assignment, var, domain):
        (i, j) = self.getMachine(assignment)
        if domain[var][0] > i:
            i = domain[var][0]
        assignment[j][var] = (i, i + self.csp.X.getVariableTime(var))
        domain[var] = [i]

    def getMachine(self, assignment):
        j = 0
        i = 0
        if len(assignment[0]) != 0:
            i = assignment[0][list(assignment[0].keys())[-1]][1] + 1
        for x in range(len(assignment)):
            if len(assignment[x]) == 0:
                j = x
                i = 0
                return i, j
            else:
                if assignment[j][list(assignment[j].keys())[-1]][1] > assignment[x][list(assignment[x].keys())[-1]][1]:
                    j = x
                    i = assignment[j][list(assignment[j].keys())[-1]][1]
        return i, j

    def assignmentIsComplete(self, assignment):
        count = 0
        for j in range(len(assignment)):
            for x in assignment[j]:
                if x != -1:
                    count = count + 1
        if count == self.csp.X.getLen():
            return True
        else:
            return False

    def selectUnassignedVariable(self, assignment):
        var = []
        for i in range(self.csp.X.getLen()):
            if self.countOfConstraint(assignment, i):
                var.append(i)
        return var

    def countOfConstraint(self, assignment, i):
        listC = self.csp.C.getConstraintList(i)
        if self.assignmentContain(assignment, i) is True:
            return False  # perchè la variabile è già stata assegnata
        if len(listC) == 0:
            return True  # perchè la variabile contiene 0 vincoli
        count = 0
        for x in listC:
            if self.assignmentContain(assignment, x):
                count = count + 1
        if count == len(listC):
            return True

    def orderDomainValues(self, var, domain):
        app_var = copy.deepcopy(var)
        for i in range(len(app_var)):
            posmin = i
            for j in range(i + 1, len(app_var)):
                if len(self.csp.C.getConstraintList(var[j])) <= len(self.csp.C.getConstraintList(var[posmin])):
                    if domain[var[posmin]][0] > domain[var[j]][0]:
                        posmin = j
                    elif domain[var[posmin]][0] == domain[var[j]][0]:
                        if self.csp.X.getVariableTime(var[posmin]) > self.csp.X.getVariableTime(var[j]):
                            posmin = j
            if posmin != i:
                app = app_var[i]
                app_var[i] = app_var[posmin]
                app_var[posmin] = app
        return app_var

    def AC_3(self, domain):
        queue = self.csp.C.getArc()
        while len(queue) != 0:
            (i, j) = queue.pop(0)
            if self.revise(i, j, domain):
                if len(domain[i]) == 0:
                    return False
                self.getNeighbors(i, j, queue)
        return True

    def getNeighbors(self, i, j, queue):
        arc = self.csp.C.getArc()
        for x in arc:
            if x[1] == i and x[0] != j:
                if (x in queue) is False:
                    queue.append(x)

    def revise(self, i, j, domain):
        domain_app = []
        revised = False
        for x in domain[i]:
            count = 0
            for y in domain[j]:
                if self.csp.C.getConstraint(i, j)(x, y) is False:
                    count = count + 1
            if count == len(domain[j]):
                domain_app.append(x)
                revised = True
        for x in domain_app:
            domain[i].remove(x)
        return revised

    def getBestSolution(self, solution):
        temp = []
        for x in solution:
            temp.append(self.getTime(x))
        i = 0
        s = solution[0]
        for x in range(len(solution)):
            if temp[i] > temp[x]:
                i = x
                s = solution[x]
        return [s]

    @staticmethod
    def getTime(solution):
        j = 0
        for x in solution:
            if solution[j][list(solution[j].keys())[-1]][1] < solution[x][list(solution[x].keys())[-1]][1]:
                j = x
        return solution[j][list(solution[j].keys())[-1]][1]

    @staticmethod
    def assignmentContain(assignment, i):
        try:
            for j in range(len(assignment)):
                for x in assignment[j]:
                    if x == i:
                        return True
            return False
        except:
            return False
