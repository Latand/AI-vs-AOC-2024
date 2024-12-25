import itertools
from typing import List, Tuple


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def evaluate_expression(numbers: List[int], operators: List[str]) -> int:
    """
    Evaluate the expression formed by inserting the given operators between numbers.
    Operators are evaluated left-to-right.
    """
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        elif op == "*":
            result *= numbers[i + 1]
        elif op == "||":
            result = int(str(result) + str(numbers[i + 1]))
    return result


def valid_combinations(target: int, numbers: List[int]) -> bool:
    """
    Check if any combination of operators can produce the target value from the numbers.
    """
    num_operators = len(numbers) - 1
    for ops in itertools.product(["+", "*", "||"], repeat=num_operators):
        try:
            if evaluate_expression(numbers, ops) == target:
                return True
        except ValueError:
            continue
    return False


def parse_line(line: str) -> Tuple[int, List[int]]:
    """Parse a single line into target and numbers."""
    target, nums = line.split(": ")
    return int(target), list(map(int, nums.split()))


def part1(data: List[str]) -> int:
    """Solve part 1 of the challenge."""
    total = 0
    for line in data:
        target, numbers = parse_line(line)
        if valid_combinations(target, numbers):
            total += target
    return total


def part2(data: List[str]) -> int:
    """Solve part 2 of the challenge."""
    total = 0
    for line in data:
        target, numbers = parse_line(line)
        if valid_combinations(target, numbers):
            total += target
    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
