def generate_secret_number(initial_secret):
    """
    Generate the next secret number according to the specified process.

    The process involves three steps:
    1. Multiply by 64 and mix
    2. Divide by 32 and mix
    3. Multiply by 2048 and mix

    Each mix involves bitwise XOR and each step is followed by pruning
    (taking modulo 16777216).
    """
    secret = initial_secret

    # Step 1: Multiply by 64 and mix
    secret ^= (secret * 64) % 16777216
    secret %= 16777216

    # Step 2: Divide by 32 and mix
    secret ^= (secret // 32) % 16777216
    secret %= 16777216

    # Step 3: Multiply by 2048 and mix
    secret ^= (secret * 2048) % 16777216
    secret %= 16777216

    return secret


def part1(data: str) -> int:
    """
    Solve Part 1: Generate 2000 secret numbers for each initial secret
    and sum the 2000th secret number.
    """
    # Convert input to list of initial secret numbers
    initial_secrets = [int(line.strip()) for line in data.split("\n") if line.strip()]

    # Track 2000th secret numbers
    final_secrets = []

    for initial_secret in initial_secrets:
        secret = initial_secret

        # Generate 2000 secret numbers
        for _ in range(2000):
            secret = generate_secret_number(secret)

        final_secrets.append(secret)

    # Sum the 2000th secret numbers
    return sum(final_secrets)


def part2(data: str) -> int:
    """
    Solve Part 2: Find the most bananas by identifying the best
    sequence of four price changes.
    """
    # Convert input to list of initial secret numbers
    initial_secrets = [int(line.strip()) for line in data.split("\n") if line.strip()]

    # Try all possible 4-change sequences
    max_bananas = 0

    # Generate all possible 4-change sequences (-3 to 3, inclusive)
    from itertools import product

    for change_sequence in product(range(-3, 4), repeat=4):
        total_bananas = 0

        # Process each initial secret
        for initial_secret in initial_secrets:
            secret = initial_secret
            prices = []

            # Generate 2000 secret numbers and prices
            for _ in range(2000):
                # Price is the ones digit of the secret number
                prices.append(secret % 10)

                # Generate next secret number
                secret = generate_secret_number(secret)

            # Find first occurrence of the change sequence
            for i in range(len(prices) - 4):
                # Check if price changes match the sequence
                if (
                    prices[i + 1] - prices[i] == change_sequence[0]
                    and prices[i + 2] - prices[i + 1] == change_sequence[1]
                    and prices[i + 3] - prices[i + 2] == change_sequence[2]
                    and prices[i + 4] - prices[i + 3] == change_sequence[3]
                ):
                    # Add the price at the point of selling
                    total_bananas += prices[i + 4]
                    break

        # Update max bananas if necessary
        max_bananas = max(max_bananas, total_bananas)

    return max_bananas


def read_input():
    """Read input from the standard Advent of Code input file."""
    with open("../input.txt") as f:
        return f.read().strip()


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
