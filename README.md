# Constraint Satisfaction Problems

This repository is an educational implementation of a small Constraint Satisfaction Problem (CSP) framework in Python.

It is intended for learning, experimentation, and demonstrating core CSP concepts rather than serving as a production-ready solver. The code favors readability and explicit algorithm structure over heavy optimization.

## What is included

The project currently includes:

- A generic `CSP` class for defining variables, domains, assignments, constraints, and neighbors
- Unary, binary, and n-ary constraints
- Backtracking search
- MRV-style variable selection using current domain size
- Degree heuristic tie-breaking using constraint count
- Least Constraining Value (LCV) ordering
- Forward checking
- AC-3 arc consistency
- MAC-style solving by running AC-3 during backtracking
- All-solutions backtracking
- Demo programs for testing CSP behavior and solver behavior
- Example CSPs such as map coloring and N-Queens

## Educational purpose

This project was created to better understand the algorithms behind CSP solving, especially topics commonly covered in AI courses:

- Backtracking search
- Constraint propagation
- Forward checking
- Arc consistency
- AC-3
- Maintaining Arc Consistency (MAC)
- Variable and value ordering heuristics

The implementation is intentionally transparent. Many operations that a highly optimized solver would compress or specialize are written in a direct way so the algorithmic steps are easier to inspect and modify.

## Repository structure

```text
csp/
  csp.py              Core CSP data structures and constraint logic
  backtracking.py     Backtracking, forward checking, AC-3, and all-solution search
  util.py             Demo/test helpers and timing utility

tests/
  demoCSP.py          Explicit regression/demo checks for the CSP class
  demoBacktracking.py Explicit regression/demo checks for the solvers

examples/
  nQueens.py          N-Queens CSP example and benchmark/demo
```

## Running the demos

From the repository root:

```bash
python3 -m tests.demoCSP
python3 -m tests.demoBacktracking
python3 -m examples.nQueens
```

The `tests/demo*.py` scripts print simple pass/fail checks and are meant to explicitly exercise the base functionality of the CSP class and solver implementations. They are lightweight regression/demo checks rather than a formal unit test suite.

The `examples/` directory is for problem-specific demonstrations, such as N-Queens, that use the generic CSP framework.

## Example: choosing a solver mode

The backtracking solver supports several inference modes:

```python
backtracking(csp, inference="none")
backtracking(csp, inference="forward_check")
backtracking(csp, inference="ac3")
```

LCV can be enabled separately:

```python
backtracking(csp, inference="forward_check", lcv=True)
backtracking(csp, inference="ac3", lcv=True)
```

To enumerate all solutions instead of stopping at the first one:

```python
backtracking_all(csp, inference="none")
backtracking_all(csp, inference="forward_check")
backtracking_all(csp, inference="ac3")
```

## Notes on AC-3

The AC-3 implementation is currently focused on binary constraints. The CSP class supports n-ary constraints, and normal backtracking consistency checks still enforce them, but AC-3 pruning itself only reasons directly over binary arcs.

This matches the standard introductory version of AC-3 and keeps the implementation easier to study.

## Performance expectations

This solver is built for clarity, not maximum speed. Some heuristics can make certain examples slower because they add bookkeeping overhead. For example, LCV may reduce the search space but still run slower if calculating prune counts costs more than the saved backtracking work.

That behavior is part of what this project is meant to demonstrate: heuristics are tradeoffs, not guaranteed speedups.

## Future improvements

Possible future additions:

- Formal unit tests with `pytest`
- Better instrumentation for node counts, consistency checks, prunes, and backtracks
- A cleaner inference-mode enum
- AC-3 preprocessing before search
- More CSP examples, such as Sudoku, graph coloring, and scheduling
- Min-conflicts local search
- Backjumping or nogood recording
- More efficient queue handling with `collections.deque`

## License

No license has been selected yet. Add one before reusing or distributing this code more broadly.
