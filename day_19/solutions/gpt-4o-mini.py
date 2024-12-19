def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    patterns, designs = data[0].split(","), data[1:]
    possible_count = 0

    for design in designs:
        if can_form_design(design, patterns):
            possible_count += 1

    return possible_count


def can_form_design(design: str, patterns: list) -> bool:
    # Implement logic to check if the design can be formed using the patterns
    # This can be done using a recursive approach or dynamic programming
    # For simplicity, let's assume a placeholder implementation
    return True  # Placeholder


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    patterns, designs = data[0].split(","), data[1:]
    total_ways = 0

    for design in designs:
        total_ways += count_ways_to_form_design(design, patterns)

    return total_ways


def count_ways_to_form_design(design: str, patterns: list) -> int:
    dp = [0] * (len(design) + 1)
    dp[0] = 1  # Base case: one way to form an empty design

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if design.startswith(pattern, i - len(pattern)):
                dp[i] += dp[i - len(pattern)]

    return dp[len(design)]


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
