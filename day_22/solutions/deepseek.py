def read_input():
    with open("../input.txt") as f:
        return [int(line.strip()) for line in f if line.strip()]


def next_secret(secret):
    temp1 = (secret ^ (secret * 64)) % 16777216
    temp2 = (temp1 ^ (temp1 // 32)) % 16777216
    new_secret = (temp2 ^ (temp2 * 2048)) % 16777216
    return new_secret


def get_2000th_secret(initial_secret):
    secret = initial_secret
    for _ in range(2000):
        secret = next_secret(secret)
    return secret


def part1(data):
    total = 0
    for initial_secret in data:
        total += get_2000th_secret(initial_secret)
    return total


def generate_prices(initial_secret, num_secrets=2000):
    secret = initial_secret
    prices = []
    for _ in range(num_secrets):
        secret = next_secret(secret)
        price = secret % 10
        prices.append(price)
    return prices


def compute_changes(prices):
    changes = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        changes.append(change)
    return changes


def find_sequences(changes, prices):
    sequences = {}
    seen = set()
    for i in range(len(changes) - 3):
        seq = tuple(changes[i : i + 4])
        if seq not in seen:
            seen.add(seq)
            price = prices[i + 4]
            sequences[seq] = price
    return sequences


def part2(data):
    sequence_sums = {}
    for initial_secret in data:
        prices = generate_prices(initial_secret)
        changes = compute_changes(prices)
        sequences = find_sequences(changes, prices)
        for seq, price in sequences.items():
            if seq in sequence_sums:
                sequence_sums[seq] += price
            else:
                sequence_sums[seq] = price
    # Find the sequence with the highest sum
    max_sum = -float("inf")
    best_sequence = None
    for seq, total in sequence_sums.items():
        if total > max_sum:
            max_sum = total
            best_sequence = seq
    return max_sum


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
