def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_input(data: str):
    """
    Parse the input into two lists of integers.

    Args:
        data (str): Raw input data

    Returns:
        tuple: Two lists of integers representing left and right lists
    """
    lines = data.split("\n")
    left_list = []
    right_list = []

    for line in lines:
        # Split each line into left and right numbers
        left, right = map(int, line.split())
        left_list.append(left)
        right_list.append(right)

    return left_list, right_list


def part1(data: str) -> int:
    """
    Calculate total distance between sorted left and right lists.

    Args:
        data (str): Raw input data

    Returns:
        int: Total distance between paired numbers
    """
    left_list, right_list = parse_input(data)

    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate distances
    total_distance = sum(
        abs(left - right) for left, right in zip(left_sorted, right_sorted)
    )

    return total_distance


def part2(data: str) -> int:
    """
    Calculate similarity score by counting occurrences.

    Args:
        data (str): Raw input data

    Returns:
        int: Total similarity score
    """
    left_list, right_list = parse_input(data)

    # Count occurrences of right list numbers
    right_counts = {}
    for num in right_list:
        right_counts[num] = right_counts.get(num, 0) + 1

    # Calculate similarity score
    similarity_score = sum(num * right_counts.get(num, 0) for num in left_list)

    return similarity_score


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: Total distance = {result1}")

    result2 = part2(data)
    print(f"Part 2: Similarity score = {result2}")


if __name__ == "__main__":
    main()
