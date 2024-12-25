import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Scans the input data for valid mul(X,Y) instructions and sums their products.
    A valid mul instruction matches the pattern mul(X,Y) where X and Y are 1-3 digit numbers.
    """
    # Regular expression to match 'mul(X,Y)' where X and Y are 1-3 digit numbers
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    matches = pattern.findall(data)

    total = 0
    for x, y in matches:
        product = int(x) * int(y)
        total += product

    return total


def part2(data: str) -> int:
    """
    Scans the input data sequentially for mul(X,Y), do(), and don't() instructions.
    Maintains a flag to enable or disable mul instructions based on do() and don't().
    Sums the products of enabled mul(X,Y) instructions.
    """
    # Regular expression to match 'mul(X,Y)', 'do()', or "don't()"
    # Using non-capturing groups for the instruction types
    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)")

    total = 0
    mul_enabled = True  # Initially, mul instructions are enabled

    # Iterate over all matches in the order they appear
    for match in pattern.finditer(data):
        mul_x, mul_y = match.group(1), match.group(2)
        instruction = match.group(0)

        if mul_x and mul_y:
            if mul_enabled:
                product = int(mul_x) * int(mul_y)
                total += product
        elif instruction == "do()":
            mul_enabled = True
        elif instruction == "don't()":
            mul_enabled = False
        # Ignore any other instructions or malformed matches

    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
