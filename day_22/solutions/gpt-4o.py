def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def generate_secret_numbers(initial_secret: int, count: int) -> list[int]:
    secret_numbers = []
    secret = initial_secret
    for _ in range(count):
        secret = (secret * 64) ^ (secret // 32) ^ (secret * 2048)
        secret %= 16777216
        secret_numbers.append(secret)
    return secret_numbers


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    initial_secrets = map(int, data.splitlines())
    total = 0
    for secret in initial_secrets:
        secret_numbers = generate_secret_numbers(secret, 2000)
        total += secret_numbers[-1]
    return total


def find_best_sequence(data: str) -> int:
    initial_secrets = map(int, data.splitlines())
    max_bananas = 0
    best_sequence = None

    # Generate all possible sequences of four price changes
    for seq in range(-9, 10):
        for seq2 in range(-9, 10):
            for seq3 in range(-9, 10):
                for seq4 in range(-9, 10):
                    sequence = [seq, seq2, seq3, seq4]
                    bananas = 0

                    for secret in initial_secrets:
                        secret_numbers = generate_secret_numbers(secret, 2000)
                        prices = [num % 10 for num in secret_numbers]
                        changes = [
                            prices[i] - prices[i - 1] for i in range(1, len(prices))
                        ]

                        # Check if the sequence occurs in changes
                        for i in range(len(changes) - 3):
                            if changes[i : i + 4] == sequence:
                                bananas += prices[i + 4]
                                break

                    if bananas > max_bananas:
                        max_bananas = bananas
                        best_sequence = sequence

    return max_bananas


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    return find_best_sequence(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
