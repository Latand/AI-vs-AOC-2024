import re


def read_input():
    """
    Reads the puzzle input from ../input.txt
    Adjust this path if your project structure is different.
    """
    with open("../input.txt") as f:
        return f.read().strip("\n")


def parse_schematics(data: str):
    """
    Split the raw input into separate 7-line blocks (schematics).
    Return a list of blocks, where each block is a list of 7 strings (each 5 chars).
    """
    # Split on blank lines.  You can also do: re.split(r"\n\s*\n", data)
    raw_blocks = data.split("\n\n")

    schematics = []
    for block in raw_blocks:
        lines = block.strip().splitlines()
        # Some blocks could be empty if the input has extra blank lines
        if len(lines) == 7:
            schematics.append(lines)
    return schematics


def is_lock(block: list[str]) -> bool:
    """
    Determine if the 7-line block is a lock:
      - The top row is '#####'
      - The bottom row is '.....'
    """
    return (block[0] == "#####") and (block[-1] == ".....")


def is_key(block: list[str]) -> bool:
    """
    Determine if the 7-line block is a key:
      - The top row is '.....'
      - The bottom row is '#####'
    """
    return (block[0] == ".....") and (block[-1] == "#####")


def get_lock_heights(block: list[str]) -> list[int]:
    """
    Convert a lock schematic into a list of 5 pin heights.
    We only look at the middle 5 rows (indices 1..5).
    For each of the 5 columns, count how many '#' from the top.
    """
    heights = []
    # block[1..5] are the "middle" rows we care about
    # each row is a 5-char string
    middle_rows = block[1:6]  # 5 rows total
    cols = zip(*middle_rows)  # transpose to get columns

    for col in cols:
        # col is a tuple of 5 characters (top to bottom)
        # count '#' from the top
        h = 0
        for ch in col:
            if ch == "#":
                h += 1
            else:
                # as soon as we hit '.', we stop counting (space below the pin)
                break
        heights.append(h)
    return heights


def get_key_heights(block: list[str]) -> list[int]:
    """
    Convert a key schematic into a list of 5 "key heights".
    We only look at the middle 5 rows (indices 1..5).
    For each column, count how many '#' from the BOTTOM.
    """
    heights = []
    middle_rows = block[1:6]  # 5 rows
    # We'll reverse the rows so row[1] is at the top, row[5] is at the bottom
    # but for counting keys, we want to count '#' upward from the bottom
    # so let's look from bottom to top in that 5-row slice
    # i.e. reversed(middle_rows).
    reversed_cols = zip(*reversed(middle_rows))

    for col in reversed_cols:
        # col is now bottom->top for that column
        h = 0
        for ch in col:
            if ch == "#":
                h += 1
            else:
                break
        heights.append(h)
    # Because we used zip(*reversed(middle_rows)), the columns come out in the correct order,
    # but each col was reversed. We computed h in that reversed order, which is correct for a key.
    # Just make sure we keep the same left->right order.
    return heights


def fits_together(lock: list[int], key: list[int]) -> bool:
    """
    Check if this lock and key pair fits in all 5 columns.
    That is, for each column i, lock[i] + key[i] <= 5.
    """
    for l, k in zip(lock, key):
        if l + k > 5:  # 5 is the total vertical space in the middle region
            return False
    return True


def part1(data: str) -> int:
    """
    Solve the puzzle: how many unique lock/key pairs can fit together?
    """
    schematics = parse_schematics(data)

    # Separate blocks into locks and keys, converting them to heights
    locks = []
    keys = []

    for block in schematics:
        if is_lock(block):
            locks.append(get_lock_heights(block))
        elif is_key(block):
            keys.append(get_key_heights(block))
        else:
            # If it doesn't match lock or key pattern, ignore or raise an error
            pass

    # Now test every lock with every key
    valid_pairs = 0
    for lock_heights in locks:
        for key_heights in keys:
            if fits_together(lock_heights, key_heights):
                valid_pairs += 1

    return valid_pairs


def part2(data: str) -> int:
    """
    The puzzle's second part is not revealed yet (per instructions).
    For now, we'll just return 0 or raise NotImplementedError.
    """
    # Not implemented
    raise NotImplementedError("Part 2 has not been revealed yet.")


def main():
    data = read_input()
    result1 = part1(data)
    print(f"Part 1: {result1}")

    # Part 2 is not solved yet, so either skip or show placeholder
    try:
        result2 = part2(data)
        print(f"Part 2: {result2}")
    except NotImplementedError:
        print("Part 2: Not yet implemented.")


if __name__ == "__main__":
    main()
