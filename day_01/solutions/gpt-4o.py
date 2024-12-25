def read_input():
    """Read the input from the input.txt file and parse it into two lists."""
    with open("../input.txt") as f:
        lines = f.read().strip().splitlines()

    left, right = [], []
    for line in lines:
        l, r = map(int, line.split())
        left.append(l)
        right.append(r)
    return left, right


def part1(left: list[int], right: list[int]) -> int:
    """Calculate the total distance between two lists based on the smallest pairings."""
    left_sorted = sorted(left)
    right_sorted = sorted(right)

    total_distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))
    return total_distance


def part2(left: list[int], right: list[int]) -> int:
    """Calculate the similarity score based on the occurrence of left elements in the right list."""
    from collections import Counter

    right_counts = Counter(right)
    similarity_score = sum(l * right_counts[l] for l in left)
    return similarity_score


def main():
    left, right = read_input()

    # Part 1
    result1 = part1(left, right)
    print(f"Part 1: {result1}")

    # Part 2
    result2 = part2(left, right)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
