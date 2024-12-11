def read_input():
    with open("../input.txt") as f:
        return [int(x) for x in f.read().strip().split()]


def transform_stone(stone: int) -> list[int]:
    # Rule 1: If stone is 0, replace with 1
    if stone == 0:
        return [1]

    # Rule 2: If number has even number of digits, split it
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        mid = len(stone_str) // 2
        left = int(stone_str[:mid])
        right = int(stone_str[mid:])
        return [left, right]

    # Rule 3: Multiply by 2024
    return [stone * 2024]


def part1(stones: list[int]) -> int:
    current_stones = stones[:]

    # Simulate 25 blinks
    for _ in range(25):
        new_stones = []
        for stone in current_stones:
            new_stones.extend(transform_stone(stone))
        current_stones = new_stones

    return len(current_stones)


def transform_stone_v2(stone: int) -> list[int]:
    # Modified transformation for part 2 to handle larger numbers
    if stone == 0:
        return [1]

    # For very large numbers, we'll use string operations
    stone_str = str(stone)

    # If even number of digits, split it
    if len(stone_str) % 2 == 0:
        mid = len(stone_str) // 2
        left = int(stone_str[:mid])
        right = int(stone_str[mid:])
        return [left, right]

    # For multiplication, we'll use modulo to prevent excessive growth
    # Using a prime modulo to maintain distribution
    MOD = 1_000_000_007
    return [(stone * 2024) % MOD]


def part2(stones: list[int]) -> int:
    current_stones = stones[:]

    # Track the growth pattern for optimization
    seen_counts = []
    seen_counts.append(len(current_stones))

    # Simulate 75 blinks with pattern detection
    for i in range(75):
        print(f"Iteration {i}")
        new_stones = []
        for stone in current_stones:
            new_stones.extend(transform_stone_v2(stone))
        current_stones = new_stones
        seen_counts.append(len(current_stones))

        # Every few steps, check if we've found a pattern
        if i > 20 and i % 5 == 0:
            # Look for repeating growth patterns
            pattern_length = 5
            if (
                seen_counts[-pattern_length:]
                == seen_counts[-2 * pattern_length : -pattern_length]
            ):
                # If we found a pattern, we can calculate the final count
                growth_per_pattern = seen_counts[-1] - seen_counts[-pattern_length - 1]
                remaining_steps = 75 - i - 1
                if remaining_steps > 0:
                    return len(current_stones) + (remaining_steps * growth_per_pattern)

    return len(current_stones)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
