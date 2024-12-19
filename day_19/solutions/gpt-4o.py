def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    lines = data.splitlines()
    patterns = lines[0].split(", ")
    designs = lines[2:]
    return patterns, designs


def can_construct(design, patterns):
    dp = [False] * (len(design) + 1)
    dp[0] = True

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and design[i - len(pattern) : i] == pattern:
                dp[i] = dp[i] or dp[i - len(pattern)]

    return dp[len(design)]


def count_ways(design, patterns):
    dp = [0] * (len(design) + 1)
    dp[0] = 1

    for i in range(1, len(design) + 1):
        for pattern in patterns:
            if i >= len(pattern) and design[i - len(pattern) : i] == pattern:
                dp[i] += dp[i - len(pattern)]

    return dp[len(design)]


def part1(data: str) -> int:
    patterns, designs = parse_input(data)
    count = 0
    for design in designs:
        if can_construct(design, patterns):
            count += 1
    return count


def part2(data: str) -> int:
    patterns, designs = parse_input(data)
    total_ways = 0
    for design in designs:
        total_ways += count_ways(design, patterns)
    return total_ways


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
