def read_input():
    """Read the input data from the file."""
    with open("../input.txt") as f:
        return f.read().strip()


def transform_stones(stones):
    """Simulate the transformation of the stones."""
    new_stones = []

    for stone in stones:
        # Rule 1: If the stone is 0, it becomes 1
        if stone == "0":
            new_stones.append("1")
        # Rule 2: If the stone has an even number of digits, split it
        elif len(stone) % 2 == 0:
            mid = len(stone) // 2
            new_stones.append(stone[:mid])
            new_stones.append(stone[mid:])
        # Rule 3: Otherwise, multiply the number by 2024
        else:
            new_stones.append(str(int(stone) * 2024))

    return new_stones


def part1(data: str) -> int:
    """Solve part 1: Simulate 25 blinks."""
    stones = data.split()
    for _ in range(25):
        stones = transform_stones(stones)
    return len(stones)


def part2(data: str) -> int:
    """Solve part 2: Simulate 75 blinks."""
    stones = data.split()
    for _ in range(75):
        stones = transform_stones(stones)
    return len(stones)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
