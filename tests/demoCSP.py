# demo.py

from csp import CSP

from tests.util import (
    print_section,
    expect_true,
    expect_false,
    expect_none,
    expect_not_none,
    expect_error,
    names,
)


def test_variables_and_domains():
    print_section("Variables and Domains")

    csp = CSP()

    x = csp.addVariable("X", [1, 2, 3])
    y = csp.addVariable("Y", ["red", "green"])

    expect_true("X exists", x in csp.variables)
    expect_true("Y exists", y in csp.variables)
    expect_true("X current domain is {1, 2, 3}", csp.domains[x] == {1, 2, 3})
    expect_true("X original domain is {1, 2, 3}", csp.original_domains[x] == {1, 2, 3})

    expect_error(
        "Duplicate variable name rejected",
        lambda: csp.addVariable("X", [4, 5, 6]),
    )


def test_domain_mutation():
    print_section("Domain Mutation")

    csp = CSP()
    x = csp.addVariable("X", [1, 2, 3])

    csp.removeFromDomain(x, 1)

    expect_false("1 removed from current domain", 1 in csp.domains[x])
    expect_true("1 still exists in original domain", 1 in csp.original_domains[x])

    expect_error(
        "Cannot remove missing value",
        lambda: csp.removeFromDomain(x, 1),
    )

    csp.restoreToDomain(x, 1)

    expect_true("1 restored to current domain", 1 in csp.domains[x])

    expect_error(
        "Cannot restore value already present",
        lambda: csp.restoreToDomain(x, 1),
    )

    expect_error(
        "Cannot restore value outside original domain",
        lambda: csp.restoreToDomain(x, 99),
    )

    csp.removeFromDomain(x, 1)
    csp.removeFromDomain(x, 2)

    expect_true("Only one value remains after pruning", csp.domains[x] == {3})

    csp.resetDomain(x)

    expect_true("resetDomain restores original domain", csp.domains[x] == {1, 2, 3})
    expect_true(
        "resetDomain copies original domain instead of aliasing it",
        csp.domains[x] is not csp.original_domains[x],
    )


def test_assignment_rules():
    print_section("Assignments")

    csp = CSP()
    x = csp.addVariable("X", [1, 2, 3])

    csp.assign(x, 2)

    expect_true("X assigned to 2", csp.assignments[x] == 2)

    expect_error(
        "Cannot assign already-assigned variable",
        lambda: csp.assign(x, 3),
    )

    csp.unassign(x)

    expect_true("X unassigned", x not in csp.assignments)

    expect_error(
        "Cannot unassign unassigned variable",
        lambda: csp.unassign(x),
    )

    expect_error(
        "Cannot assign value outside domain",
        lambda: csp.assign(x, 99),
    )


def test_unary_binary_nary_constraints():
    print_section("Unary, Binary, and N-ary Constraints")

    csp = CSP()

    a = csp.addVariable("A", [1, 2, 3])
    b = csp.addVariable("B", [1, 2, 3])
    c = csp.addVariable("C", [1, 2, 3])

    csp.addUnaryConstraint(a, lambda x: x != 1)

    expect_false("A = 1 violates unary constraint", csp.isConsistent(a, 1))
    expect_true("A = 2 satisfies unary constraint", csp.isConsistent(a, 2))

    csp.addBinaryConstraint(a, b, lambda x, y: x != y)

    csp.assign(a, 2)

    expect_false("B = 2 conflicts with A = 2", csp.isConsistent(b, 2))
    expect_true("B = 3 is consistent with A = 2", csp.isConsistent(b, 3))

    csp.unassign(a)

    csp.addNaryConstraint([a, b, c], lambda x, y, z: x + y + z == 6)

    csp.assign(a, 1)
    csp.assign(b, 2)

    expect_true("C = 3 completes sum to 6", csp.isConsistent(c, 3))
    expect_false("C = 2 does not complete sum to 6", csp.isConsistent(c, 2))

    csp.unassign(a)
    csp.unassign(b)


def test_automatic_neighbors():
    print_section("Automatic Neighbor Creation")

    csp = CSP()

    a = csp.addVariable("A", [1, 2])
    b = csp.addVariable("B", [1, 2])
    c = csp.addVariable("C", [1, 2])

    csp.addNaryConstraint([a, b, c], lambda x, y, z: True)

    expect_true("A has B as neighbor", b in csp.neighbors[a])
    expect_true("A has C as neighbor", c in csp.neighbors[a])
    expect_true("B has A as neighbor", a in csp.neighbors[b])
    expect_true("B has C as neighbor", c in csp.neighbors[b])
    expect_true("C has A as neighbor", a in csp.neighbors[c])
    expect_true("C has B as neighbor", b in csp.neighbors[c])

    for var in sorted(csp.variables, key=lambda v: v.name):
        print(f"{var.name}: {names(csp.neighbors[var])}")

    expect_error(
        "Duplicate manual neighbor edge rejected",
        lambda: csp.addNeighbors(a, b),
    )

    expect_error(
        "Self-neighbor rejected",
        lambda: csp.addNeighbors(a, a),
    )


def test_directed_neighbors():
    print_section("Directed Neighbors")

    csp = CSP()

    a = csp.addVariable("A", [1, 2])
    b = csp.addVariable("B", [1, 2])

    csp.addNeighbors(a, b, symmetric=False)

    expect_true("A has B as directed neighbor", b in csp.neighbors[a])
    expect_false("B does not have A as directed neighbor", a in csp.neighbors[b])


def test_mrv_degree_selection():
    print_section("MRV / Degree Variable Selection")

    csp = CSP()

    a = csp.addVariable("A", [1, 2, 3])
    b = csp.addVariable("B", [1])
    c = csp.addVariable("C", [1, 2])

    csp.addBinaryConstraint(a, b, lambda x, y: x != y)
    csp.addBinaryConstraint(a, c, lambda x, y: x != y)

    selected = csp.selectUnassignedVariable()

    print(f"Selected variable: {selected.name}")

    expect_true("MRV selects variable with smallest domain", selected == b)


def test_lcv_ordering():
    print_section("LCV Value Ordering")

    csp = CSP()

    x = csp.addVariable("X", [1, 2, 3])
    y = csp.addVariable("Y", [1, 2, 3])
    z = csp.addVariable("Z", [1, 2, 3])

    # X=1 removes one value from Y.
    # X=2 removes one value from Y and one value from Z.
    # X=3 removes one value from Z.
    csp.addBinaryConstraint(x, y, lambda xv, yv: not (xv == 1 and yv == 1))
    csp.addBinaryConstraint(x, y, lambda xv, yv: not (xv == 2 and yv == 2))
    csp.addBinaryConstraint(x, z, lambda xv, zv: not (xv == 2 and zv == 2))
    csp.addBinaryConstraint(x, z, lambda xv, zv: not (xv == 3 and zv == 3))

    scores = [(value, csp.getPruneCount(x, value)) for value in csp.orderValues(x)]
    ordered = csp.orderValues(x, lcv=True)

    print(f"Prune scores: {scores}")
    print(f"LCV order: {ordered}")

    expect_true("X=2 is most constraining", csp.getPruneCount(x, 2) == 2)
    expect_true("X=1 prunes one value", csp.getPruneCount(x, 1) == 1)
    expect_true("X=3 prunes one value", csp.getPruneCount(x, 3) == 1)
    expect_true("LCV puts value 2 last", ordered[-1] == 2)


def main():
    test_variables_and_domains()
    test_domain_mutation()
    test_assignment_rules()
    test_unary_binary_nary_constraints()
    test_automatic_neighbors()
    test_directed_neighbors()
    test_mrv_degree_selection()
    test_lcv_ordering()

    print_section("Demo Complete")
    print("CSP demo completed.")


if __name__ == "__main__":
    main()
