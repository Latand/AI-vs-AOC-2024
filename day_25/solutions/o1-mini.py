def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    # Parse input into blocks, separated by double newlines
    blocks = data.strip().split("\n\n")

    # Separate lock and key schematics
    lock_schematics = []
    key_schematics = []
    for block in blocks:
        lines = block.strip().split("\n")
        if lines[0].startswith("#"):
            lock_schematics.append(lines)
        else:
            key_schematics.append(lines)

    def schematic_to_heights(schematic, is_lock=True) -> list:
        heights = []
        for col in zip(*schematic[1:-1]):  # Skip first and last rows
            if is_lock:
                # Calculate height from top
                height = sum(1 for c in col if c == "#")
            else:
                # Calculate height from bottom
                height = sum(1 for c in reversed(col) if c == "#")
            heights.append(height)
        return heights

    # Convert schematics to heights
    locks = [schematic_to_heights(s, is_lock=True) for s in lock_schematics]
    keys = [schematic_to_heights(s, is_lock=False) for s in key_schematics]

    # Count valid lock/key pairs
    count = 0
    for lock in locks:
        for key in keys:
            if all(l + k <= 5 for l, k in zip(lock, key)):
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
