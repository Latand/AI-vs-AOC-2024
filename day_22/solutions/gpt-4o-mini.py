def read_input():
    with open("../input.txt") as f:
        return f.read().strip().splitlines()


def generate_secret_numbers(initial: int, count: int) -> list[int]:
    secret_numbers = [initial]
    for _ in range(count):
        current = secret_numbers[-1]
        # Step 1: Multiply by 64 and mix
        current = (current * 64) ^ current
        current %= 16777216
        # Step 2: Divide by 32 and mix
        current = (current // 32) ^ current
        current %= 16777216
        # Step 3: Multiply by 2048 and mix
        current = (current * 2048) ^ current
        current %= 16777216
        secret_numbers.append(current)
    return secret_numbers


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    initial_numbers = list(map(int, data))
    total_sum = sum(generate_secret_numbers(num, 2000)[-1] for num in initial_numbers)
    return total_sum


def calculate_price_changes(secret_numbers: list[int]) -> list[int]:
    prices = [num % 10 for num in secret_numbers]
    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    return changes


def find_best_sequence(changes: list[int]) -> int:
    best_sum = 0
    for i in range(len(changes) - 3):
        sequence = changes[i : i + 4]
        current_sum = 0
        for j in range(len(changes) - 3):
            if changes[j : j + 4] == sequence:
                current_sum += (
                    changes[j + 4] + 10
                )  # Adding the price at the time of sale
        best_sum = max(best_sum, current_sum)
    return best_sum


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    initial_numbers = list(map(int, data))
    total_changes = []

    for num in initial_numbers:
        secret_numbers = generate_secret_numbers(num, 2000)
        changes = calculate_price_changes(secret_numbers)
        total_changes.extend(changes)

    best_bananas = find_best_sequence(total_changes)
    return best_bananas


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
