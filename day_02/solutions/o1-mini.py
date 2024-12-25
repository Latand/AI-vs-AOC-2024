def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def is_strictly_increasing(levels):
    return all(x < y for x, y in zip(levels, levels[1:]))


def is_strictly_decreasing(levels):
    return all(x > y for x, y in zip(levels, levels[1:]))


def has_valid_differences(levels):
    return all(1 <= abs(x - y) <= 3 for x, y in zip(levels, levels[1:]))


def is_safe(levels):
    return (
        is_strictly_increasing(levels) or is_strictly_decreasing(levels)
    ) and has_valid_differences(levels)


def part1(data: str) -> int:
    """
    Counts the number of safe reports based on the initial rules.
    """
    safe_count = 0
    for line in data.splitlines():
        if not line.strip():
            continue  # Skip empty lines
        levels = list(map(int, line.strip().split()))
        if is_safe(levels):
            safe_count += 1
    return safe_count


def can_be_safe_by_removing_one(levels):
    """
    Determines if a report can be made safe by removing exactly one level.
    """
    n = len(levels)
    for i in range(n):
        # Create a new list without the i-th element
        modified = levels[:i] + levels[i + 1 :]
        if is_safe(modified):
            return True
    return False


def part2(data: str) -> int:
    """
    Counts the number of safe reports, allowing for the removal of one level in unsafe reports.
    """
    safe_count = 0
    for line in data.splitlines():
        if not line.strip():
            continue  # Skip empty lines
        levels = list(map(int, line.strip().split()))
        if is_safe(levels):
            safe_count += 1
        elif can_be_safe_by_removing_one(levels):
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
