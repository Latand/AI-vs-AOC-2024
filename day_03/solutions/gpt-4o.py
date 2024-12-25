import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Find and sum all valid mul(X,Y) instructions in the corrupted memory.
    """
    # Regex to capture valid mul(X,Y) instructions
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")

    # Find all matches
    matches = mul_pattern.findall(data)

    # Sum the results of the multiplications
    return sum(int(x) * int(y) for x, y in matches)


def part2(data: str) -> int:
    """
    Handle do() and don't() instructions to enable or disable mul instructions,
    then sum the results of enabled multiplications.
    """
    # Regex to capture valid mul(X,Y) and do/don't instructions
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    do_pattern = re.compile(r"do\(\)")
    dont_pattern = re.compile(r"don't\(\)")

    # Initial state: mul instructions are enabled
    enabled = True
    total_sum = 0

    # Tokenize the input to process step-by-step
    tokens = re.finditer(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)", data)

    for token in tokens:
        if token.group().startswith("mul("):
            if enabled:
                x, y = map(int, token.groups())
                total_sum += x * y
        elif token.group() == "do()":
            enabled = True
        elif token.group() == "don't()":
            enabled = False

    return total_sum


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
