def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def is_safe_report(levels):
    """
    Check if a report is safe according to the given rules:
    1. Levels are either all increasing or all decreasing.
    2. Adjacent differences are between 1 and 3.
    """
    is_increasing = True
    is_decreasing = True

    for i in range(len(levels) - 1):
        diff = abs(levels[i + 1] - levels[i])

        if diff < 1 or diff > 3:
            return False

        if levels[i + 1] < levels[i]:
            is_increasing = False
        elif levels[i + 1] > levels[i]:
            is_decreasing = False

    return is_increasing or is_decreasing


def part1(data):
    """
    Part 1: Count safe reports where both increasing or decreasing sequences have
    adjacent differences between 1 and 3.
    """
    safe_count = 0
    for report in data:
        levels = list(map(int, report.split()))
        if is_safe_report(levels):
            safe_count += 1
    return safe_count


def is_safe_report_with_dampener(levels):
    """
    Check if a report is safe with the Problem Dampener, which allows one level
    to be removed.
    """
    if is_safe_report(levels):
        return True

    # Try removing each level once and check if it becomes safe
    for i in range(len(levels)):
        modified_levels = levels[:i] + levels[i + 1 :]
        if is_safe_report(modified_levels):
            return True

    return False


def part2(data):
    """
    Part 2: Count safe reports considering the Problem Dampener.
    """
    safe_count = 0
    for report in data:
        levels = list(map(int, report.split()))
        if is_safe_report_with_dampener(levels):
            safe_count += 1
    return safe_count


def main():
    data = read_input()

    # Part 1: Safe reports without the problem dampener
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2: Safe reports with the problem dampener
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
