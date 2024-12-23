from typing import List
from collections import defaultdict


def read_input() -> List[int]:
    with open("../input.txt") as f:
        return [int(line.strip()) for line in f if line.strip()]


def generate_next_secret(secret: int) -> int:
    """
    Generates the next secret number based on the given pseudorandom process.
    """
    # Step 1: Multiply by 64, XOR with current secret, then prune
    secret = (secret * 64) ^ secret
    secret %= 16777216  # Prune to 24 bits

    # Step 2: Divide by 32 (floor division), XOR with current secret, then prune
    secret = (secret // 32) ^ secret
    secret %= 16777216  # Prune to 24 bits

    # Step 3: Multiply by 2048, XOR with current secret, then prune
    secret = (secret * 2048) ^ secret
    secret %= 16777216  # Prune to 24 bits

    return secret


def part1(data: List[int]) -> int:
    """
    Simulates the secret number generation for each buyer and sums the 2000th secret numbers.
    """
    total = 0
    for initial_secret in data:
        secret = initial_secret
        for _ in range(2000):
            secret = generate_next_secret(secret)
        total += secret
    return total


def get_price_changes(secret: int) -> List[int]:
    """
    Generates the first 2000 secret numbers and returns the list of price changes.
    """
    prices = []
    changes = []
    secret = initial_secret = secret
    for _ in range(2000):
        secret = generate_next_secret(secret)
        price = secret % 10
        prices.append(price)
        if len(prices) > 1:
            changes.append(price - prices[-2])
    return changes


def part2(data: List[int]) -> int:
    """
    Determines the best sequence of four price changes to maximize total bananas.
    """
    sequence_to_total = defaultdict(int)

    for initial_secret in data:
        secret = initial_secret
        prices = []
        changes = []
        for _ in range(2000):
            secret = generate_next_secret(secret)
            price = secret % 10
            prices.append(price)
            if len(prices) > 1:
                changes.append(price - prices[-2])

        # Track sequences and the first occurrence price
        seen_sequences = {}
        for i in range(len(changes) - 3):
            seq = tuple(changes[i : i + 4])
            if seq not in seen_sequences:
                seen_sequences[seq] = prices[
                    i + 4
                ]  # Price at which the sequence is completed

        # Update the total bananas for each sequence
        for seq, price in seen_sequences.items():
            sequence_to_total[seq] += price

    # Find the sequence with the maximum total bananas
    if not sequence_to_total:
        return 0  # No sequences found

    best_sequence = max(sequence_to_total, key=lambda k: sequence_to_total[k])
    return sequence_to_total[best_sequence]


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
