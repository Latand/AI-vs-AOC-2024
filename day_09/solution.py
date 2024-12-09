def read_input():
    with open("input.txt") as f:
        return f.read().strip()


def parse_disk_map(data: str) -> list[tuple[int, int]]:
    """Parse disk map into list of (size, is_file) tuples."""
    return [(int(data[i]), i % 2 == 0) for i in range(len(data))]


def create_block_list(disk_map: list[tuple[int, int]]) -> list[int | None]:
    """Convert disk map to list of blocks where numbers are file IDs and None is free space."""
    blocks = []
    file_id = 0

    for size, is_file in disk_map:
        if is_file:
            blocks.extend([file_id] * size)
            file_id += 1
        else:
            blocks.extend([None] * size)

    return blocks


def compact_disk(blocks: list[int | None]) -> list[int | None]:
    """Move files from right to left to compact the disk."""
    while True:
        # Find rightmost file and leftmost space
        rightmost_file = len(blocks) - 1
        while rightmost_file >= 0 and blocks[rightmost_file] is None:
            rightmost_file -= 1

        if rightmost_file < 0:
            break

        leftmost_space = 0
        while leftmost_space < rightmost_file and blocks[leftmost_space] is not None:
            leftmost_space += 1

        if leftmost_space >= rightmost_file:
            break

        # Move the file
        blocks[leftmost_space] = blocks[rightmost_file]
        blocks[rightmost_file] = None

    return blocks


def calculate_checksum(blocks: list[int | None]) -> int:
    """Calculate checksum by summing position * file_id for all blocks."""
    return sum(
        pos * file_id for pos, file_id in enumerate(blocks) if file_id is not None
    )


def part1(data: str) -> int:
    """Solve part 1 of the puzzle."""
    disk_map = parse_disk_map(data)
    blocks = create_block_list(disk_map)
    compacted = compact_disk(blocks)
    return calculate_checksum(compacted)


def compact_whole_files(blocks: list[int | None]) -> list[int | None]:
    """
    Compact whole files by moving them to the leftmost available free space.

    Files are moved in order of decreasing file ID number starting with the file with the highest file ID number.
    Each file is moved at most once.
    If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.
    """
    # First, identify unique files and their sizes
    file_sizes = {}
    for file_id in set(block for block in blocks if block is not None):
        file_sizes[file_id] = blocks.count(file_id)

    # Sort file IDs in descending order
    sorted_file_ids = sorted(file_sizes.keys(), reverse=True)

    for file_id in sorted_file_ids:
        file_size = file_sizes[file_id]

        # Find current file positions
        current_positions = [i for i, block in enumerate(blocks) if block == file_id]

        # Identify the starting position of the file
        current_start = current_positions[0] if current_positions else None

        if current_start is None:
            continue  # File not found, skip

        # Find the leftmost available free space that can accommodate the file
        start_pos = 0
        while start_pos < current_start:
            # Check if the span from start_pos to start_pos + file_size is free
            if all(
                blocks[pos] is None for pos in range(start_pos, start_pos + file_size)
            ):
                break
            start_pos += 1
        else:
            # No suitable free space found
            continue

        if start_pos != current_start:
            # Move the file to the new position
            for pos in current_positions:
                blocks[pos] = None
            for i in range(start_pos, start_pos + file_size):
                blocks[i] = file_id

    return blocks


def part2(data: str) -> int:
    """Solve part 2 of the puzzle."""
    disk_map = parse_disk_map(data)
    blocks = create_block_list(disk_map)
    compacted = compact_whole_files(blocks)
    return calculate_checksum(compacted)


if __name__ == "__main__":
    data = read_input()
    # print("Part 1:", part1(data))
    print("Part 2:", part2(data))
