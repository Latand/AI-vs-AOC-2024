import itertools


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def is_safe(report):
    """
    Check if a report is safe based on the rules for Part 1.
    """
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]

    # Check if all differences are within the range of -3 to 3 and non-zero
    if not all(-3 <= diff <= 3 and diff != 0 for diff in differences):
        return False

    # Check if the report is either all increasing or all decreasing
    return all(diff > 0 for diff in differences) or all(
        diff < 0 for diff in differences
    )


def is_safe_with_dampener(report):
    """
    Check if a report is safe based on the rules for Part 2, allowing removal of one level.
    """
    # If the report is already safe, return True
    if is_safe(report):
        return True

    # Try removing each level and check if the resulting report is safe
    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]
        if is_safe(modified_report):
            return True

    return False


def part1(data):
    """
    Count how many reports are safe based on Part 1 rules.
    """
    reports = [list(map(int, line.split())) for line in data]
    return sum(is_safe(report) for report in reports)


def part2(data):
    """
    Count how many reports are safe based on Part 2 rules (with dampener).
    """
    reports = [list(map(int, line.split())) for line in data]
    return sum(is_safe_with_dampener(report) for report in reports)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
