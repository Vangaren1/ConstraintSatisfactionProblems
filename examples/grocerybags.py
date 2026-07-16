from csp.csp import CSP
from csp.backtracking import backtracking, backtracking_all
from csp.util import timed_run, print_section, expect_true


def groceryBags(items: list[int], capacity: int, bagCount: int):
    csp = CSP()

    itemList = [i for i in range(len(items))]
    bags = [i for i in range(bagCount)]

    for index, weight in enumerate(items):
        csp.addVariable(index, bags)

    def bagCap(*assignedBags):
        loads = [0 for _ in range(bagCount)]

        for itemIndex, bag in enumerate(assignedBags):
            loads[bag] += items[itemIndex]

            if loads[bag] > capacity:
                return False

        return True

    csp.addNaryConstraint(itemList, bagCap)

    return csp


def minGroceryBags(items: list[int], capacity: int, inference="none", lcv=False):
    if len(items) == 0:
        return None, 0
    if max(items) > capacity:
        return None, None
    totalWeight = sum(items)

    lower = (totalWeight + capacity - 1) // capacity
    upper = len(items)

    for num_bags in range(lower, upper + 1):
        csp = groceryBags(items, capacity, num_bags)
        result = backtracking(csp, inference=inference, lcv=lcv)

        if result is not None:
            return result, num_bags

    return None, None


def canFitInBags(items: list[int], capacity: int, bagCount: int) -> bool:
    csp = groceryBags(items, capacity, bagCount)
    result = backtracking(csp)
    return result is not None


def test_grocery_bag_cases():
    print_section("Grocery Bag CSP Cases")

    cases = [
        # items, capacity, bagCount, expectedResult
        ([6, 4, 5, 5], 10, 2, True),  # 6+4, 5+5
        ([6, 6, 6], 10, 2, False),  # each 6 needs its own bag
        ([2, 3, 4], 10, 1, True),  # total 9
        ([8, 8, 4], 10, 2, False),  # total 20 but cannot pair 4 with either 8
        ([8, 8, 4], 10, 3, True),  # each 8 alone, 4 alone
        ([10, 10, 10], 10, 3, True),  # exact one per bag
        ([10, 10, 10], 10, 2, False),  # total capacity too small
        ([11], 10, 1, False),  # item exceeds capacity
        ([], 10, 0, True),  # no items need no bags
        ([], 10, 1, True),  # no items fit trivially
        ([6, 4] * 4, 10, 4, True),
        ([6, 4] * 4, 10, 3, False),
    ]

    for index, (items, capacity, bagCount, expected) in enumerate(cases, start=1):
        actual = canFitInBags(items, capacity, bagCount)

        expect_true(
            f"case {index}: items={items}, capacity={capacity}, bags={bagCount} -> {expected}",
            actual == expected,
        )


if __name__ == "__main__":
    test_grocery_bag_cases()
