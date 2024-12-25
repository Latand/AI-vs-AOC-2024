def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def parse_patterns(data: str):
    """Parse the input into locks and keys patterns."""
    patterns = data.split("\n\n")
    locks = []
    keys = []

    for pattern in patterns:
        lines = pattern.split("\n")
        # Skip the first and last line as they are fixed patterns
        pattern_lines = lines[1:-1]

        # Check if it's a lock (top row filled) or key (bottom row filled)
        if lines[0].strip() == "#####":  # It's a lock
            locks.append(pattern_lines)
        else:  # It's a key
            keys.append(pattern_lines)

    return locks, keys


def get_heights(pattern_lines):
    """Convert pattern lines into a list of column heights."""
    heights = []
    # Get the width from the pattern
    width = len(pattern_lines[0])

    for col in range(width):
        height = 0
        # For locks, count from top down
        if pattern_lines[0][col] == "#":
            for row in range(len(pattern_lines)):
                if pattern_lines[row][col] == "#":
                    height += 1
                else:
                    break
        # For keys, count from bottom up
        else:
            for row in range(len(pattern_lines) - 1, -1, -1):
                if pattern_lines[row][col] == "#":
                    height += 1
                else:
                    break
        heights.append(height)

    return heights


def can_fit(lock_heights, key_heights):
    """Check if a key fits in a lock without overlapping."""
    total_height = len(lock_heights) + 1  # Add 1 for the fixed top/bottom rows

    for lock_h, key_h in zip(lock_heights, key_heights):
        if lock_h + key_h > total_height:
            return False
    return True


def part1(data: str) -> int:
    """Count how many unique lock/key pairs fit together without overlapping."""
    locks, keys = parse_patterns(data)

    # Convert patterns to heights
    lock_heights = [get_heights(lock) for lock in locks]
    key_heights = [get_heights(key) for key in keys]

    # Count valid combinations
    valid_pairs = 0
    for lock_h in lock_heights:
        for key_h in key_heights:
            if can_fit(lock_h, key_h):
                valid_pairs += 1

    return valid_pairs


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    main()
