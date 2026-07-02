from csp.csp import CSP


def backtracking(thisCSP: CSP, forwardCheck=False, lcv=False):
    var = thisCSP.selectUnassignedVariable()

    if var is None:
        return thisCSP

    for value in thisCSP.orderValues(var, lcv):
        if thisCSP.isConsistent(var, value):
            thisCSP.assign(var, value)

            failed = False
            pruned = []

            if forwardCheck:
                failed, pruned = forwardCheckFunc(thisCSP, var)

            if not failed:
                result = backtracking(thisCSP, forwardCheck, lcv)

                if result is not None:
                    return result

            if forwardCheck:
                for neigh, neighVal in pruned:
                    thisCSP.restoreToDomain(neigh, neighVal)

            thisCSP.unassign(var)

    return None


def forwardCheckFunc(thisCSP: CSP, var):
    pruned = []
    failed = False

    for neighbor in thisCSP.neighbors[var]:
        if neighbor in thisCSP.assignments:
            continue

        for neighborVal in list(thisCSP.domains[neighbor]):
            if not thisCSP.isConsistent(neighbor, neighborVal):
                pruned.append((neighbor, neighborVal))

    for neigh, neighVal in pruned:
        thisCSP.removeFromDomain(neigh, neighVal)

    for neighbor in thisCSP.neighbors[var]:
        if neighbor not in thisCSP.assignments and len(thisCSP.domains[neighbor]) == 0:
            failed = True
            break

    return failed, pruned


def backtracking_all(csp, forwardCheck=False, lcv=False):
    solutions = []

    def dfs():
        var = csp.selectUnassignedVariable()

        if var is None:
            solutions.append(dict(csp.assignments))
            return

        for value in csp.orderValues(var, lcv):
            if csp.isConsistent(var, value):
                csp.assign(var, value)

                failed = False
                pruned = []

                if forwardCheck:
                    failed, pruned = forwardCheckFunc(csp, var)

                if not failed:
                    dfs()

                if forwardCheck:
                    for neigh, neighVal in pruned:
                        csp.restoreToDomain(neigh, neighVal)

                csp.unassign(var)

    dfs()
    return solutions
