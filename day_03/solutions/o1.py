import re


def read_input():
    """
    Reads the puzzle input from ../input.txt
    """
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Part 1:
    Find all valid mul(X,Y) instructions where X and Y are each 1-3 digit numbers.
    Sum the products of all such instructions, ignoring everything else.
    """
    # Regex to match mul( X, Y ) where X, Y are 1-3 digit numbers
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, data)
    total = 0

    for x_str, y_str in matches:
        x = int(x_str)
        y = int(y_str)
        total += x * y

    return total


def part2(data: str) -> int:
    """
    Part 2:
    In addition to the mul(X,Y) instructions from Part 1,
    handle do() and don't() instructions that enable or disable
    processing of subsequent mul instructions.

    Initially, mul instructions are enabled.
    Only the most recent do() or don't() applies.
    """
    pattern = r"(do\(\)|don't\(\)|mul\(\d{1,3},\d{1,3}\))"
    total = 0
    enabled = True  # At the beginning, mul instructions are enabled.

    for match in re.finditer(pattern, data):
        token = match.group(0)

        if token == "do()":
            enabled = True
        elif token == "don't()":
            enabled = False
        else:
            # It's a valid mul(...) instruction
            # Extract the numbers inside mul(...)
            mul_match = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", token)
            if mul_match:
                x = int(mul_match.group(1))
                y = int(mul_match.group(2))
                if enabled:
                    total += x * y

    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
