def read_input(file_path):
    with open(file_path, "r") as f:
        return list(map(int, f.read().strip().split()))


def simulate_blinks(stones, blinks):
    for _ in range(blinks):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                mid = len(str(stone)) // 2
                left = int(str(stone)[:mid])
                right = int(str(stone)[mid:])
                new_stones.extend([left, right])
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return len(stones)


# Part 1


def part1(file_path):
    stones = read_input(file_path)
    return simulate_blinks(stones, 25)


# Part 2 with an optimized approach


def simulate_blinks_optimized(stones, blinks):
    from collections import Counter

    # Track stones and their counts using a Counter
    current_state = Counter(stones)

    for _ in range(blinks):
        next_state = Counter()
        for stone, count in current_state.items():
            if stone == 0:
                next_state[1] += count
            elif len(str(stone)) % 2 == 0:
                mid = len(str(stone)) // 2
                left = int(str(stone)[:mid])
                right = int(str(stone)[mid:])
                next_state[left] += count
                next_state[right] += count
            else:
                next_state[stone * 2024] += count
        current_state = next_state

    # Return total number of stones
    return sum(current_state.values())


def part2(file_path):
    stones = read_input(file_path)
    return simulate_blinks_optimized(stones, 75)


if __name__ == "__main__":
    input_file = "../input.txt"  # Update with your input file path

    # Solve Part 1
    result1 = part1(input_file)
    print(f"Part 1: {result1}")

    # Solve Part 2
    result2 = part2(input_file)
    print(f"Part 2: {result2}")
