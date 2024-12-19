def read_input():
    with open("../input.txt") as f:
        raw = f.read()
    return raw


def count_ways(design, patterns):
    # DP array: ways[i] = number of ways to form design[:i]
    ways = [0] * (len(design) + 1)
    ways[0] = 1

    # Precompute pattern lengths and store patterns in a set for quick membership
    # Actually we need to iterate over patterns anyway, but a list is fine.
    for i in range(1, len(design) + 1):
        for p in patterns:
            plen = len(p)
            if i - plen >= 0 and design[i - plen : i] == p:
                ways[i] += ways[i - plen]

    return ways[len(design)]


def part1(designs, patterns):
    # Count how many designs are possible (have at least one arrangement)
    count_possible = 0
    for d in designs:
        if count_ways(d, patterns) > 0:
            count_possible += 1
    return count_possible


def part2(designs, patterns):
    # Sum the number of ways for each design
    total_ways = 0
    for d in designs:
        total_ways += count_ways(d, patterns)
    return total_ways


def main():
    data = read_input().strip("\n")
    # Parse input
    parts = data.split("\n\n")
    # First part: patterns line
    patterns_line = parts[0].strip()
    # After blank line: designs
    designs_lines = parts[1].strip().split("\n")

    # Patterns are comma-separated on the first line
    patterns = [p.strip() for p in patterns_line.split(",") if p.strip()]

    # Compute answers
    result1 = part1(designs_lines, patterns)
    print(f"Part 1: {result1}")

    result2 = part2(designs_lines, patterns)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
