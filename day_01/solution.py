from collections import Counter


def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def parse_input(data: str) -> tuple[list[int], list[int]]:
    """
    Parse input into two lists of integers.

    Expected input format:
    Left list numbers on the left, right list numbers on the right
    """
    lines = data.split("\n")
    left_list = []
    right_list = []

    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid input line: {line}")

        try:
            left_list.append(int(parts[0]))
            right_list.append(int(parts[1]))
        except ValueError:
            raise ValueError(f"Non-integer values in line: {line}")

    return left_list, right_list


def part1(data: str) -> int:
    """Solve part 1 of the puzzle: Calculate total distance between sorted lists."""
    left_list, right_list = parse_input(data)

    # Sort both lists
    left_list.sort()
    right_list.sort()

    # Calculate absolute differences and sum them
    total_distance = sum(
        abs(left - right) for left, right in zip(left_list, right_list)
    )

    return total_distance


def part2(data: str) -> int:
    """
    Calculate similarity score by multiplying each left list number
    by its occurrence count in the right list.
    """
    left_list, right_list = parse_input(data)

    # Count occurrences of numbers in the right list
    right_counts = Counter(right_list)

    # Calculate similarity score
    similarity_score = sum(num * right_counts.get(num, 0) for num in left_list)

    return similarity_score


if __name__ == "__main__":
    data = read_input()

    print("Part 1:", part1(data))
    print("Part 2:", part2(data))
