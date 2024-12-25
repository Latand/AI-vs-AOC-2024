def read_input():
    with open("../input.txt") as f:
        return f.read().strip()


def compact_disk_part1(disk_map: str) -> int:
    # Simulate the process for part 1: move individual blocks
    blocks = list(disk_map)
    free_space = blocks.count(".")

    # Compress the disk map by moving the file blocks to the left
    # Count the number of file blocks and move them to the left
    file_blocks = [block for block in blocks if block != "."]

    # Fill remaining space with '.' after all the file blocks have been moved
    blocks = file_blocks + ["."] * free_space

    # Calculate the checksum
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != ".":
            checksum += pos * int(block)

    return checksum


def compact_disk_part2(disk_map: str) -> int:
    # Simulate the process for part 2: move whole files
    blocks = list(disk_map)
    free_space = blocks.count(".")

    # Parse files and free space
    files = []
    file_id = 0
    i = 0

    while i < len(blocks):
        # Each file consists of consecutive digits
        if blocks[i] != ".":
            file_length = 0
            while i < len(blocks) and blocks[i] != ".":
                file_length += 1
                i += 1
            files.append((file_id, file_length))
            file_id += 1
        else:
            i += 1

    # Now attempt to move files from the end to the leftmost available space
    # Move files in reverse order of their file ID
    for file_id, file_length in reversed(files):
        # Look for space where this file can be moved
        for j in range(len(blocks) - file_length + 1):
            if all(blocks[k] == "." for k in range(j, j + file_length)):
                # Move the file by placing it in the found space
                for k in range(j, j + file_length):
                    blocks[k] = str(file_id)
                break

    # Calculate the checksum
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != ".":
            checksum += pos * int(block)

    return checksum


def part1(data: str) -> int:
    """
    Solution for part 1: Move individual blocks to the left.
    """
    return compact_disk_part1(data)


def part2(data: str) -> int:
    """
    Solution for part 2: Move whole files to the leftmost free space.
    """
    return compact_disk_part2(data)


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
