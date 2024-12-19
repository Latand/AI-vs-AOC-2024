from typing import List, Dict


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    patterns, designs = data.split("\n\n")
    patterns = [p.strip() for p in patterns.split(",")]
    designs = [d.strip() for d in designs.splitlines()]
    return patterns, designs


def can_match_pattern(
    design: str, patterns: List[str], memo: Dict[str, bool] = None
) -> bool:
    if memo is None:
        memo = {}

    if design == "":
        return True
    if design in memo:
        return memo[design]

    for pattern in patterns:
        if design.startswith(pattern):
            if can_match_pattern(design[len(pattern) :], patterns, memo):
                memo[design] = True
                return True

    memo[design] = False
    return False


def count_combinations(
    design: str, patterns: List[str], memo: Dict[str, int] = None
) -> int:
    if memo is None:
        memo = {}

    if design == "":
        return 1
    if design in memo:
        return memo[design]

    total = 0
    for pattern in patterns:
        if design.startswith(pattern):
            total += count_combinations(design[len(pattern) :], patterns, memo)

    memo[design] = total
    return total


def part1(data: str) -> int:
    patterns, designs = parse_input(data)

    possible_count = 0
    for design in designs:
        if can_match_pattern(design, patterns):
            possible_count += 1

    return possible_count


def part2(data: str) -> int:
    patterns, designs = parse_input(data)

    total_combinations = 0
    for design in designs:
        if can_match_pattern(design, patterns):  # Only count if it's possible
            combinations = count_combinations(design, patterns)
            total_combinations += combinations

    return total_combinations


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
