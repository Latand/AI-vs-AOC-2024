def apply_operator(a, b, operator):
    if operator == "+":
        return a + b
    elif operator == "*":
        return a * b
    elif operator == "||":
        return int(str(a) + str(b))
    else:
        raise ValueError("Unknown operator")


def compute_possible_results(numbers, operators):
    if not numbers:
        return set()

    possible_results = {numbers[0]}
    for num in numbers[1:]:
        next_possible = set()
        for prev in possible_results:
            for op in operators:
                try:
                    result = apply_operator(prev, num, op)
                    next_possible.add(result)
                except:
                    continue
        possible_results = next_possible
    return possible_results


def main():
    # Read input from input.txt
    with open("../input.txt", "r") as f:
        lines = f.read().splitlines()

    total_sum = 0
    # operators = ['+', '*']       # Uncomment for part one
    operators = ["+", "*", "||"]  # For part two

    for line in lines:
        if not line:
            continue
        parts = line.strip().split(": ", 1)
        if len(parts) != 2:
            continue
        test_value_str, numbers_str = parts
        test_value = int(test_value_str)
        numbers = list(map(int, numbers_str.strip().split()))

        possible_results = compute_possible_results(numbers, operators)
        if test_value in possible_results:
            total_sum += test_value

    print(total_sum)


if __name__ == "__main__":
    main()
