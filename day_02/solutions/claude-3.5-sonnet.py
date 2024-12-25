def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def is_valid_sequence(levels):
    """Check if a sequence of levels is valid according to the rules"""
    if len(levels) < 2:
        return True

    # Check if sequence is increasing or decreasing
    differences = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]

    # All differences should have the same sign (all positive or all negative)
    if not all(d > 0 for d in differences) and not all(d < 0 for d in differences):
        return False

    # Check if differences are between 1 and 3
    return all(1 <= abs(d) <= 3 for d in differences)


def check_with_removal(levels):
    """Check if removing one number makes the sequence valid"""
    # Try removing each number and check if resulting sequence is valid
    for i in range(len(levels)):
        new_levels = levels[:i] + levels[i + 1 :]
        if is_valid_sequence(new_levels):
            return True
    return False


def part1(data: str) -> int:
    """
    Count how many reports are safe according to the original rules
    """
    reports = []
    for line in data.split("\n"):
        if line.strip():
            levels = [int(x) for x in line.strip().split()]
            reports.append(levels)

    safe_count = 0
    for levels in reports:
        if is_valid_sequence(levels):
            safe_count += 1

    return safe_count


def part2(data: str) -> int:
    """
    Count how many reports are safe with the Problem Dampener
    """
    reports = []
    for line in data.split("\n"):
        if line.strip():
            levels = [int(x) for x in line.strip().split()]
            reports.append(levels)

    safe_count = 0
    for levels in reports:
        # Check if sequence is already valid
        if is_valid_sequence(levels):
            safe_count += 1
        # If not valid, check if removing one number makes it valid
        elif check_with_removal(levels):
            safe_count += 1

    return safe_count


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
