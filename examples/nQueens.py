from csp.csp import CSP
from csp.backtracking import backtracking, backtracking_all
from csp.util import timed_run


def nQueens(n: int, inference="none", lcv=False):
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
    return backtracking(c, inference=inference, lcv=lcv)


def nqueensprint(csp):
    return


def main():
    i = 20
    timed_run(f"nQueens n={i} | basic", nQueens, nqueensprint, i)
    timed_run(
        f"nQueens n={i} | forward checking",
        nQueens,
        nqueensprint,
        i,
        inference="forward_check",
    )
    timed_run(
        f"nQueens n={i} | forward checking + LCV",
        nQueens,
        nqueensprint,
        i,
        inference="forward_check",
        lcv=True,
    )
    timed_run(
        f"nQueens n={i} | AC-3 + LCV",
        nQueens,
        nqueensprint,
        i,
        inference="ac3",
        lcv=True,
    )


if __name__ == "__main__":
    main()
