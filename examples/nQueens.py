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


def main():
    timed_run("nQueens n=20 | basic", nQueens, 20)
    timed_run("nQueens n=20 | forward checking", nQueens, 20, forwardCheck=True)
    timed_run(
        "nQueens n=20 | forward checking + LCV",
        nQueens,
        20,
        forwardCheck=True,
        lcv=True,
    )


if __name__ == "__main__":
    main()
