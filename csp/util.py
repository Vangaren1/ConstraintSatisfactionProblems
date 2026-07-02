from time import perf_counter


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


def expect_none(description, value):
    if value is None:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}: expected None, got {value}")


def expect_not_none(description, value):
    if value is not None:
        print(f"[PASS] {description}")
    else:
        print(f"[FAIL] {description}: expected solution, got None")


def names(items):
    return sorted(item.name for item in items)


def timed_run(label, func, cspPrintFunc=None, *args, **kwargs):
    start = perf_counter()
    result = func(*args, **kwargs)
    elapsed = perf_counter() - start
    if cspPrintFunc is not None:
        cspPrintFunc(result)
    print(f"{label}: {elapsed:.6f} seconds")
    return result
