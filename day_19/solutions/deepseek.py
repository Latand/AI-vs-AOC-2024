def read_input():
    with open("../input.txt") as f:
        lines = f.read().strip().splitlines()
    blank_line = lines.index("")
    patterns = set(lines[0].split(", "))
    designs = lines[blank_line + 1 :]
    return patterns, designs


def part1(patterns, designs):
    count = 0
    for design in designs:
        n = len(design)
        dp = [False] * (n + 1)
        dp[0] = True
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and design[j:i] in patterns:
                    dp[i] = True
                    break
        if dp[n]:
            count += 1
    return count


def part2(patterns, designs):
    total = 0
    for design in designs:
        n = len(design)
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] > 0 and design[j:i] in patterns:
                    dp[i] += dp[j]
        total += dp[n]
    return total


def main():
    patterns, designs = read_input()

    result1 = part1(patterns, designs)
    print(f"Part 1: {result1}")

    result2 = part2(patterns, designs)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
