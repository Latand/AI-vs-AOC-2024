def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    from functools import lru_cache

    stones = list(map(int, data.split()))

    @lru_cache(maxsize=None)
    def count_stones(num, blinks):
        if blinks == 0:
            return 1
        if num == 0:
            return count_stones(1, blinks - 1)
        elif len(str(num)) % 2 == 0:
            digits = str(num)
            half = len(digits) // 2
            left = int(digits[:half].lstrip("0") or "0")
            right = int(digits[half:].lstrip("0") or "0")
            return count_stones(left, blinks - 1) + count_stones(right, blinks - 1)
        else:
            return count_stones(num * 2024, blinks - 1)

    total = 0
    for stone in stones:
        total += count_stones(stone, 25)
    return total


def part2(data: str) -> int:
    stones = list(map(int, data.split()))
    blinks = 75

    from collections import defaultdict

    memo = {}

    def compute(num, remaining):
        key = (num, remaining)
        if key in memo:
            return memo[key]
        if remaining == 0:
            return 1
        if num == 0:
            result = compute(1, remaining - 1)
        elif len(str(num)) % 2 == 0:
            digits = str(num)
            half = len(digits) // 2
            left = int(digits[:half].lstrip("0") or "0")
            right = int(digits[half:].lstrip("0") or "0")
            result = compute(left, remaining - 1) + compute(right, remaining - 1)
        else:
            result = compute(num * 2024, remaining - 1)
        memo[key] = result
        return result

    total = 0
    for stone in stones:
        total += compute(stone, blinks)
    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
