from itertools import product
from typing import List, Set


def read_input() -> List[str]:
    with open("input.txt") as f:
        return f.read().strip().split("\n")


def evaluate_expression(nums: List[int], operators: List[str]) -> int:
    """Evaluate expression left-to-right with given operators."""
    result = nums[0]
    i = 0
    while i < len(operators):
        if operators[i] == "||":
            result = int(str(result) + str(nums[i + 1]))
        elif operators[i] == "+":
            result += nums[i + 1]
        else:  # multiplication
            result *= nums[i + 1]
        i += 1
    return result


def solve_equation(line: str, allowed_operators: Set[str]) -> bool:
    """Determine if an equation can be solved using the allowed operators."""
    test_value, nums_str = line.split(": ")
    test_value = int(test_value)
    nums = list(map(int, nums_str.split()))

    if len(nums) == 1:
        return nums[0] == test_value

    # Early termination checks
    if "||" in allowed_operators:
        # Check if concatenation of all numbers equals test value
        concat_all = int("".join(map(str, nums)))
        if concat_all == test_value:
            return True
    else:
        # If only + and * are allowed, we can do more aggressive pruning
        min_possible = nums[0]
        for num in nums[1:]:
            min_possible = min(min_possible + num, min_possible * num)
        if min_possible > test_value:
            return False

    for ops in product(allowed_operators, repeat=len(nums) - 1):
        try:
            if evaluate_expression(nums, list(ops)) == test_value:
                return True
        except ValueError:  # Handle potential overflow from concatenation
            continue
    return False


def part1(data: List[str]) -> int:
    """Solve part 1 of the puzzle - only + and * operators allowed."""
    return sum(
        int(line.split(": ")[0]) for line in data if solve_equation(line, {"+", "*"})
    )


def part2(data: List[str]) -> int:
    """Solve part 2 of the puzzle - +, *, and || operators allowed."""
    return sum(
        int(line.split(": ")[0])
        for line in data
        if solve_equation(line, {"+", "*", "||"})
    )


if __name__ == "__main__":
    data = read_input()
    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
