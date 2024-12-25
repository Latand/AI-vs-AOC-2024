import itertools


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def evaluate(expression):
    result = expression[0]
    for i in range(1, len(expression), 2):
        op = expression[i]
        num = expression[i + 1]
        if op == "+":
            result += num
        elif op == "*":
            result *= num
        elif op == "||":
            result = int(str(result) + str(num))
    return result


def solve(data, operators):
    total_calibration = 0
    lines = data.splitlines()
    for line in lines:
        target, nums_str = line.split(": ")
        target = int(target)
        nums = [int(n) for n in nums_str.split()]

        if len(nums) == 1:
            if nums[0] == target:
                total_calibration += target
            continue

        for ops in itertools.product(operators, repeat=len(nums) - 1):
            expression = [nums[0]]
            for i in range(len(ops)):
                expression.append(ops[i])
                expression.append(nums[i + 1])
            if evaluate(expression) == target:
                total_calibration += target
                break
    return total_calibration


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    return solve(data, ["+", "*"])


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    return solve(data, ["+", "*", "||"])


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
