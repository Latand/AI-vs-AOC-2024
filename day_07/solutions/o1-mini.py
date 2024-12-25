import itertools
import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_line(line):
    """
    Parses a single line of input.
    Returns the test value and the list of numbers.
    """
    test_value_part, numbers_part = line.split(":")
    test_value = int(test_value_part.strip())
    numbers = list(map(int, numbers_part.strip().split()))
    return test_value, numbers


def part1(data: str) -> int:
    """
    Solution for part 1:
    Insert '+' and '*' operators between numbers to match the test value.
    Operators are evaluated left-to-right.
    Sum the test values of all equations that can be made true.
    """
    total_calibration = 0
    lines = data.splitlines()

    for line in lines:
        test_value, numbers = parse_line(line)
        if can_make_test_value_part1(numbers, test_value):
            total_calibration += test_value

    return total_calibration


def can_make_test_value_part1(numbers, test_value):
    """
    Determines if any combination of '+' and '*' operators between the numbers
    results in the test_value when evaluated left-to-right.
    """
    operators = ["+", "*"]
    num_operators = len(numbers) - 1
    for ops in itertools.product(operators, repeat=num_operators):
        result = numbers[0]
        for op, num in zip(ops, numbers[1:]):
            if op == "+":
                result += num
            elif op == "*":
                result *= num
        if result == test_value:
            return True
    return False


def part2(data: str) -> int:
    """
    Solution for part 2:
    Insert '+', '*', and '||' operators between numbers to match the test value.
    Operators are evaluated left-to-right.
    Sum the test values of all equations that can be made true.
    """
    total_calibration = 0
    lines = data.splitlines()

    for line in lines:
        test_value, numbers = parse_line(line)
        if can_make_test_value_part2(numbers, test_value):
            total_calibration += test_value

    return total_calibration


def can_make_test_value_part2(numbers, test_value):
    """
    Determines if any combination of '+', '*', and '||' operators between the numbers
    results in the test_value when evaluated left-to-right.
    """
    operators = ["+", "*", "||"]
    num_operators = len(numbers) - 1
    for ops in itertools.product(operators, repeat=num_operators):
        try:
            result = numbers[0]
            for op, num in zip(ops, numbers[1:]):
                if op == "+":
                    result += num
                elif op == "*":
                    result *= num
                elif op == "||":
                    # Concatenate digits: e.g., 12 || 345 = 12345
                    result = int(f"{result}{num}")
            if result == test_value:
                return True
        except:
            # In case of any errors (e.g., invalid concatenation), skip this combination
            continue
    return False


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
