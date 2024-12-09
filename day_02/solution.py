def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def is_safe_report(report: list[int]) -> bool:
    """
    Check if a report is safe based on two conditions:
    1. Levels are either all increasing or all decreasing
    2. Adjacent levels differ by at least 1 and at most 3
    """
    # Check if all levels are increasing
    increasing = all(0 < report[i + 1] - report[i] <= 3 for i in range(len(report) - 1))

    # Check if all levels are decreasing
    decreasing = all(0 < report[i] - report[i + 1] <= 3 for i in range(len(report) - 1))

    return increasing or decreasing


def is_safe_with_dampener(report: list[int]) -> bool:
    """
    Check if a report is safe using the Problem Dampener.
    Tries removing each level to see if the resulting report becomes safe.
    """
    # If the original report is already safe, return True
    if is_safe_report(report):
        return True

    # Try removing each level and check if the resulting report is safe
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]
        if is_safe_report(modified_report):
            return True

    return False


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    # Parse input into list of reports
    reports = [[int(level) for level in line.split()] for line in data.split("\n")]

    # Count safe reports
    safe_reports = sum(1 for report in reports if is_safe_report(report))

    return safe_reports


def part2(data: str) -> int:
    """Solve part 2 of the puzzle with Problem Dampener."""
    # Parse input into list of reports
    reports = [[int(level) for level in line.split()] for line in data.split("\n")]

    # Count safe reports using Problem Dampener
    safe_reports = sum(1 for report in reports if is_safe_with_dampener(report))

    return safe_reports


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
