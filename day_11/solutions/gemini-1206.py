def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def transform_stones(stones):
    new_stones = []
    for stone in stones:
        stone_str = str(stone)
        if stone == 0:
            new_stones.append(1)
        elif len(stone_str) % 2 == 0:
            mid = len(stone_str) // 2
            new_stones.append(int(stone_str[:mid]))
            new_stones.append(int(stone_str[mid:]))
        else:
            new_stones.append(stone * 2024)
    return new_stones


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    stones = [int(x) for x in data.split()]
    for _ in range(25):
        stones = transform_stones(stones)
    return len(stones)


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    stones = [int(x) for x in data.split()]
    prev_time = len(stones)
    for i in range(75):
        stones = transform_stones(stones)
        curr_time = len(stones)
        increase = ((curr_time - prev_time) / prev_time) * 100
        print(f"Iteration {i}: {increase:.2f}% increase")
        prev_time = curr_time
    return len(stones)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
