def mix(secret, value):
    return secret ^ value


def prune(secret):
    return secret % 16777216


def next_secret(secret):
    secret = mix(secret, secret * 64)
    secret = prune(secret)
    secret = mix(secret, secret // 32)
    secret = prune(secret)
    secret = mix(secret, secret * 2048)
    secret = prune(secret)
    return secret


def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    initial_secrets = [int(line) for line in data.splitlines()]
    total = 0
    for secret in initial_secrets:
        for _ in range(2000):
            secret = next_secret(secret)
        total += secret
    return total


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    initial_secrets = [int(line) for line in data.splitlines()]
    all_prices = []
    for secret in initial_secrets:
        prices = [secret % 10]
        for _ in range(2000):
            secret = next_secret(secret)
            prices.append(secret % 10)
        all_prices.append(prices)

    best_sequence = None
    max_bananas = 0

    for s1 in range(-9, 10):
        for s2 in range(-9, 10):
            for s3 in range(-9, 10):
                for s4 in range(-9, 10):
                    sequence = (s1, s2, s3, s4)
                    total_bananas = 0
                    for prices in all_prices:
                        changes = [
                            prices[i] - prices[i - 1] for i in range(1, len(prices))
                        ]
                        found = False
                        for i in range(len(changes) - 3):
                            if (
                                changes[i] == sequence[0]
                                and changes[i + 1] == sequence[1]
                                and changes[i + 2] == sequence[2]
                                and changes[i + 3] == sequence[3]
                            ):
                                total_bananas += prices[i + 4]
                                found = True
                                break
                    if total_bananas > max_bananas:
                        max_bananas = total_bananas
                        best_sequence = sequence
    return max_bananas


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
