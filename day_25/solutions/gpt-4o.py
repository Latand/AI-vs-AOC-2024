def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_schematics(data: str):
    blocks = data.split("\n\n")
    locks = []
    keys = []

    for block in blocks:
        lines = block.splitlines()
        # Skip the first and last rows
        heights = [sum(1 for char in col if char == "#") for col in zip(*lines[1:-1])]
        if lines[0].strip() == "#####":
            locks.append(heights)
        else:
            keys.append(heights)

    return locks, keys


def can_fit(lock, key):
    return all(l + k < 7 for l, k in zip(lock, key))


def part1(data: str) -> int:
    locks, keys = parse_schematics(data)
    count = 0

    for lock in locks:
        for key in keys:
            if can_fit(lock, key):
                count += 1

    return count


def part2(data: str) -> int:
    """
    Solution for part 2
    """
    pass


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
