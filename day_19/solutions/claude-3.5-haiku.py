def read_input():
    with open("../input.txt") as f:
        data = f.read().strip().split("\n")

    # Split available patterns and target designs
    sep_index = data.index("")
    patterns = data[:sep_index][0].split(", ")
    designs = data[sep_index + 1 :]

    return patterns, designs


def can_create_design(design: str, patterns: list, memo=None):
    """
    Check if a design can be created and count the number of ways to create it.
    Using memoization to optimize recursive calls.
    """
    if memo is None:
        memo = {}

    # Base cases
    if not design:
        return 1

    if design in memo:
        return memo[design]

    ways = 0
    for pattern in patterns:
        if design.startswith(pattern):
            # Try using this pattern at the start
            remaining_ways = can_create_design(design[len(pattern) :], patterns, memo)
            ways += remaining_ways

    memo[design] = ways
    return ways


def part1(patterns: list, designs: list) -> int:
    """
    Count how many designs are possible.
    """
    return sum(1 for design in designs if can_create_design(design, patterns) > 0)


def part2(patterns: list, designs: list) -> int:
    """
    Count the total number of ways to create all designs.
    """
    return sum(can_create_design(design, patterns) for design in designs)


def main():
    patterns, designs = read_input()
    result1 = part1(patterns, designs)
    print(f"Part 1: {result1}")
    result2 = part2(patterns, designs)

    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
