from csp.csp import CSP
from csp.backtracking import backtracking, backtracking_all
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


def nqueensprint(csp):
    return


def main():
    i = 20
    timed_run(f"nQueens n={i} | basic", nQueens, nqueensprint, i)
    timed_run(
        f"nQueens n={i} | forward checking", nQueens, nqueensprint, i, forwardCheck=True
    )
    timed_run(
        f"nQueens n={i} | forward checking + LCV",
        nQueens,
        nqueensprint,
        i,
        forwardCheck=True,
        lcv=True,
    )


if __name__ == "__main__":
    main()
