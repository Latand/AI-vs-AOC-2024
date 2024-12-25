import re


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str) -> tuple[list[int], list[int]]:
    """
    Parses the input string into two lists of integers.

    Args:
        data: The input string.

    Returns:
        A tuple containing two lists of integers.
    """
    left_list = []
    right_list = []
    for line in data.splitlines():
        left, right = map(int, re.findall(r"\d+", line))
        left_list.append(left)
        right_list.append(right)
    return left_list, right_list


def part1(data: str) -> int:
    """
    Calculates the total distance between the left and right lists.

    Args:
        data: The input string.

    Returns:
        The total distance between the lists.
    """
    left_list, right_list = parse_input(data)
    left_list.sort()
    right_list.sort()
    total_distance = 0
    for i in range(len(left_list)):
        total_distance += abs(left_list[i] - right_list[i])
    return total_distance


def part2(data: str) -> int:
    """
    Calculates the similarity score between the left and right lists.

    Args:
        data: The input string.

    Returns:
        The similarity score between the lists.
    """
    left_list, right_list = parse_input(data)
    similarity_score = 0
    for num in left_list:
        count = right_list.count(num)
        similarity_score += num * count
    return similarity_score


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
