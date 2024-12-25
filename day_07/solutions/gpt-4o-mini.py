import itertools


def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def apply_operator(left, right, operator):
    if operator == "+":
        return left + right
    elif operator == "*":
        return left * right
    elif operator == "||":
        return int(f"{left}{right}")


def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i in range(len(operators)):
        result = apply_operator(result, numbers[i + 1], operators[i])
    return result


def generate_operator_combinations(num_count, operators):
    return itertools.product(operators, repeat=num_count - 1)


def part1(data):
    valid_test_values = 0
    for line in data:
        test_value_str, nums_str = line.split(":")
        test_value = int(test_value_str.strip())
        nums = list(map(int, nums_str.split()))

        # Generate all combinations of + and * operators
        operator_combinations = generate_operator_combinations(len(nums), ["+", "*"])

        for operators in operator_combinations:
            result = evaluate_expression(nums, operators)
            if result == test_value:
                valid_test_values += test_value
                break  # No need to check further combinations for this line

    return valid_test_values


def part2(data):
    valid_test_values = 0
    for line in data:
        test_value_str, nums_str = line.split(":")
        test_value = int(test_value_str.strip())
        nums = list(map(int, nums_str.split()))

        # Generate all combinations of +, * and || operators
        operator_combinations = generate_operator_combinations(
            len(nums), ["+", "*", "||"]
        )

        for operators in operator_combinations:
            result = evaluate_expression(nums, operators)
            if result == test_value:
                valid_test_values += test_value
                break  # No need to check further combinations for this line

    return valid_test_values


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
