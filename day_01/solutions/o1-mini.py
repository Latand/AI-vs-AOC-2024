import re
from collections import Counter


def read_input():
    with open("../input.txt") as f:
        lines = f.readlines()

    left = []
    right = []
    for line in lines:
        # Split the line by whitespace and extract two numbers
        numbers = re.findall(r"\d+", line)
        if len(numbers) >= 2:
            left.append(int(numbers[0]))
            right.append(int(numbers[1]))

    return left, right


def part1(data: tuple) -> int:
    left, right = data
    if len(left) != len(right):
        raise ValueError("Left and right lists must be of the same length for part1.")

    # Sort both lists
    sorted_left = sorted(left)
    sorted_right = sorted(right)

    # Calculate the total distance
    total_distance = 0
    for l, r in zip(sorted_left, sorted_right):
        distance = abs(l - r)
        total_distance += distance

    return total_distance


def part2(data: tuple) -> int:
    left, right = data
    # Count the occurrences of each number in the right list
    right_counter = Counter(right)

    # Calculate the similarity score
    similarity_score = 0
    for number in left:
        count = right_counter.get(number, 0)
        similarity_score += number * count

    return similarity_score


def main():
    left, right = read_input()

    result1 = part1((left, right))
    print(f"Part 1: {result1}")

    result2 = part2((left, right))
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
