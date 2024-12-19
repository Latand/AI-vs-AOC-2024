def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def solve():
    data = read_input()
    parts = data.split("\n\n")
    towels = parts[0].split(", ")
    designs = parts[1].split("\n")

    def can_make(design, towels):
        dp = [False] * (len(design) + 1)
        dp[0] = True
        for i in range(len(design)):
            if dp[i]:
                for towel in towels:
                    if design[i:].startswith(towel):
                        dp[i + len(towel)] = True
        return dp[len(design)]

    count = 0
    for design in designs:
        if can_make(design, towels):
            count += 1
    print(f"Part 1: {count}")

    def count_ways(design, towels):
        dp = [0] * (len(design) + 1)
        dp[0] = 1
        for i in range(len(design)):
            if dp[i] > 0:
                for towel in towels:
                    if design[i:].startswith(towel):
                        dp[i + len(towel)] += dp[i]
        return dp[len(design)]

    total_ways = 0
    for design in designs:
        ways = count_ways(design, towels)
        if ways > 0:
            total_ways += ways
    print(f"Part 2: {total_ways}")


if __name__ == "__main__":
    solve()
