from dataclasses import dataclass
from typing import Callable, Any
from collections import defaultdict


@dataclass(frozen=True)
class CSPVariable:
    name: str


@dataclass(frozen=True)
class CSPConstraint:
    variables: tuple[CSPVariable, ...]
    function: Callable[..., bool]


class CSP:
    def __init__(self):
        self.variables: set[CSPVariable] = set()
        self.domains: dict[CSPVariable, set[Any]] = {}
        self.original_domains: dict[CSPVariable, set[Any]] = {}
        self.assignments: dict[CSPVariable, Any] = {}
        self.constraints: set[CSPConstraint] = set()
        self.neighbors: dict[CSPVariable, set[CSPVariable]] = defaultdict(set)

    def _requireVariable(self, var):
        if var not in self.variables:
            raise ValueError(f"Variable {var.name} does not exist in this CSP")

    def _requireVariableNew(self, var):
        if var in self.variables:
            raise ValueError(f"Variable {var.name} already exists in this CSP")

    def _requireUnassigned(self, var):
        self._requireVariable(var)

        if var in self.assignments:
            raise ValueError(f"Variable {var.name} is already assigned")

    def _requireAssigned(self, var):
        self._requireVariable(var)

        if var not in self.assignments:
            raise ValueError(f"Variable {var.name} is not currently assigned")

    def _requireValueInDomain(self, var, value):
        self._requireVariable(var)

        if value not in self.domains[var]:
            raise ValueError(f"Value {value} is not in domain of {var.name}")

    def _addNeighborEdge(self, var1, var2):
        if var1 == var2:
            raise ValueError(f"The value {var1.name} cannot be its own neighbor")

        self.neighbors[var1].add(var2)
        self.neighbors[var2].add(var1)

    def addVariable(self, name, domain):
        new_var = CSPVariable(name)

        self._requireVariableNew(new_var)

        self.variables.add(new_var)
        self.domains[new_var] = set(domain)
        self.original_domains[new_var] = set(domain)

        return new_var

    def addUnaryConstraint(self, var, constraint):
        return self.addNaryConstraint([var], constraint)

    def addBinaryConstraint(self, var1, var2, constraint):
        return self.addNaryConstraint([var1, var2], constraint)

    def addNaryConstraint(self, vars, constraint):
        new_con = CSPConstraint(tuple(vars), constraint)

        for v in vars:
            self._requireVariable(v)

        if new_con in self.constraints:
            raise ValueError("Constraint already exists")

        self.constraints.add(new_con)
        for i in range(len(vars)):
            for j in range(i + 1, len(vars)):
                self._addNeighborEdge(vars[i], vars[j])

        return new_con

    def assign(self, var, value):
        self._requireUnassigned(var)
        self._requireValueInDomain(var, value)

        self.assignments[var] = value

    def unassign(self, var):
        self._requireAssigned(var)
        self.assignments.pop(var)

    def getLegalValues(self, var):
        self._requireVariable(var)
        return tuple(s for s in self.domains[var])

    def removeFromDomain(self, var, value):
        self._requireVariable(var)

        if value not in self.domains[var]:
            raise ValueError(f"Value {value} is not currently in domain of {var.name}")

        self.domains[var].remove(value)

    def restoreToDomain(self, var, value):
        self._requireVariable(var)

        if value not in self.original_domains[var]:
            raise ValueError(f"Value {value} was not in original domain of {var.name}")

        if value in self.domains[var]:
            raise ValueError(
                f"Value {value} is already in current domain of {var.name}"
            )

        self.domains[var].add(value)

    def resetDomain(self, var):
        self._requireVariable(var)

        self.domains[var] = self.original_domains[var].copy()

    def resetAllDomains(self):
        for var in self.variables:
            self.resetDomain(var)

    def getConstraintsFor(self, var):
        self._requireVariable(var)

        return [
            constraint for constraint in self.constraints if var in constraint.variables
        ]

    def isConsistent(self, var, value) -> bool:
        self._requireUnassigned(var)
        self._requireValueInDomain(var, value)

        constraints = self.getConstraintsFor(var)
        self.assign(var, value)

        try:
            for constraint in constraints:
                notAssigned = [
                    v for v in constraint.variables if v not in self.assignments
                ]

                if len(notAssigned) > 0:
                    continue

                values = [self.assignments[v] for v in constraint.variables]

                if not constraint.function(*values):
                    return False

            return True

        finally:
            self.unassign(var)

    def selectUnassignedVariable(self):
        candidates = []

        for var in self.variables:
            if var not in self.assignments:
                domain_size = len(self.domains[var])
                constraint_count = len(self.getConstraintsFor(var))
                candidates.append((var, domain_size, constraint_count))

        if len(candidates) == 0:
            return None

        candidates.sort(key=lambda item: (item[1], -item[2]))

        return candidates[0][0]

    def getPruneCount(self, var, value):
        if not self.isConsistent(var, value):
            return float("inf")

        pruned = 0
        self.assign(var, value)

        try:
            for neighbor in self.neighbors[var]:
                if neighbor in self.assignments:
                    continue

                for nval in list(self.domains[neighbor]):
                    if not self.isConsistent(neighbor, nval):
                        pruned += 1

            return pruned

        finally:
            self.unassign(var)

    def orderValues(self, var, lcv=False):
        initialValues = list(self.domains[var])
        if not lcv:
            return initialValues

        withPruneCount = [(val, self.getPruneCount(var, val)) for val in initialValues]

        withPruneCount.sort(key=lambda item: item[1])

        return [val[0] for val in withPruneCount]

    def addNeighbors(self, var1, var2, symmetric=True):
        self._requireVariable(var1)
        self._requireVariable(var2)
        if var1 == var2:
            raise ValueError(f"The value {var1.name} cannot be it's own neighbor")
        if var1 in self.neighbors[var2]:
            raise ValueError(
                f"The value {var1.name} is already a neighbor to {var2.name}"
            )
        if symmetric and var2 in self.neighbors[var1]:
            raise ValueError(
                f"The value {var2.name} is already a neighbor to {var1.name}"
            )
        self.neighbors[var1].add(var2)
        if symmetric:
            self.neighbors[var2].add(var1)
