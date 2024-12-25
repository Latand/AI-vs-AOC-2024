import re
from typing import List, Tuple
from itertools import product


def read_input() -> str:
    with open("../input.txt") as f:
        return f.read().strip()


def parse_line(line: str) -> Tuple[int, List[int]]:
    """Parse a line into test value and numbers."""
    test_value, numbers = line.split(": ")
    return int(test_value), [int(x) for x in numbers.split()]


def evaluate_expression(numbers: List[int], operators: List[str]) -> int:
    """
    Evaluate an expression with the given numbers and operators.
    Operators are evaluated left-to-right.
    """
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        elif op == "*":
            result *= numbers[i + 1]
        elif op == "||":
            # Concatenation operator
            result = int(str(result) + str(numbers[i + 1]))
    return result


def find_valid_combinations(
    test_value: int, numbers: List[int], use_concat: bool = False
) -> bool:
    """
    Find if there exists any combination of operators that produces the test value.
    """
    operators = ["+", "*"] if not use_concat else ["+", "*", "||"]
    # We need len(numbers) - 1 operators
    for ops in product(operators, repeat=len(numbers) - 1):
        if evaluate_expression(numbers, ops) == test_value:
            return True
    return False


def part1(data: str) -> int:
    """
    Solution for part 1: Find sum of test values that can be achieved using + and *
    """
    total = 0
    for line in data.splitlines():
        test_value, numbers = parse_line(line)
        if find_valid_combinations(test_value, numbers):
            total += test_value
    return total


def part2(data: str) -> int:
    """
    Solution for part 2: Find sum of test values that can be achieved using +, *, and ||
    """
    total = 0
    for line in data.splitlines():
        test_value, numbers = parse_line(line)
        if find_valid_combinations(test_value, numbers, use_concat=True):
            total += test_value
    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
