from csp.csp import CSP
from csp.backtracking import backtracking, backtracking_all
from csp.util import timed_run, print_section


def nQueens(n: int, inference="none", lcv=False, solver=backtracking):
    c = CSP()

    domain = [i for i in range(n)]
    for i in range(n):
        c.addVariable(i, domain)
    for y in range(n):
        for x in range(y + 1, n):
            if x != y:
                c.addBinaryConstraint(x, y, lambda a, b: a != b)
                c.addBinaryConstraint(
                    x, y, lambda a, b, x=x, y=y: abs(x - y) != abs(a - b)
                )
    return solver(c, inference=inference, lcv=lcv)


def nqueensprint(csp: CSP):
    assignments = csp.assignments
    rows = sorted((var.name, col) for var, col in assignments.items())
    n = len(rows)
    grid = [["-" for _ in range(n)] for _ in range(n)]
    for row, col in rows:
        grid[row][col] = "Q"

    for row in grid:
        print(row)


def printQueenSolutions(solutions):
    print(f"Solutions found: {len(solutions)}")

    if not solutions:
        return

    # Print only the first solution so output stays readable.
    solution = solutions[0]
    rows = sorted((var.name, col) for var, col in solution.items())
    n = len(rows)

    grid = [["-" for _ in range(n)] for _ in range(n)]

    for row, col in rows:
        grid[row][col] = "Q"

    for row in grid:
        print(row)


def main():
    n = 20

    print_section("N-Queens | First Solution")

    timed_run(
        f"nQueens n={n} | basic",
        nQueens,
        nqueensprint,
        n,
    )

    timed_run(
        f"nQueens n={n} | forward checking",
        nQueens,
        nqueensprint,
        n,
        inference="forward_check",
    )

    timed_run(
        f"nQueens n={n} | forward checking + LCV",
        nQueens,
        nqueensprint,
        n,
        inference="forward_check",
        lcv=True,
    )

    timed_run(
        f"nQueens n={n} | AC-3",
        nQueens,
        nqueensprint,
        n,
        inference="ac3",
    )

    timed_run(
        f"nQueens n={n} | AC-3 + LCV",
        nQueens,
        nqueensprint,
        n,
        inference="ac3",
        lcv=True,
    )

    all_n = 8

    print_section("N-Queens | All Solutions")

    timed_run(
        f"nQueens n={all_n} | all solutions | basic",
        nQueens,
        printQueenSolutions,
        all_n,
        solver=backtracking_all,
    )

    timed_run(
        f"nQueens n={all_n} | all solutions | forward checking",
        nQueens,
        printQueenSolutions,
        all_n,
        inference="forward_check",
        solver=backtracking_all,
    )

    timed_run(
        f"nQueens n={all_n} | all solutions | forward checking + LCV",
        nQueens,
        printQueenSolutions,
        all_n,
        inference="forward_check",
        lcv=True,
        solver=backtracking_all,
    )

    timed_run(
        f"nQueens n={all_n} | all solutions | AC-3",
        nQueens,
        printQueenSolutions,
        all_n,
        inference="ac3",
        solver=backtracking_all,
    )

    timed_run(
        f"nQueens n={all_n} | all solutions | AC-3 + LCV",
        nQueens,
        printQueenSolutions,
        all_n,
        inference="ac3",
        lcv=True,
        solver=backtracking_all,
    )


if __name__ == "__main__":
    main()
