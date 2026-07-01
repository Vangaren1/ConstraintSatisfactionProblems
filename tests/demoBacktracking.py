# demoBacktracking.py

from csp import CSP
from csp.backtracking import backtracking
from tests.util import print_section, expect_true, expect_none, expect_not_none


def assignment_dict(csp):
    return {var.name: value for var, value in csp.assignments.items()}


def print_assignments(csp):
    if csp is None:
        print("No solution.")
        return

    print("Assignments:")
    for var in sorted(csp.assignments, key=lambda v: v.name):
        print(f"  {var.name} = {csp.assignments[var]}")


def is_fully_assigned(csp):
    return csp is not None and len(csp.assignments) == len(csp.variables)


def build_map_coloring_csp():
    csp = CSP()

    wa = csp.addVariable("WA", ["red", "green", "blue"])
    nt = csp.addVariable("NT", ["red", "green", "blue"])
    sa = csp.addVariable("SA", ["red", "green", "blue"])
    q = csp.addVariable("Q", ["red", "green", "blue"])

    csp.addBinaryConstraint(wa, nt, lambda a, b: a != b)
    csp.addBinaryConstraint(wa, sa, lambda a, b: a != b)
    csp.addBinaryConstraint(nt, sa, lambda a, b: a != b)
    csp.addBinaryConstraint(sa, q, lambda a, b: a != b)

    return csp


def build_unsatisfiable_binary_csp():
    csp = CSP()

    a = csp.addVariable("A", [1])
    b = csp.addVariable("B", [1])

    csp.addBinaryConstraint(a, b, lambda x, y: x != y)

    return csp


def build_unary_csp():
    csp = CSP()

    x = csp.addVariable("X", [1, 2, 3])
    csp.addUnaryConstraint(x, lambda value: value % 2 == 0)

    return csp


def build_nary_sum_csp():
    csp = CSP()

    a = csp.addVariable("A", [1, 2, 3])
    b = csp.addVariable("B", [1, 2, 3])
    c = csp.addVariable("C", [1, 2, 3])

    csp.addNaryConstraint([a, b, c], lambda x, y, z: x + y + z == 6)

    return csp


def build_unsatisfiable_nary_csp():
    csp = CSP()

    a = csp.addVariable("A", [1])
    b = csp.addVariable("B", [1])
    c = csp.addVariable("C", [1])

    csp.addNaryConstraint([a, b, c], lambda x, y, z: x + y + z == 4)

    return csp


def build_lcv_demo_csp():
    csp = CSP()

    x = csp.addVariable("X", [1, 2, 3])
    y = csp.addVariable("Y", [1, 2, 3])
    z = csp.addVariable("Z", [1, 2, 3])

    csp.addBinaryConstraint(x, y, lambda xv, yv: not (xv == 1 and yv == 1))
    csp.addBinaryConstraint(x, y, lambda xv, yv: not (xv == 2 and yv == 2))
    csp.addBinaryConstraint(x, z, lambda xv, zv: not (xv == 2 and zv == 2))
    csp.addBinaryConstraint(x, z, lambda xv, zv: not (xv == 3 and zv == 3))

    return csp, x


def assert_map_coloring_solution(result):
    expect_not_none("Map coloring has a solution", result)
    expect_true("All variables assigned", is_fully_assigned(result))

    assignments = assignment_dict(result)

    expect_true("WA != NT", assignments["WA"] != assignments["NT"])
    expect_true("WA != SA", assignments["WA"] != assignments["SA"])
    expect_true("NT != SA", assignments["NT"] != assignments["SA"])
    expect_true("SA != Q", assignments["SA"] != assignments["Q"])

    print_assignments(result)


def test_plain_backtracking_map_coloring():
    print_section("Map Coloring - Plain Backtracking")

    csp = build_map_coloring_csp()
    result = backtracking(csp, forwardCheck=False, lcv=False)

    assert_map_coloring_solution(result)


def test_forward_checking_map_coloring():
    print_section("Map Coloring - Forward Checking")

    csp = build_map_coloring_csp()
    result = backtracking(csp, forwardCheck=True, lcv=False)

    assert_map_coloring_solution(result)


def test_forward_checking_with_lcv_map_coloring():
    print_section("Map Coloring - Forward Checking + LCV")

    csp = build_map_coloring_csp()
    result = backtracking(csp, forwardCheck=True, lcv=True)

    assert_map_coloring_solution(result)


def test_unsatisfiable_binary():
    print_section("Unsatisfiable Binary CSP")

    csp = build_unsatisfiable_binary_csp()
    result = backtracking(csp, forwardCheck=False, lcv=False)

    expect_none("Plain backtracking returns None", result)


def test_unsatisfiable_binary_forward_checking():
    print_section("Unsatisfiable Binary CSP - Forward Checking")

    csp = build_unsatisfiable_binary_csp()
    result = backtracking(csp, forwardCheck=True, lcv=False)

    expect_none("Forward checking returns None", result)


def test_unary_constraint():
    print_section("Unary Constraint CSP")

    csp = build_unary_csp()
    result = backtracking(csp)

    expect_not_none("Unary CSP has a solution", result)
    expect_true("All variables assigned", is_fully_assigned(result))

    assignments = assignment_dict(result)

    expect_true("X must be even", assignments["X"] == 2)

    print_assignments(result)


def test_nary_sum_plain():
    print_section("N-ary Sum CSP - Plain Backtracking")

    csp = build_nary_sum_csp()
    result = backtracking(csp, forwardCheck=False, lcv=False)

    expect_not_none("N-ary sum CSP has a solution", result)
    expect_true("All variables assigned", is_fully_assigned(result))

    assignments = assignment_dict(result)

    expect_true(
        "A + B + C == 6",
        assignments["A"] + assignments["B"] + assignments["C"] == 6,
    )

    print_assignments(result)


def test_nary_sum_forward_checking():
    print_section("N-ary Sum CSP - Forward Checking")

    csp = build_nary_sum_csp()
    result = backtracking(csp, forwardCheck=True, lcv=False)

    expect_not_none("N-ary sum CSP has a solution", result)
    expect_true("All variables assigned", is_fully_assigned(result))

    assignments = assignment_dict(result)

    expect_true(
        "A + B + C == 6",
        assignments["A"] + assignments["B"] + assignments["C"] == 6,
    )

    print_assignments(result)


def test_unsatisfiable_nary():
    print_section("Unsatisfiable N-ary CSP")

    csp = build_unsatisfiable_nary_csp()
    result = backtracking(csp, forwardCheck=False, lcv=False)

    expect_none("Impossible n-ary CSP returns None", result)


def test_lcv_ordering_used_by_csp():
    print_section("LCV Ordering Demonstration")

    csp, x = build_lcv_demo_csp()

    scores = [(value, csp.getPruneCount(x, value)) for value in csp.orderValues(x)]
    ordered = csp.orderValues(x, lcv=True)

    print(f"Prune scores: {scores}")
    print(f"LCV order: {ordered}")

    expect_true("Most constraining value 2 is last", ordered[-1] == 2)


def main():
    test_plain_backtracking_map_coloring()
    test_forward_checking_map_coloring()
    test_forward_checking_with_lcv_map_coloring()

    test_unsatisfiable_binary()
    test_unsatisfiable_binary_forward_checking()

    test_unary_constraint()

    test_nary_sum_plain()
    test_nary_sum_forward_checking()
    test_unsatisfiable_nary()

    test_lcv_ordering_used_by_csp()

    print_section("Demo Complete")
    print("Backtracking demo completed.")


if __name__ == "__main__":
    main()
