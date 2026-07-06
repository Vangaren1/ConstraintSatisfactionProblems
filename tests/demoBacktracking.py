# demoBacktracking.py

from csp.csp import CSP
from csp.backtracking import backtracking, backtracking_all, ac3
from csp.util import print_section, expect_true, expect_none, expect_not_none, expect_error


def expect_equal(description, actual, expected):
    if actual == expected:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}: expected {expected}, got {actual}")


def assignment_dict(csp):
    return {var.name: value for var, value in csp.assignments.items()}


def solution_dict(solution):
    return {var.name: value for var, value in solution.items()}


def print_assignments(csp):
    if csp is None:
        print("No solution.")
        return

    print("Assignments:")
    for var in sorted(csp.assignments, key=lambda v: str(v.name)):
        print(f"  {var.name} = {csp.assignments[var]}")


def is_fully_assigned(csp):
    return csp is not None and len(csp.assignments) == len(csp.variables)


def assert_clean_domains(csp):
    for var in csp.variables:
        if csp.domains[var] != csp.original_domains[var]:
            print(
                f"[FAIL] Domain restored for {var.name}: "
                f"expected {csp.original_domains[var]}, got {csp.domains[var]}"
            )
            return
    print("[PASS] Domains restored after search")


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


def build_two_variable_not_equal_csp():
    csp = CSP()

    a = csp.addVariable("A", [1, 2])
    b = csp.addVariable("B", [1, 2])

    csp.addBinaryConstraint(a, b, lambda x, y: x != y)

    return csp


def build_ac3_chain_csp():
    csp = CSP()

    a = csp.addVariable("A", [1, 2, 3])
    b = csp.addVariable("B", [1, 2, 3])
    c = csp.addVariable("C", [2, 3])

    csp.addBinaryConstraint(a, b, lambda av, bv: av < bv)
    csp.addBinaryConstraint(b, c, lambda bv, cv: bv < cv)

    return csp, a, b, c


def assert_map_coloring_solution(result):
    expect_not_none("Map coloring has a solution", result)
    expect_true("All variables assigned", is_fully_assigned(result))

    if result is None:
        return

    assignments = assignment_dict(result)

    expect_true("WA != NT", assignments["WA"] != assignments["NT"])
    expect_true("WA != SA", assignments["WA"] != assignments["SA"])
    expect_true("NT != SA", assignments["NT"] != assignments["SA"])
    expect_true("SA != Q", assignments["SA"] != assignments["Q"])

    print_assignments(result)


def test_default_inference_argument():
    print_section("Default Inference Argument")

    csp = build_map_coloring_csp()

    try:
        result = backtracking(csp)
        assert_map_coloring_solution(result)
    except Exception as e:
        print(f"[FAIL] backtracking(csp) should use inference='none': {type(e).__name__}: {e}")


def test_invalid_inference_argument():
    print_section("Invalid Inference Argument")

    expect_error(
        "Invalid inference mode rejected",
        lambda: backtracking(build_map_coloring_csp(), inference="forwardCheck"),
    )


def test_map_coloring_modes():
    for inference, lcv in (
        ("none", False),
        ("forward_check", False),
        ("forward_check", True),
        ("ac3", False),
        ("ac3", True),
    ):
        label = f"Map Coloring - inference={inference}, lcv={lcv}"
        print_section(label)

        csp = build_map_coloring_csp()
        result = backtracking(csp, inference=inference, lcv=lcv)

        assert_map_coloring_solution(result)


def test_unsatisfiable_binary_modes():
    for inference in ("none", "forward_check", "ac3"):
        print_section(f"Unsatisfiable Binary CSP - inference={inference}")

        csp = build_unsatisfiable_binary_csp()
        result = backtracking(csp, inference=inference)

        expect_none("Solver returns None", result)
        assert_clean_domains(csp)


def test_unary_constraint():
    print_section("Unary Constraint CSP")

    csp = build_unary_csp()
    result = backtracking(csp, inference="none")

    expect_not_none("Unary CSP has a solution", result)
    expect_true("All variables assigned", is_fully_assigned(result))

    if result is None:
        return

    assignments = assignment_dict(result)

    expect_equal("X must be even", assignments["X"], 2)

    print_assignments(result)


def test_nary_sum_modes():
    for inference in ("none", "forward_check", "ac3"):
        print_section(f"N-ary Sum CSP - inference={inference}")

        csp = build_nary_sum_csp()
        result = backtracking(csp, inference=inference)

        expect_not_none("N-ary sum CSP has a solution", result)
        expect_true("All variables assigned", is_fully_assigned(result))

        if result is None:
            continue

        assignments = assignment_dict(result)

        expect_equal(
            "A + B + C == 6",
            assignments["A"] + assignments["B"] + assignments["C"],
            6,
        )

        print_assignments(result)


def test_unsatisfiable_nary():
    print_section("Unsatisfiable N-ary CSP")

    csp = build_unsatisfiable_nary_csp()
    result = backtracking(csp, inference="none")

    expect_none("Impossible n-ary CSP returns None", result)


def test_backtracking_all_modes():
    for inference in ("none", "forward_check", "ac3"):
        print_section(f"All Solutions - inference={inference}")

        csp = build_two_variable_not_equal_csp()
        solutions = backtracking_all(csp, inference=inference)
        normalized = [solution_dict(solution) for solution in solutions]
        normalized_set = {tuple(sorted(solution.items())) for solution in normalized}

        print(f"Solutions: {normalized}")

        expect_equal("Two valid assignments found", len(solutions), 2)
        expect_true("Solution A=1, B=2 found", tuple(sorted({"A": 1, "B": 2}.items())) in normalized_set)
        expect_true("Solution A=2, B=1 found", tuple(sorted({"A": 2, "B": 1}.items())) in normalized_set)
        assert_clean_domains(csp)


def test_ac3_chain_pruning():
    print_section("AC-3 Chain Pruning")

    csp, a, b, c = build_ac3_chain_csp()

    failed, pruned = ac3(csp)

    print(f"Failed: {failed}")
    print(f"Pruned: {[(var.name, value) for var, value in pruned]}")
    print(f"Domains: A={csp.domains[a]}, B={csp.domains[b]}, C={csp.domains[c]}")

    expect_true("AC-3 succeeds", not failed)
    expect_equal("A domain pruned to {1}", csp.domains[a], {1})
    expect_equal("B domain pruned to {2}", csp.domains[b], {2})
    expect_equal("C domain pruned to {3}", csp.domains[c], {3})


def test_ac3_detects_failure():
    print_section("AC-3 Detects Failure")

    csp = CSP()
    a = csp.addVariable("A", [2])
    b = csp.addVariable("B", [1])

    csp.addBinaryConstraint(a, b, lambda av, bv: av < bv)

    failed, pruned = ac3(csp)

    print(f"Failed: {failed}")
    print(f"Pruned: {[(var.name, value) for var, value in pruned]}")

    expect_true("AC-3 reports failure", failed)
    expect_true("At least one domain is empty", len(csp.domains[a]) == 0 or len(csp.domains[b]) == 0)


def main():
    test_default_inference_argument()
    test_invalid_inference_argument()

    test_map_coloring_modes()
    test_unsatisfiable_binary_modes()

    test_unary_constraint()
    test_nary_sum_modes()
    test_unsatisfiable_nary()

    test_backtracking_all_modes()

    test_ac3_chain_pruning()
    test_ac3_detects_failure()

    print_section("Demo Complete")
    print("Backtracking demo completed.")


if __name__ == "__main__":
    main()
