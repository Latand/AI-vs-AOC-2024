def read_input():
    with open("../input.txt") as f:
        return [list(map(int, line.strip().split())) for line in f if line.strip()]


def is_strictly_monotonic(levels):
    if len(levels) < 2:
        return True  # Single level is trivially safe
    if all(x < y for x, y in zip(levels, levels[1:])):
        return True
    if all(x > y for x, y in zip(levels, levels[1:])):
        return True
    return False


def differences(levels):
    return [abs(x - y) for x, y in zip(levels, levels[1:])]


def is_safe(levels):
    if not is_strictly_monotonic(levels):
        return False
    diffs = differences(levels)
    if all(1 <= d <= 3 for d in diffs):
        return True
    return False


def is_safe_with_dampener(levels):
    if is_safe(levels):
        return True
    for i in range(len(levels)):
        modified = levels[:i] + levels[i + 1 :]
        if is_safe(modified):
            return True
    return False


def main():
    reports = read_input()

    safe_part1 = 0
    safe_part2 = 0

    for report in reports:
        if is_safe(report):
            safe_part1 += 1
            safe_part2 += 1
        else:
            if is_safe_with_dampener(report):
                safe_part2 += 1

    print(f"Part 1: {safe_part1}")
    print(f"Part 2: {safe_part2}")


if __name__ == "__main__":
    main()
