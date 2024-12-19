import os
from typing import Set


def read_input() -> str:
    """
    Reads the input from ../input.txt and returns it as a single string.
    """
    input_path = os.path.join(os.path.dirname(__file__), "../input.txt")
    with open(input_path, "r") as f:
        return f.read().strip()


def parse_input(data: str):
    """
    Parses the input data into towel patterns and desired designs.
    """
    towel_patterns_part, designs_part = data.split("\n\n")
    towel_patterns = [pattern.strip() for pattern in towel_patterns_part.split(",")]
    desired_designs = [
        line.strip() for line in designs_part.strip().split("\n") if line.strip()
    ]
    return towel_patterns, desired_designs


def part1(data: str) -> int:
    """
    Counts how many designs can be constructed using the available towel patterns.
    """
    towel_patterns, desired_designs = parse_input(data)
    towel_set: Set[str] = set(towel_patterns)
    possible_count = 0

    for design in desired_designs:
        n = len(design)
        dp = [False] * (n + 1)
        dp[0] = True  # Empty string is always constructible

        for i in range(1, n + 1):
            for pattern in towel_set:
                pl = len(pattern)
                if pl <= i and design[i - pl : i] == pattern and dp[i - pl]:
                    dp[i] = True
                    break  # No need to check other patterns if one matches

        if dp[n]:
            possible_count += 1

    return possible_count


def part2(data: str) -> int:
    """
    Counts the total number of different ways all designs can be constructed.
    """
    towel_patterns, desired_designs = parse_input(data)
    towel_set: Set[str] = set(towel_patterns)
    total_ways = 0

    for design in desired_designs:
        n = len(design)
        dp = [0] * (n + 1)
        dp[0] = 1  # One way to construct an empty string

        for i in range(1, n + 1):
            for pattern in towel_set:
                pl = len(pattern)
                if pl <= i and design[i - pl : i] == pattern:
                    dp[i] += dp[i - pl]

        total_ways += dp[n]

    return total_ways


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
