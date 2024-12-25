import re


def read_input():
    """Reads the puzzle input from the '../input.txt' file."""
    with open("../input.txt") as f:
        return f.read().strip()


def parse_equations(data: str):
    """
    Parses each line of the input into (target_value, list_of_numbers).

    Example line: '3267: 81 40 27'
      -> (3267, [81, 40, 27])
    """
    equations = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        # Match pattern like '3267: 81 40 27'
        # Group(1) -> '3267'
        # Group(2) -> '81 40 27'
        match = re.match(r"^(\d+):\s+(.+)$", line)
        if not match:
            continue

        target = int(match.group(1))
        numbers_str = match.group(2).split()
        numbers = list(map(int, numbers_str))

        equations.append((target, numbers))

    return equations


def can_make_target(numbers, target, allow_concatenate):
    """
    Returns True if it's possible to form 'target' by inserting
    operators +, * (and optionally || if allow_concatenate=True)
    between the numbers in 'numbers' (evaluated left to right).
    """

    # We'll do a DFS/backtracking approach:
    # current_index = which number we are about to use
    # current_value = the result so far
    # If current_index == len(numbers), check if current_value == target
    # Otherwise, try all possible operators with numbers[current_index].

    # Allowed operators vary depending on part:
    # Part 1 -> ['+', '*']
    # Part 2 -> ['+', '*', '||']

    operators = ["+", "*"]
    if allow_concatenate:
        operators.append("||")

    def dfs(index, current_value):
        # If we've consumed all numbers, check if we hit the target
        if index == len(numbers):
            return current_value == target

        next_num = numbers[index]

        for op in operators:
            if op == "+":
                new_value = current_value + next_num
            elif op == "*":
                new_value = current_value * next_num
            else:  # op == '||'
                # Concatenate as string, then convert back to int
                new_value = int(str(current_value) + str(next_num))

            if dfs(index + 1, new_value):
                return True

        return False

    # Edge case: if there's only one number, check directly
    if len(numbers) == 1:
        return numbers[0] == target

    # Start DFS from the second number, with the first as current_value
    return dfs(1, numbers[0])


def part1(data: str) -> int:
    """
    Part 1: Use only + and * to see if the given sequence of numbers
    can produce the target value (evaluated left to right).
    Sum up all target values that can be produced.
    """
    equations = parse_equations(data)
    total = 0
    for target, nums in equations:
        if can_make_target(nums, target, allow_concatenate=False):
            total += target
    return total


def part2(data: str) -> int:
    """
    Part 2: Use +, *, and ||. Sum up all target values that can be produced.
    """
    equations = parse_equations(data)
    total = 0
    for target, nums in equations:
        if can_make_target(nums, target, allow_concatenate=True):
            total += target
    return total


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
