def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def part1(data: str) -> int:
    """
    Solution for part 1: Calculate the total distance between the sorted lists.
    """
    # Parse input
    left_list = list(map(int, data[0].split()))
    right_list = list(map(int, data[1].split()))

    # Sort both lists
    left_list.sort()
    right_list.sort()

    # Calculate the total distance
    total_distance = 0
    for a, b in zip(left_list, right_list):
        total_distance += abs(a - b)

    return total_distance


def part2(data: str) -> int:
    """
    Solution for part 2: Calculate the total similarity score.
    """
    # Parse input
    left_list = list(map(int, data[0].split()))
    right_list = list(map(int, data[1].split()))

    # Calculate the total similarity score
    similarity_score = 0
    for num in left_list:
        similarity_score += num * right_list.count(num)

    return similarity_score


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
