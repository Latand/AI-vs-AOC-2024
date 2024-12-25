def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def is_safe(levels: list[int]) -> bool:
    """
    Checks if a report is safe based on the given rules.
    """
    if len(levels) < 2:
        return True

    increasing = all(levels[i] < levels[i + 1] for i in range(len(levels) - 1))
    decreasing = all(levels[i] > levels[i + 1] for i in range(len(levels) - 1))

    if not (increasing or decreasing):
        return False

    for i in range(len(levels) - 1):
        diff = abs(levels[i + 1] - levels[i])
        if not (1 <= diff <= 3):
            return False

    return True


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    reports = data.splitlines()
    safe_count = 0
    for report in reports:
        levels = [int(x) for x in report.split()]
        if is_safe(levels):
            safe_count += 1
    return safe_count


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    reports = data.splitlines()
    safe_count = 0
    for report in reports:
        levels = [int(x) for x in report.split()]
        if is_safe(levels):
            safe_count += 1
        else:
            for i in range(len(levels)):
                temp_levels = levels[:i] + levels[i + 1 :]
                if is_safe(temp_levels):
                    safe_count += 1
                    break
    return safe_count


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
