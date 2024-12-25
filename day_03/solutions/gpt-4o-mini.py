import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    Extract valid `mul(X, Y)` instructions and sum their products.
    """
    # Find all valid mul instructions using regex
    mul_pattern = r"mul\((\d+),(\d+)\)"
    mul_instructions = re.findall(mul_pattern, data)

    # Calculate the sum of products of valid mul instructions
    total_sum = sum(int(x) * int(y) for x, y in mul_instructions)

    return total_sum


def part2(data: str) -> int:
    """
    Solution for part 2
    Handle `do()` and `don't()` instructions to enable/disable multiplications.
    """
    enabled = True  # Start with multiplications enabled
    total_sum = 0

    # Regex for matching mul, do(), and don't()
    pattern = r"mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)"
    instructions = re.findall(pattern, data)

    for instruction in instructions:
        mul_x, mul_y = instruction
        if mul_x and mul_y:  # It's a mul instruction
            if enabled:
                total_sum += int(mul_x) * int(mul_y)
        elif "do()" in instruction:  # Enable future mul instructions
            enabled = True
        elif "don't()" in instruction:  # Disable future mul instructions
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
