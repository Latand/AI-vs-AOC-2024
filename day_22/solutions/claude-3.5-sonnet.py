def read_input():
    with open("../input.txt") as f:
        return [int(x) for x in f.read().strip().split("\n")]


def generate_next_secret(secret: int) -> int:
    # Step 1: Multiply by 64 and mix
    result = secret * 64
    secret ^= result
    secret %= 16777216

    # Step 2: Divide by 32 and mix
    result = secret // 32
    secret ^= result
    secret %= 16777216

    # Step 3: Multiply by 2048 and mix
    result = secret * 2048
    secret ^= result
    secret %= 16777216

    return secret


def generate_sequence(initial: int, count: int) -> list:
    sequence = [initial]
    current = initial

    for _ in range(count):
        current = generate_next_secret(current)
        sequence.append(current)

    return sequence


def get_price_changes(sequence: list) -> list:
    prices = [x % 10 for x in sequence]  # Get ones digit
    changes = []

    for i in range(1, len(prices)):
        changes.append(prices[i] - prices[i - 1])

    return changes


def find_sequence_value(changes: list, target_sequence: list) -> int:
    sequence_len = len(target_sequence)

    for i in range(len(changes) - sequence_len + 1):
        if changes[i : i + sequence_len] == target_sequence:
            # Return the price at the position after the sequence
            return (
                changes[i + sequence_len - 1]
                + changes[i + sequence_len - 2]
                + changes[i + sequence_len - 3]
                + changes[i + sequence_len - 4]
            ) % 10

    return 0


def evaluate_sequence(initial_numbers: list, target_sequence: list) -> int:
    total_bananas = 0

    for initial in initial_numbers:
        sequence = generate_sequence(initial, 2000)
        changes = get_price_changes(sequence)

        for i in range(len(changes) - len(target_sequence) + 1):
            if changes[i : i + len(target_sequence)] == target_sequence:
                total_bananas += sequence[i + len(target_sequence)] % 10
                break

    return total_bananas


def find_best_sequence(initial_numbers: list) -> tuple:
    best_sequence = None
    max_bananas = 0

    # Try all possible sequences of length 4 with values from -9 to 9
    for a in range(-9, 10):
        for b in range(-9, 10):
            for c in range(-9, 10):
                for d in range(-9, 10):
                    sequence = [a, b, c, d]
                    bananas = evaluate_sequence(initial_numbers, sequence)

                    if bananas > max_bananas:
                        max_bananas = bananas
                        best_sequence = sequence

    return best_sequence, max_bananas


def part1(data: str) -> int:
    """
    Solution for part 1: Sum of 2000th secret numbers
    """
    total = 0
    for initial in data:
        sequence = generate_sequence(initial, 2000)
        total += sequence[-1]
    return total


def part2(data: str) -> int:
    """
    Solution for part 2: Maximum possible bananas
    """
    best_sequence, max_bananas = find_best_sequence(data)
    return max_bananas


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
