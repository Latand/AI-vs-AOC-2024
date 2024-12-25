def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_schematics(data):
    locks = []
    keys = []
    blocks = data.split("\n\n")
    for block in blocks:
        lines = block.splitlines()
        if lines[0][0] == "#":
            locks.append(lines)
        else:
            keys.append(lines)
    return locks, keys


def get_heights(schematic):
    heights = []
    for col in range(len(schematic[0])):
        height = 0
        for row in range(len(schematic)):
            if schematic[row][col] == "#":
                height += 1
        heights.append(height)
    return heights


def calculate_heights(schematics):
    result = []
    for schematic in schematics:
        result.append(get_heights(schematic[1:-1]))
    return result


def check_fit(lock_heights, key_heights):
    for lock_height, key_height in zip(lock_heights, key_heights):
        if lock_height + key_height > 6:
            return False
    return True


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    locks, keys = parse_schematics(data)
    lock_heights = calculate_heights(locks)
    key_heights = calculate_heights(keys)

    count = 0
    for l_heights in lock_heights:
        for k_heights in key_heights:
            if check_fit(l_heights, k_heights):
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
