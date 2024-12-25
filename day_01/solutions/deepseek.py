def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    lines = data.splitlines()
    left = []
    right = []
    for line in lines:
        l, r = map(int, line.strip().split())
        left.append(l)
        right.append(r)
    left_sorted = sorted(left)
    right_sorted = sorted(right)
    total_distance = 0
    for l, r in zip(left_sorted, right_sorted):
        total_distance += abs(l - r)
    return total_distance


def part2(data: str) -> int:
    lines = data.splitlines()
    left = []
    right = []
    for line in lines:
        l, r = map(int, line.strip().split())
        left.append(l)
        right.append(r)
    from collections import Counter

    right_counter = Counter(right)
    similarity_score = 0
    for num in left:
        similarity_score += num * right_counter.get(num, 0)
    return similarity_score


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
