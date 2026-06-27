# demo.py

from csp import CSP


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def expect_error(description, func):
    try:
        func()
        print(f"[FAIL] {description}: expected error, but none was raised")
    except Exception as e:
        print(f"[PASS] {description}: {type(e).__name__}: {e}")


def expect_true(description, value):
    if value:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}")


def expect_false(description, value):
    if not value:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}")


def main():
    print_section("Create CSP")

    csp = CSP()

    wa = csp.addVariable("WA", ["red", "green", "blue"])
    nt = csp.addVariable("NT", ["red", "green", "blue"])
    sa = csp.addVariable("SA", ["red", "green", "blue"])
    q = csp.addVariable("Q", ["red", "green", "blue"])

    print("Variables:")
    for var in csp.variables:
        print(f"  {var.name}: {csp.getLegalValues(var)}")

    expect_true("WA exists in CSP", wa in csp.variables)
    expect_true("WA domain has 3 values", len(csp.domains[wa]) == 3)

    print_section("Duplicate Variable Test")

    expect_error(
        "Adding duplicate variable WA",
        lambda: csp.addVariable("WA", ["red", "green", "blue"])
    )

    print_section("Domain Mutation Tests")

    expect_true(
        "WA original domain starts with red",
        "red" in csp.original_domains[wa]
    )

    expect_true(
        "WA current domain starts with red",
        "red" in csp.domains[wa]
    )

    csp.removeFromDomain(wa, "red")

    expect_false(
        "WA current domain no longer has red after removeFromDomain",
        "red" in csp.domains[wa]
    )

    expect_true(
        "WA original domain still has red after removeFromDomain",
        "red" in csp.original_domains[wa]
    )

    expect_error(
        "Cannot remove red from WA twice",
        lambda: csp.removeFromDomain(wa, "red")
    )

    expect_error(
        "Cannot remove value outside original/current domain",
        lambda: csp.removeFromDomain(wa, "purple")
    )

    csp.restoreToDomain(wa, "red")

    expect_true(
        "WA current domain has red again after restoreToDomain",
        "red" in csp.domains[wa]
    )

    expect_error(
        "Cannot restore red when already present",
        lambda: csp.restoreToDomain(wa, "red")
    )

    expect_error(
        "Cannot restore purple because it was never in original domain",
        lambda: csp.restoreToDomain(wa, "purple")
    )

    csp.removeFromDomain(wa, "red")
    csp.removeFromDomain(wa, "green")

    expect_true(
        "WA current domain has only one value after pruning",
        len(csp.domains[wa]) == 1
    )

    csp.resetDomain(wa)

    expect_true(
        "WA domain reset restores all original values",
        csp.domains[wa] == csp.original_domains[wa]
    )

    expect_true(
        "WA domain reset uses a copied set, not the same set object",
        csp.domains[wa] is not csp.original_domains[wa]
    )

    csp.removeFromDomain(wa, "blue")
    csp.removeFromDomain(nt, "green")
    csp.removeFromDomain(sa, "red")

    expect_false("WA missing blue before resetAllDomains", "blue" in csp.domains[wa])
    expect_false("NT missing green before resetAllDomains", "green" in csp.domains[nt])
    expect_false("SA missing red before resetAllDomains", "red" in csp.domains[sa])

    csp.resetAllDomains()

    expect_true(
        "WA restored by resetAllDomains",
        csp.domains[wa] == csp.original_domains[wa]
    )

    expect_true(
        "NT restored by resetAllDomains",
        csp.domains[nt] == csp.original_domains[nt]
    )

    expect_true(
        "SA restored by resetAllDomains",
        csp.domains[sa] == csp.original_domains[sa]
    )

    print_section("Assignment Tests")

    csp.assign(wa, "red")
    expect_true("WA assigned to red", csp.assignments[wa] == "red")

    expect_error(
        "Cannot assign WA twice",
        lambda: csp.assign(wa, "green")
    )

    expect_error(
        "Cannot assign value outside domain",
        lambda: csp.assign(nt, "purple")
    )

    csp.unassign(wa)
    expect_true("WA unassigned", wa not in csp.assignments)

    expect_error(
        "Cannot unassign WA twice",
        lambda: csp.unassign(wa)
    )

    print_section("Unary Constraint Tests")

    # WA cannot be red
    csp.addUnaryConstraint(wa, lambda color: color != "red")

    expect_false(
        "WA = red violates unary constraint",
        csp.isConsistent(wa, "red")
    )

    expect_true(
        "WA = green satisfies unary constraint",
        csp.isConsistent(wa, "green")
    )

    print_section("Binary Constraint Tests")

    # Adjacent regions cannot have the same color
    csp.addBinaryConstraint(wa, nt, lambda a, b: a != b)
    csp.addBinaryConstraint(wa, sa, lambda a, b: a != b)
    csp.addBinaryConstraint(nt, sa, lambda a, b: a != b)
    csp.addBinaryConstraint(sa, q, lambda a, b: a != b)

    csp.assign(wa, "green")

    expect_false(
        "NT = green conflicts with WA = green",
        csp.isConsistent(nt, "green")
    )

    expect_true(
        "NT = blue is consistent with WA = green",
        csp.isConsistent(nt, "blue")
    )

    csp.unassign(wa)

    print_section("N-ary Constraint Tests")

    # Artificial n-ary constraint:
    # WA, NT, and SA cannot all be different.
    csp.addNaryConstraint(
        [wa, nt, sa],
        lambda wa_color, nt_color, sa_color:
            len({wa_color, nt_color, sa_color}) < 3
    )

    csp.assign(wa, "red")
    csp.assign(nt, "green")

    expect_false(
        "SA = blue makes WA/NT/SA all different",
        csp.isConsistent(sa, "blue")
    )

    expect_true(
        "SA = red does not make all three different",
        csp.isConsistent(sa, "red")
    )

    csp.unassign(wa)
    csp.unassign(nt)

    print_section("Constraint Lookup Tests")

    wa_constraints = csp.getConstraintsFor(wa)
    nt_constraints = csp.getConstraintsFor(nt)
    q_constraints = csp.getConstraintsFor(q)

    print(f"WA constraints: {len(wa_constraints)}")
    print(f"NT constraints: {len(nt_constraints)}")
    print(f"Q constraints: {len(q_constraints)}")

    expect_true("WA has constraints", len(wa_constraints) > 0)
    expect_true("Q has at least one constraint", len(q_constraints) > 0)

    print_section("MRV / Degree Heuristic Test")

    selected = csp.selectUnassignedVariable()

    print(f"Selected variable: {selected.name}")

    expect_true(
        "selectUnassignedVariable returns an unassigned variable",
        selected not in csp.assignments
    )

    print_section("Neighbor Tests")

    csp.addNeighbors(wa, nt)
    csp.addNeighbors(wa, sa)
    csp.addNeighbors(nt, sa)
    csp.addNeighbors(sa, q)

    print("Neighbors:")
    for var in csp.variables:
        neighbor_names = [n.name for n in csp.neighbors[var]]
        print(f"  {var.name}: {neighbor_names}")

    expect_true("WA has NT as neighbor", nt in csp.neighbors[wa])
    expect_true("NT has WA as neighbor", wa in csp.neighbors[nt])
    expect_true("SA has Q as neighbor", q in csp.neighbors[sa])
    expect_true("Q has SA as neighbor", sa in csp.neighbors[q])

    expect_error(
        "Cannot make WA its own neighbor",
        lambda: csp.addNeighbors(wa, wa)
    )

    expect_error(
        "Cannot duplicate WA/NT neighbor relationship",
        lambda: csp.addNeighbors(wa, nt)
    )

    print_section("Directed Neighbor Test")

    directed_csp = CSP()

    a = directed_csp.addVariable("A", [1, 2, 3])
    b = directed_csp.addVariable("B", [1, 2, 3])

    directed_csp.addNeighbors(a, b, symmetric=False)

    expect_true("A has B as directed neighbor", b in directed_csp.neighbors[a])
    expect_false("B does not have A as directed neighbor", a in directed_csp.neighbors[b])

    print_section("Final State")

    print(f"Variables: {[v.name for v in csp.variables]}")
    print(f"Assignments: {csp.assignments}")
    print(f"Constraint count: {len(csp.constraints)}")
    print(f"Neighbor count: {sum(len(v) for v in csp.neighbors.values())}")

    print("\nDemo completed.")


if __name__ == "__main__":
    main()