from csp.csp import CSP


def backtracking(thisCSP: CSP, inference: str = "none", lcv=False):
    """Backtracking Algorithm for a Constraint Satisfaction Problem

    Args:
        thisCSP (CSP): The instance of a CSP having the algorithm run on
        inference (str, optional): Specifies the type of inference to run.
            Defaults to "none".
            Other options:  "forward_check", "ac3"
        lcv (bool, optional): Indicates whether to use the least constrained
            value or not. Defaults to False.

    Returns:
        None:  If there is no solution for this problem.
        thisCSP:  The CSP with all values assigned in a valid solution.
    """

    if inference not in ("none", "forward_check", "ac3"):
        raise ValueError("Invalid selection for inference type")
    forwardCheck = inference == "forward_check"
    useAC3 = inference == "ac3"

    var = thisCSP.selectUnassignedVariable()

    if var is None:
        return thisCSP

    for value in thisCSP.orderValues(var, lcv):
        if thisCSP.isConsistent(var, value):
            thisCSP.assign(var, value)

            failed, pruned = inferenceFunc(thisCSP, forwardCheck, useAC3, var, value)

            if not failed:
                result = backtracking(thisCSP, inference, lcv)

                if result is not None:
                    return result

            for neigh, neighVal in reversed(pruned):
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


def backtracking_all(thisCSP: CSP, inference="none", lcv=False):

    if inference not in ("none", "forward_check", "ac3"):
        raise ValueError("Invalid selection for inference type")
    forwardCheck = inference == "forward_check"
    useAC3 = inference == "ac3"

    solutions = []

    def dfs():
        var = thisCSP.selectUnassignedVariable()

        if var is None:
            solutions.append(dict(thisCSP.assignments))
            return

        for value in thisCSP.orderValues(var, lcv):
            if thisCSP.isConsistent(var, value):
                thisCSP.assign(var, value)

                failed, pruned = inferenceFunc(
                    thisCSP, forwardCheck, useAC3, var, value
                )

                if not failed:
                    dfs()

                for neigh, neighVal in reversed(pruned):
                    thisCSP.restoreToDomain(neigh, neighVal)

                thisCSP.unassign(var)

    dfs()
    return solutions


def ac3(thisCSP: CSP, initial_arcs=None):
    pruned = []

    if initial_arcs is None:
        queue = []

        for xi in thisCSP.variables:
            for xj in thisCSP.neighbors[xi]:
                queue.append((xi, xj))
    else:
        queue = list(initial_arcs)

    while len(queue) > 0:
        xi, xj = queue.pop(0)

        revised, newly_pruned = revise(thisCSP, xi, xj)

        pruned.extend(newly_pruned)

        if revised:
            if len(thisCSP.domains[xi]) == 0:
                return True, pruned

            for xk in thisCSP.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return False, pruned


def revise(thisCSP: CSP, xi, xj):
    revised = False
    pruned = []

    for x in list(thisCSP.domains[xi]):
        has_support = False

        for y in thisCSP.domains[xj]:
            if thisCSP.isPairConsistent(xi, x, xj, y):
                has_support = True
                break

        if not has_support:
            thisCSP.removeFromDomain(xi, x)
            pruned.append((xi, x))
            revised = True

    return revised, pruned


def restrictDomainToValue(thisCSP: CSP, var, value):
    pruned = []

    for otherValue in list(thisCSP.domains[var]):
        if otherValue != value:
            thisCSP.removeFromDomain(var, otherValue)
            pruned.append((var, otherValue))

    return pruned


def inferenceFunc(thisCSP: CSP, forwardCheck: bool, useAC3: bool, var, value):
    failed = False
    pruned = []
    if forwardCheck:
        failed, pruned = forwardCheckFunc(thisCSP, var)

    elif useAC3:
        pruned.extend(restrictDomainToValue(thisCSP, var, value))

        initial_arcs = []
        for neighbor in thisCSP.neighbors[var]:
            initial_arcs.append((neighbor, var))

        failed, ac3_pruned = ac3(thisCSP, initial_arcs)
        pruned.extend(ac3_pruned)

    return failed, pruned
