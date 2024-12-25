import re


def read_input():
    """
    Reads the puzzle input from ../input.txt
    Returns it as a list of lists of integers (each report is a list of levels).
    """
    with open("../input.txt") as f:
        lines = f.read().strip().splitlines()

    # We'll split each line on whitespace to get the levels (numbers)
    # Use regex split or just str.split; either works here.
    reports = []
    for line in lines:
        if line.strip():
            # Parse integers
            levels = [int(x) for x in re.split(r"\s+", line.strip())]
            reports.append(levels)

    return reports


def is_safe_report(levels):
    """
    Checks if a report (list of levels) is 'safe' under the original rules (Part 1):
      1) Levels are either strictly increasing or strictly decreasing.
      2) No two adjacent levels differ by 0, or by more than 3.
         (Differences must be in {1, 2, 3} in absolute value.)
    Returns True if safe, False otherwise.

    Edge cases:
      - If there's only one level, we can consider it safe (no differences to violate the rules).
      - If first difference is 0, or out of allowed range, that immediately fails.
    """

    n = len(levels)
    if n < 2:
        # With only one level, there's no difference to check, so it's trivially safe
        return True

    # Calculate differences
    diffs = []
    for i in range(n - 1):
        diff = levels[i + 1] - levels[i]
        # If the difference is zero or out of allowed abs range, it's unsafe
        if diff == 0 or abs(diff) > 3:
            return False
        diffs.append(diff)

    # All diffs must be strictly positive OR strictly negative
    # Check the sign of the first difference
    first_diff_sign = diffs[0] > 0  # True if positive, False if negative

    # If it's actually 0 here, we would've already returned False above.
    # So we know it's either positive or negative.

    for d in diffs:
        if (d > 0) != first_diff_sign:
            # Found a difference that doesn't match the sign of the first difference
            return False

    return True


def is_safe_with_dampener(levels):
    """
    Checks if a report (list of levels) is 'safe' when the Problem Dampener can remove
    exactly one level (or remove none if it's already safe).

    The same rules apply as Part 1, except we are allowed to remove
    one element from the levels to try and make it safe.
    """

    # If it's already safe, no need to remove anything.
    if is_safe_report(levels):
        return True

    # Otherwise, try removing each level in turn and check safety.
    n = len(levels)
    if n <= 2:
        # If n <= 2 and wasn't already safe above, it must fail for some reason
        # (like a 0 difference or something out-of-range). But let's just check anyway:
        # We remove one level and then check the leftover.
        # If after removal we have 1 or 0 levels, that might be trivially safe.
        for i in range(n):
            new_report = levels[:i] + levels[i + 1 :]
            if is_safe_report(new_report):
                return True
        return False

    for i in range(n):
        new_report = levels[:i] + levels[i + 1 :]
        if is_safe_report(new_report):
            return True

    return False


def part1(data):
    """
    Part 1: Count how many reports are safe by the original definition.
    """
    safe_count = 0
    for report in data:
        if is_safe_report(report):
            safe_count += 1
    return safe_count


def part2(data):
    """
    Part 2: Now each report can ignore one "bad" level (via the Problem Dampener).
    Count how many reports are now safe under this rule.
    """
    safe_count = 0
    for report in data:
        if is_safe_with_dampener(report):
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
