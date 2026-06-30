from csp import CSP


def backtracking(thisCSP: CSP, forwardCheck=False, lcv=False):
    var = thisCSP.selectUnassignedVariable()

    if var is None:
        return thisCSP

    for value in thisCSP.orderValues(var, lcv):
        if thisCSP.isConsistent(var, value):
            thisCSP.assign(var, value)

            pruned = []
            failed = False

            if forwardCheck:
                for neighbor in thisCSP.neighbors[var]:
                    if neighbor in thisCSP.assignments:
                        continue

                    for neighborVal in list(thisCSP.domains[neighbor]):
                        if not thisCSP.isConsistent(neighbor, neighborVal):
                            pruned.append((neighbor, neighborVal))

                for neigh, neighVal in pruned:
                    thisCSP.removeFromDomain(neigh, neighVal)

                for neighbor in thisCSP.neighbors[var]:
                    if (
                        neighbor not in thisCSP.assignments
                        and len(thisCSP.domains[neighbor]) == 0
                    ):
                        failed = True
                        break

            if not failed:
                result = backtracking(thisCSP, forwardCheck, lcv)

                if result is not None:
                    return result

            if forwardCheck:
                for neigh, neighVal in pruned:
                    thisCSP.restoreToDomain(neigh, neighVal)

            thisCSP.unassign(var)

    return None
