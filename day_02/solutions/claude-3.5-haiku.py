def read_input():
    with open("../input.txt") as f:
        return f.read().strip().split("\n")


def is_safe_sequence(sequence):
    """
    Check if a sequence is safe based on the given rules:
    1. Levels are either all increasing or all decreasing
    2. Adjacent levels differ by at least 1 and at most 3
    """
    # Check if sequence is increasing
    increasing = all(
        sequence[i + 1] - sequence[i] in range(1, 4) for i in range(len(sequence) - 1)
    )

    # Check if sequence is decreasing
    decreasing = all(
        sequence[i] - sequence[i + 1] in range(1, 4) for i in range(len(sequence) - 1)
    )

    return increasing or decreasing


def part1(data):
    """
    Count the number of safe reports in the input
    """
    safe_reports = 0
    for report in data:
        # Convert report to list of integers
        levels = list(map(int, report.split()))

        # Check if the report is safe
        if is_safe_sequence(levels):
            safe_reports += 1

    return safe_reports


def part2(data):
    """
    Count the number of safe reports when using the Problem Dampener
    which allows removing a single bad level
    """
    safe_reports = 0

    for report in data:
        # Convert report to list of integers
        levels = list(map(int, report.split()))

        # First, check if the original sequence is safe
        if is_safe_sequence(levels):
            safe_reports += 1
            continue

        # Try removing each level to see if it becomes safe
        is_dampener_safe = False
        for i in range(len(levels)):
            # Create a new sequence without the i-th level
            modified_levels = levels[:i] + levels[i + 1 :]

            if is_safe_sequence(modified_levels):
                is_dampener_safe = True
                break

        # If removing a single level makes the report safe, count it
        if is_dampener_safe:
            safe_reports += 1

    return safe_reports


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
