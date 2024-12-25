def read_input():
    """Read and parse input into two lists of numbers"""
    with open("../input.txt") as f:
        lines = f.read().strip().split("\n")

    left_list = []
    right_list = []

    for line in lines:
        left, right = line.split()
        left_list.append(int(left))
        right_list.append(int(right))

    return left_list, right_list


def part1(data: tuple[list[int], list[int]]) -> int:
    """
    Calculate total distance between paired sorted numbers from both lists.

    Args:
        data: Tuple of (left_list, right_list) containing numbers

    Returns:
        Total distance between paired numbers
    """
    left_list, right_list = data

    # Sort both lists to pair smallest with smallest
    sorted_left = sorted(left_list)
    sorted_right = sorted(right_list)

    total_distance = 0

    # Calculate distance between each pair
    for left, right in zip(sorted_left, sorted_right):
        distance = abs(left - right)
        total_distance += distance

    return total_distance


def part2(data: tuple[list[int], list[int]]) -> int:
    """
    Calculate similarity score by multiplying each left number by its frequency
    in the right list.

    Args:
        data: Tuple of (left_list, right_list) containing numbers

    Returns:
        Total similarity score
    """
    left_list, right_list = data

    # Count frequencies in right list
    right_frequencies = {}
    for num in right_list:
        right_frequencies[num] = right_frequencies.get(num, 0) + 1

    similarity_score = 0

    # Calculate similarity score for each number in left list
    for num in left_list:
        # Multiply number by its frequency in right list (0 if not present)
        frequency = right_frequencies.get(num, 0)
        similarity_score += num * frequency

    return similarity_score


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
