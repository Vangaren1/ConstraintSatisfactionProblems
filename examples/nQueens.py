from csp.csp import CSP
from csp.backtracking import backtracking
from csp.util import timed_run


def nQueens(n: int, forwardCheck=False, lcv=False):
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
    return backtracking(c, forwardCheck=forwardCheck, lcv=lcv)


def printQueenCSP(csp: CSP):
    rows = [(r.name, csp.assignments[r]) for r in csp.variables]
    rows.sort()
    n = len(rows)
    grid = [["-" for _ in range(n)] for _ in range(n)]
    for row, Q in rows:
        grid[row][Q] = "Q"
    for g in grid:
        print(g)


def main():

    n = 8

    timed_run(f"nQueens n={n} | basic", nQueens, printQueenCSP, n)
    timed_run(
        f"nQueens n={n} | forward checking",
        nQueens,
        printQueenCSP,
        n,
        forwardCheck=True,
    )
    timed_run(
        f"nQueens n={n} | forward checking + LCV",
        nQueens,
        printQueenCSP,
        n,
        forwardCheck=True,
        lcv=True,
    )


if __name__ == "__main__":
    main()
