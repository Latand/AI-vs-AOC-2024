from collections import Counter


def read_input():
    with open("../input.txt") as f:
        return list(map(int, f.read().strip().split()))


def stones_produced(k):
    if k == 0:
        return [1]
    elif len(str(k)) % 2 == 0:
        s = str(k)
        half = len(s) // 2
        left = int(s[:half].lstrip("0") or "0")
        right = int(s[half:].lstrip("0") or "0")
        return [left, right]
    else:
        return [k * 2024]


def part1(data):
    counts = Counter(data)
    N = 25  # Number of blinks
    for _ in range(N):
        new_counts = Counter()
        for k in counts:
            cnt = counts[k]
            produced = stones_produced(k)
            for s in produced:
                new_counts[s] += cnt
        counts = new_counts
    total_stones = sum(counts.values())
    return total_stones


def stone_count(k, n, memo):
    if n == 0:
        return 1
    key = (k, n)
    if key in memo:
        return memo[key]

    if k == 0:
        stones = [1]
    elif len(str(k)) % 2 == 0:
        s = str(k)
        half = len(s) // 2
        left = int(s[:half].lstrip("0") or "0")
        right = int(s[half:].lstrip("0") or "0")
        stones = [left, right]
    else:
        stones = [k * 2024]

    total = 0
    for s in stones:
        total += stone_count(s, n - 1, memo)
    memo[key] = total
    return total


def part2(data):
    N = 75  # Number of blinks
    memo = {}
    total_stones = 0
    for k in data:
        total_stones += stone_count(k, N, memo)
    return total_stones


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
