import re  # Importing regex module


def parse_input(data: str):
    """
    Parses the input data to extract register values and the program.
    """
    match = re.search(
        r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\nProgram: ([\d,]+)",
        data,
    )
    if match:
        reg_a = int(match.group(1))
        reg_b = int(match.group(2))
        reg_c = int(match.group(3))
        program = list(map(int, match.group(4).split(",")))
        return reg_a, reg_b, reg_c, program
    return None, None, None, []


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    reg_a, reg_b, reg_c, program = parse_input(data)
    output = execute_program(reg_a, reg_b, reg_c, program)
    print(f"Part 1 Output: {output}")
    return output  # Return the output instead of a placeholder


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    reg_a, reg_b, reg_c, program = parse_input(data)
    for initial_a in range(1, 1000000):  # Arbitrary large number for search
        reg_a = initial_a
        output = execute_program(reg_a, reg_b, reg_c, program)
        if output == ",".join(map(str, program)):
            print(f"Part 2 Initial A: {initial_a}")
            return initial_a
    return 0  # Placeholder return value


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
