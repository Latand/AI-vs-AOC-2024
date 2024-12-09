import re  # Importing regex module


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    # Extract valid mul instructions using regex
    matches = re.findall(r"mul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)", data)
    # Calculate the sum of the products
    return sum(int(x) * int(y) for x, y in matches)


def part2(data: str) -> int:
    """Solve part 2 of the puzzle.

    Handles do() and don't() instructions that enable/disable multiplication operations.
    Only enabled multiplications are included in the final sum.
    """
    # Find all control instructions and multiplications with their positions
    controls = [(m.start(), m.group()) for m in re.finditer(r"do\(\)|don't\(\)", data)]

    muls = [
        (m.start(), int(m.group(1)), int(m.group(2)))
        for m in re.finditer(r"mul\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)", data)
    ]

    # Combine and sort all operations by position
    operations = [(pos, "control", cmd) for pos, cmd in controls] + [
        (pos, "mul", (x, y)) for pos, x, y in muls
    ]
    operations.sort()  # Sort by position

    total = 0
    enabled = True  # Multiplications are enabled by default

    # Process operations in order
    for _, op_type, data in operations:
        if op_type == "control":
            enabled = data == "do()"  # Update state based on control instruction
        elif op_type == "mul" and enabled:
            x, y = data
            total += x * y  # Add multiplication result if enabled

    return total


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
