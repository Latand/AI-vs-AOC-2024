def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def extract_heights(block: str) -> list[int]:
    """
    Extracts the heights of the pins or keys from a given block.
    Skips the first and last rows.
    """
    lines = block.strip().splitlines()[1:-1]  # Skip first and last rows
    heights = [0] * len(lines[0])  # Initialize heights list
    for line in lines:
        for i, char in enumerate(line):
            if char == "#":
                heights[i] += 1  # Increment height for pins
    return heights


def part1(data: str) -> int:
    """
    Solution for part 1
    """
    blocks = data.split("\n\n")  # Split input into blocks
    lock_heights = [extract_heights(block) for block in blocks if block.startswith("#")]
    key_heights = [extract_heights(block) for block in blocks if block.startswith(".")]

    # Check for unique lock/key pairs that fit together
    unique_pairs = 0
    for lock in lock_heights:
        for key in key_heights:
            if all(
                l + k <= 5 for l, k in zip(lock, key)
            ):  # Assuming 5 is the max height
                unique_pairs += 1

    return unique_pairs


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
