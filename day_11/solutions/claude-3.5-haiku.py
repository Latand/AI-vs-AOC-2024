def read_input():
    with open("../input.txt") as f:
        return [int(x) for x in f.read().strip().split()]


def part1(stones: list[int]) -> int:
    """
    Solve part 1 by simulating the stone changes for 25 blinks.
    """
    for _ in range(25):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                left, right = str(stone), str(stone)
                new_stones.extend([int(left[:len(left)//2]), int(right[len(right)//:])])
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return len(stones)


def part2(stones: list[int]) -> int:
    """
    Solve part 2 by simulating the stone changes for 75 blinks.
    """
    for _ in range(75):
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                left, right = str(stone), str(stone)
                new_stones.extend([int(left[:len(left)//2]), int(right[len(right)//:])])
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    return len(stones)


def main():
    stones = read_input()

    result1 = part1(stones.copy())
    print(f"Part 1: {result1}")

    result2 = part2(stones.copy())
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()