from itertools import product
from typing import List, Tuple


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().split("\n")


def evaluate_expression(nums: List[int], operators: List[str]) -> int:
    """
    Evaluate an expression with given numbers and operators.
    Operators are applied left-to-right.
    Supports +, *, ||
    """
    result = nums[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += nums[i + 1]
        elif op == "*":
            result *= nums[i + 1]
        elif op == "||":
            result = int(str(result) + str(nums[i + 1]))
    return result


def find_valid_equations(line: str, operators: List[str]) -> List[int]:
    """
    Find valid equations for a given line with specified operators.
    """
    # Parse the line
    test_val, nums_str = line.split(": ")
    test_val = int(test_val)
    nums = list(map(int, nums_str.split()))

    # Only generate operators for spaces between numbers
    valid_solutions = []

    # Generate all possible operator combinations
    for op_combo in product(operators, repeat=len(nums) - 1):
        try:
            result = evaluate_expression(nums, list(op_combo))
            if result == test_val:
                valid_solutions.append(test_val)
        except Exception:
            # Skip any invalid expressions
            continue

    return valid_solutions


def part1(data: List[str]) -> int:
    """
    Solve Part 1 with + and * operators
    """
    operators = ["+", "*"]
    return sum(
        solution for line in data for solution in find_valid_equations(line, operators)
    )


def part2(data: List[str]) -> int:
    """
    Solve Part 2 with +, *, and || operators
    """
    operators = ["+", "*", "||"]
    return sum(
        solution for line in data for solution in find_valid_equations(line, operators)
    )


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
