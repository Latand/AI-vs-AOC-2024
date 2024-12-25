import re
from collections import Counter


def read_input():
    """
    Reads the puzzle input from ../input.txt and returns two lists:
    left_list, right_list
    Each line in input.txt is expected to have two integers: left_value right_value
    """
    left_list = []
    right_list = []
    with open("../input.txt") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Use regex (or split) to parse two integers per line
            nums = re.findall(r"-?\d+", line)
            if len(nums) == 2:
                left_list.append(int(nums[0]))
                right_list.append(int(nums[1]))
    return left_list, right_list


def part1(left_list, right_list) -> int:
    """
    Part 1:
    1) Sort both lists in ascending order.
    2) Pair the sorted values (i-th in left_list with i-th in right_list).
    3) Sum the absolute difference of each pair.
    """
    sorted_left = sorted(left_list)
    sorted_right = sorted(right_list)
    total_distance = 0
    for l_val, r_val in zip(sorted_left, sorted_right):
        total_distance += abs(l_val - r_val)
    return total_distance


def part2(left_list, right_list) -> int:
    """
    Part 2:
    1) Count frequency of each number in the right_list.
    2) For each value in the left_list, multiply the value by the frequency
       of that value in right_list.
    3) Sum all those products to get the total similarity score.
    """
    freq_right = Counter(right_list)
    total_similarity = 0
    for val in left_list:
        # freq_right[val] gives the count of how many times `val` is in right_list
        total_similarity += val * freq_right[val]
    return total_similarity


def main():
    left_list, right_list = read_input()

    result1 = part1(left_list, right_list)
    print(f"Part 1: {result1}")

    result2 = part2(left_list, right_list)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
