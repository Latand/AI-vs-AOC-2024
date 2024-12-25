import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_mul_instructions(memory: str) -> list:
    """
    Parse mul instructions from corrupted memory.
    Handles various possible formats and invalid characters.
    """
    # Regex to match mul instructions with flexible formatting
    mul_pattern = r"mul\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)"

    # Find all valid mul instructions
    matches = re.findall(mul_pattern, memory)

    # Convert matches to list of multiplication tuples
    return [(int(x), int(y)) for x, y in matches]


def solve_part1(memory: str) -> int:
    """
    Solve part 1: Add up results of all mul instructions
    """
    # Get all mul instructions
    mul_instructions = parse_mul_instructions(memory)

    # Calculate and sum the results of mul instructions
    return sum(x * y for x, y in mul_instructions)


def solve_part2(memory: str) -> int:
    """
    Solve part 2: Handle do() and don't() instructions
    """
    # Track whether mul instructions are currently enabled
    mul_enabled = True
    total = 0

    # Use a more complex regex to capture mul, do(), and don't() instructions
    pattern = r"(mul\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)|do\(\)|don\'?t\(\))"
    instructions = re.findall(pattern, memory)

    for instruction in instructions:
        full_match = instruction[0]

        # Check for do() or don't() instructions
        if full_match == "do()":
            mul_enabled = True
        elif full_match == "don't()":
            mul_enabled = False

        # Check for mul instruction
        elif mul_enabled:
            x, y = int(instruction[1]), int(instruction[2])
            total += x * y

    return total


def main():
    memory = read_input()

    result1 = solve_part1(memory)
    print(f"Part 1: {result1}")

    result2 = solve_part2(memory)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
