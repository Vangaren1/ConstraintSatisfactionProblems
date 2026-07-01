from csp import CSP
from csp.backtracking import backtracking


def nQueens(n: int):
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
    return backtracking(c)


def main():
    for i in range(20):
        print(f"n = {i}")
        print(nQueens(i))
    pass


if __name__ == "__main__":
    main()
